#!/usr/bin/env python3
"""离线检查镜头 JSON；仅依赖 Python 3 标准库，不写文件、不联网。

这是格式/数值/引用检查器，不是剧情、授权或图像质量判断器。
用法：python3 tools/check_shots.py <shots.json> --assets <assets.json> --root .
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

FRAMINGS = {"远景", "全景", "中景", "近景", "特写", "大特写"}
METHODS = {"静帧运镜", "图生视频", "后期合成", "实拍"}
KINDS = {"character", "scene", "prop", "sound", "music", "voice", "image", "video"}
STATUSES = {"planned", "generated", "approved", "rejected"}
REQUIRED = {
    "shot_id", "scene_id", "source_refs", "purpose", "framing", "angle",
    "camera_move", "action", "dialogue", "voiceover", "sfx", "edit_duration_s",
    "generation_duration_s", "recorded_audio_duration_s", "asset_ids",
    "continuity_in", "continuity_out", "production_method", "post_notes",
}


def is_number(value: Any, minimum: float = 0, strict: bool = False) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if not math.isfinite(value):
        return False
    return value > minimum if strict else value >= minimum


def in_enum(value: Any, allowed: Any) -> bool:
    return isinstance(value, str) and value in allowed


def string_list(value: Any, nonempty: bool = False) -> bool:
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(isinstance(x, str) and bool(x.strip()) for x in value))


def validate(doc: Any, assets_doc: Any, root: Path) -> Tuple[List[str], List[str], Dict[str, Any]]:
    errors: List[str] = []
    warnings: List[str] = []
    summary: Dict[str, Any] = {"shot_count": 0, "total_duration_s": 0.0}
    root = root.resolve()
    if not isinstance(doc, dict) or not isinstance(assets_doc, dict):
        return ["镜头与资产 JSON 顶层必须都是对象。"], [], summary
    if doc.get("schema_version") != "1.0" or assets_doc.get("schema_version") != "1.0":
        errors.append("schema_version 必须为字符串 1.0。")
    if not in_enum(doc.get("status"), {"draft", "approved"}):
        errors.append("镜头表 status 必须为 draft 或 approved；approved 仍需外部人工确认记录。")
    episode = doc.get("episode_id")
    if not isinstance(episode, str) or not re.fullmatch(r"EP\d{2,}", episode):
        errors.append("episode_id 应形如 EP01。")
        episode = "EP01"
    numeric_config = {
        "target_duration_s": (True, 60),
        "duration_tolerance_s": (False, 2),
        "speech_rate_assumption_chars_per_s": (True, 4),
        "pause_allowance_s": (False, 0.8),
    }
    config: Dict[str, float] = {}
    for key, (strict, fallback) in numeric_config.items():
        value = doc.get(key)
        if not is_number(value, strict=strict):
            errors.append("%s 必须为有限%s数值。" % (key, "正" if strict else "非负"))
            value = fallback
        config[key] = float(value)
    assets = assets_doc.get("assets")
    if not isinstance(assets, list):
        return errors + ["assets 必须是列表。"], warnings, summary
    registry: Dict[str, Dict[str, Any]] = {}
    for index, item in enumerate(assets, 1):
        tag = "资产第%d项" % index
        if not isinstance(item, dict):
            errors.append(tag + "必须是对象。")
            continue
        aid = item.get("asset_id")
        if not isinstance(aid, str) or not aid.strip():
            errors.append(tag + "缺少有效 asset_id。")
            continue
        if aid in registry:
            errors.append("重复资产编号：" + aid)
        registry[aid] = item
        if not in_enum(item.get("kind"), KINDS) or not in_enum(item.get("status"), STATUSES):
            errors.append(aid + " 的 kind/status 无效。")
        if not isinstance(item.get("label"), str) or not item["label"].strip():
            errors.append(aid + " 缺少 label。")
        if "path" not in item:
            errors.append(aid + " 缺少 path；尚未生成用 null。")
        path = item.get("path")
        if path is not None and (not isinstance(path, str) or not path.strip()):
            errors.append(aid + " 的 path 应为非空字符串或 null。")
            continue
        if path:
            rel = Path(path)
            candidate = (root / rel).resolve()
            try:
                candidate.relative_to(root)
                inside = not rel.is_absolute()
            except ValueError:
                inside = False
            if not inside:
                errors.append(aid + " 的 path 超出项目根目录或不是相对路径。")
            elif not candidate.is_file():
                errors.append(aid + " 登记了不存在的文件：" + path)
            if item.get("status") == "planned":
                warnings.append(aid + " 已登记路径但仍为 planned，请核实实际状态。")
        elif in_enum(item.get("status"), {"generated", "approved"}):
            errors.append(aid + " 标为已生成/确认，但没有真实 path。")
    shots = doc.get("shots")
    if not isinstance(shots, list) or not shots:
        return errors + ["shots 必须是非空列表；空模板不能当成成品。"], warnings, summary
    seen = set()
    used = set()
    total = 0.0
    for index, shot in enumerate(shots, 1):
        if not isinstance(shot, dict):
            errors.append("第%d镜必须是对象。" % index)
            continue
        sid = shot.get("shot_id")
        tag = sid if isinstance(sid, str) and sid else "第%d镜" % index
        missing = sorted(REQUIRED - set(shot))
        if missing:
            errors.append(tag + " 缺字段：" + ", ".join(missing))
        if not isinstance(sid, str) or not re.fullmatch(re.escape(episode) + r"_SH\d{3,}", sid):
            errors.append(tag + " 镜号应形如 " + episode + "_SH001。")
        elif sid in seen:
            errors.append("重复镜号：" + sid)
        else:
            seen.add(sid)
        for key in ("scene_id", "purpose", "framing", "angle", "camera_move", "action",
                    "continuity_in", "continuity_out", "production_method"):
            if not isinstance(shot.get(key), str) or not shot[key].strip():
                errors.append(tag + " 的 " + key + " 必须为非空文字。")
        for key in ("voiceover", "sfx", "post_notes"):
            if not isinstance(shot.get(key), str):
                errors.append(tag + " 的 " + key + " 必须为文字；未使用填空字符串。")
        if not in_enum(shot.get("framing"), FRAMINGS):
            errors.append(tag + " 景别不在约定范围。")
        if not in_enum(shot.get("production_method"), METHODS):
            errors.append(tag + " 制作方式不在约定范围。")
        if not string_list(shot.get("source_refs"), nonempty=True):
            errors.append(tag + " 需要非空 source_refs 列表。")
        duration = shot.get("edit_duration_s")
        duration_ok = is_number(duration, strict=True)
        if not duration_ok:
            errors.append(tag + " edit_duration_s 必须是有限正数。")
        else:
            total += float(duration)
        generated = shot.get("generation_duration_s")
        if generated is not None and not is_number(generated, strict=True):
            errors.append(tag + " generation_duration_s 应为正数或 null。")
        elif generated is not None and duration_ok and generated < duration:
            warnings.append(tag + " 生成时长小于采用时长；请说明慢放、延帧或其他处理。")
        ids = shot.get("asset_ids")
        if not string_list(ids, nonempty=True):
            errors.append(tag + " 需要非空 asset_ids 列表。")
            ids = []
        for aid in ids:
            used.add(aid)
            if aid not in registry:
                errors.append(tag + " 引用了未登记素材：" + aid)
            elif registry[aid].get("status") == "rejected":
                errors.append(tag + " 引用了已淘汰素材：" + aid)
        dialogue = shot.get("dialogue")
        spoken = shot.get("voiceover") if isinstance(shot.get("voiceover"), str) else ""
        if not isinstance(dialogue, list):
            errors.append(tag + " dialogue 必须是列表。")
            dialogue = []
        for entry in dialogue:
            if not isinstance(entry, dict):
                errors.append(tag + " 每项对白必须是对象。")
                continue
            speaker = entry.get("speaker_id")
            text = entry.get("text")
            if not isinstance(text, str) or not text.strip():
                errors.append(tag + " 对白 text 必须为非空文字。")
            else:
                spoken += text
            if not isinstance(speaker, str) or speaker not in registry:
                errors.append(tag + " 对白说话人未登记。")
            elif registry[speaker].get("kind") != "character":
                errors.append(tag + " 对白说话人必须是 character 资产。")
            elif speaker not in ids:
                warnings.append(tag + " 说话人不在本镜素材清单，请核实是否画外音：" + speaker)
        audio = shot.get("recorded_audio_duration_s")
        if audio is not None and not is_number(audio):
            errors.append(tag + " recorded_audio_duration_s 应为非负数或 null。")
        elif duration_ok:
            if audio is not None:
                if audio > duration:
                    warnings.append(tag + " 实测声音 %.2f 秒超过采用 %.2f 秒。" % (audio, duration))
                if spoken and audio == 0:
                    warnings.append(tag + " 有对白/旁白但实测时长为零，请核实。")
            elif spoken:
                count = sum(c.isalnum() for c in spoken)
                estimate = count / config["speech_rate_assumption_chars_per_s"] + config["pause_allowance_s"]
                if estimate > duration:
                    warnings.append(tag + " 声音粗估 %.2f 秒超过采用 %.2f 秒；请朗读验证。" % (estimate, duration))
    summary = {"shot_count": len(shots), "total_duration_s": round(total, 6),
               "target_duration_s": config["target_duration_s"], "used_asset_count": len(used)}
    if abs(total - config["target_duration_s"]) > config["duration_tolerance_s"] + 1e-9:
        errors.append("采用总时长 %.2f 秒与目标 %.2f 秒的差超过允许误差 %.2f 秒。" %
                      (total, config["target_duration_s"], config["duration_tolerance_s"]))
    pending = sorted(a for a in used if a in registry and registry[a].get("status") == "planned")
    if pending:
        warnings.append("以下仅为计划素材，尚非真实成品：" + ", ".join(pending))
    warnings.append("数值检查不验证原文证据、剧情/空间逻辑、画面质量、商用权或人工批准。")
    return errors, warnings, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shots", type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        with args.shots.open(encoding="utf-8-sig") as handle:
            doc = json.load(handle)
        with args.assets.open(encoding="utf-8-sig") as handle:
            assets = json.load(handle)
        errors, warnings, summary = validate(doc, assets, args.root)
    except (OSError, ValueError) as exc:
        print("读取失败：%s" % exc, file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for msg in errors:
        print("[错误] " + msg)
    for msg in warnings:
        print("[提醒] " + msg)
    print("结果：" + ("存在错误，请修复。" if errors else "格式/数值检查通过；仍需人工复核。"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
