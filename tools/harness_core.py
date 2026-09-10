"""Offline contracts and media inspection for the manju v2 preview harness.
Python >= 3.9, standard library only. Never makes network requests.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

class StudioError(ValueError):
    """Actionable validation or execution error."""


def require(ok: bool, message: str) -> None:
    if not ok:
        raise StudioError(message)


def integer(x: Any, name: str, low: int = 0, high: int = 10**9) -> int:
    require(type(x) is int and low <= x <= high, f'{name}: 需要 {low}..{high} 的整数，不能是布尔值')
    return x


def number(x: Any, name: str, low: float, high: float) -> float:
    require(type(x) in (int, float) and math.isfinite(x) and low <= x <= high,
            f'{name}: 需要 {low}..{high} 的有限数值')
    return float(x)


def text(x: Any, name: str) -> str:
    require(isinstance(x, str) and bool(x.strip()) and '\x00' not in x, f'{name}: 需要非空文字')
    return x


def fields(obj: Any, required: set[str], optional: set[str], name: str) -> None:
    require(isinstance(obj, dict), f'{name}: 需要对象')
    missing = required - obj.keys()
    extra = obj.keys() - required - optional
    require(not missing, f'{name}: 缺少 {sorted(missing)}')
    require(not extra, f'{name}: 不支持字段 {sorted(extra)}，不得静默丢弃')


def safe_path(root: Path, value: Any, must_exist: bool = False) -> Path:
    text(value, 'path')
    require(not any(c in value for c in ('\n', '\r', '\\', ':')), '路径不能含换行、反斜杠或协议/盘符')
    p = Path(value)
    require(not p.is_absolute() and '..' not in p.parts and value not in ('.', ''), '必须是项目内相对文件路径')
    base = root.resolve()
    result = (base / p).resolve()
    require(result.is_relative_to(base), f'路径越出项目（包括符号链接）: {value}')
    if must_exist:
        require(result.is_file() and result.stat().st_size > 0, f'文件缺失或为空: {value}')
    return result


def output_path(root: Path, value: str, suffix: str) -> Path:
    p = safe_path(root, value)
    require(Path(value).parts[0] in ('08_audio', '10_edit', '11_exports', '07_reviews', '12_runs'), '输出只能写入后期/检查/任务目录，不得改原稿或输入素材')
    require(p.suffix.lower() == suffix, f'输出必须使用 {suffix} 后缀')
    require(not p.exists(), f'拒绝覆盖已有文件: {value}，请使用新版本名')
    return p


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def canonical_hash(value: Any) -> str:
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    except (TypeError, ValueError) as e:
        raise StudioError(f'无法计算规范哈希: {e}') from e
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def valid_hash(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def read_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f'非法 JSON 常量 {value}')
    def no_duplicate(pairs: list[tuple[str, Any]]) -> dict:
        result: dict = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'JSON 重复键 {key}')
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant, object_pairs_hook=no_duplicate)
    except (OSError, UnicodeError, ValueError) as e:
        raise StudioError(f'无法读取 JSON {path.name}: {e}') from e


def run(argv: list[str], timeout: int = 60, cwd: Path | None = None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise StudioError(f'本地工具失败: {e}') from e
    require(result.returncode == 0, f'{Path(argv[0]).name} 失败: {result.stderr[-6000:]}')
    return result


def probe(path: Path, count_frames: bool = False) -> dict:
    binary = shutil.which('ffprobe')
    require(bool(binary), '缺少 ffprobe；请由用户决定是否安装 FFmpeg，不自动安装')
    cmd = [binary, '-v', 'error', '-protocol_whitelist', 'file,pipe', '-show_format', '-show_streams', '-of', 'json']
    if count_frames:
        cmd.append('-count_frames')
    cmd.append(str(path))
    try:
        return json.loads(run(cmd, timeout=120).stdout)
    except ValueError as e:
        raise StudioError(f'ffprobe 没有返回有效 JSON: {e}') from e


def stream_duration(info: dict, kind: str) -> float | None:
    """Use the selected stream, not container duration when A/V lengths differ."""
    streams = [s for s in info.get('streams', []) if s.get('codec_type') == kind]
    if not streams:
        return None
    s = streams[0]
    candidates = [s.get('duration')]
    ticks, base = s.get('duration_ts'), s.get('time_base')
    if ticks is not None and base:
        try:
            candidates.append(float(Fraction(str(base))) * int(ticks))
        except (ValueError, ZeroDivisionError):
            pass
    # Some Matroska files expose duration in stream tags only.
    stamp = s.get('tags', {}).get('DURATION')
    if isinstance(stamp, str) and re.fullmatch(r'\d+:\d{2}:\d{2}(\.\d+)?', stamp):
        h, m, sec = stamp.split(':')
        candidates.append(int(h) * 3600 + int(m) * 60 + float(sec))
    if len(info.get('streams', [])) == 1:
        candidates.append(info.get('format', {}).get('duration'))
    for value in candidates:
        try:
            f = float(value)
            if math.isfinite(f) and f > 0:
                return f
        except (ValueError, TypeError):
            pass
    return None


def timing_fingerprint(tl: dict) -> str:
    return canonical_hash({k: tl[k] for k in ('fps_num', 'fps_den', 'duration_frames', 'video', 'audio')})


def request_fingerprint(job: dict) -> str:
    return canonical_hash({k: job.get(k) for k in ('type', 'provider', 'model', 'input_refs', 'parameters')})


def file_ref(root: Path, obj: dict, check_files: bool, allowed: set[str] | None = None) -> Path:
    p = safe_path(root, obj.get('path'), must_exist=check_files)
    require(valid_hash(obj.get('sha256')), f'{obj.get("path")}: 需要真实的64位小写 SHA-256；未知素材只能留在草案模板，不能通过生产校验')
    if allowed:
        require(p.suffix.lower() in allowed, f'不支持该媒体扩展名: {p.suffix}')
    if check_files:
        require(sha256_file(p) == obj['sha256'], f'素材哈希不匹配，需复核采用版本: {obj["path"]}')
    return p


def parse_srt(content: str, max_ms: int | None = None) -> list[dict]:
    require(isinstance(content, str) and bool(content.strip()), 'SRT 不能为空')
    blocks = re.split(r'\n[ \t]*\n', content.replace('\r\n', '\n').strip('\ufeff \n'))
    pattern = r'(\d{2,}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2,}):(\d{2}):(\d{2}),(\d{3})'
    result, previous_end = [], 0
    for i, block in enumerate(blocks, 1):
        lines = block.splitlines()
        require(len(lines) >= 3 and lines[0] == str(i), f'SRT 第{i}段序号或文本错误')
        m = re.fullmatch(pattern, lines[1])
        require(m is not None, f'SRT 第{i}段时间格式不正确')
        v = [int(x) for x in m.groups()]
        require(v[1] < 60 and v[2] < 60 and v[5] < 60 and v[6] < 60, 'SRT 分秒值越界')
        start = ((v[0]*60+v[1])*60+v[2])*1000+v[3]
        end = ((v[4]*60+v[5])*60+v[6])*1000+v[7]
        require(start >= previous_end and end > start, 'SRT 重叠、倒序或零时长；当前后端只接受单轨非重叠字幕')
        if max_ms is not None:
            require(end <= max_ms, 'SRT 超过成片时长')
        require(bool('\n'.join(lines[2:]).strip()), 'SRT 文本为空')
        result.append({'start_ms': start, 'end_ms': end, 'text': '\n'.join(lines[2:])})
        previous_end = end
    return result


def validate_timeline(tl: Any, root: Path, check_files: bool = False) -> dict:
    fields(tl, {'schema_version','episode_id','status','fps_num','fps_den','width','height','duration_frames','video','audio','subtitles'}, {'notes'}, 'timeline')
    require(tl['schema_version'] == '2.0', '仅支持 timeline v2.0')
    text(tl['episode_id'], 'episode_id')
    require(tl['status'] in ('draft','approved'), '时间线 status 只能 draft/approved')
    fps = Fraction(integer(tl['fps_num'], 'fps_num', 1, 120000), integer(tl['fps_den'], 'fps_den', 1, 10000))
    require(1 <= fps <= 60, '基础预览器只处理 1..60 fps')
    w, h = integer(tl['width'],'width',16,1280), integer(tl['height'],'height',16,1280)
    require(w % 2 == 0 and h % 2 == 0 and w*h <= 921600, '预览尺寸须偶数且不超过921600像素')
    total = integer(tl['duration_frames'], 'duration_frames', 1)
    duration = float(total/fps)
    require(duration <= 180, '本预览器单片上限180秒；较长片需另行确认并扩展后端')
    require(isinstance(tl['video'],list) and 1 <= len(tl['video']) <= 60, '需要1..60个实际画面事件')
    require(isinstance(tl['audio'],list) and len(tl['audio']) <= 64, 'audio 应为最多64项的列表')
    ids: set[str] = set(); cursor = 0; inspected: dict[str, dict] = {}; warnings = []
    def media_info(path: Path) -> dict:
        key = str(path)
        if key not in inspected:
            inspected[key] = probe(path)
        return inspected[key]
    def event_base(c: dict) -> tuple[int,int]:
        cid = text(c['clip_id'],'clip_id')
        require(cid not in ids, f'重复 clip_id {cid}'); ids.add(cid)
        text(c['asset_id'], 'asset_id')
        st = integer(c['start_frame'], 'start_frame')
        n = integer(c['duration_frames'], 'duration_frames', 1)
        integer(c['source_in_ms'], 'source_in_ms')
        require(st+n <= total, f'{cid}: 事件超出时间线')
        return st,n
    for c in tl['video']:
        fields(c, {'clip_id','shot_id','asset_id','kind','path','sha256','start_frame','duration_frames','source_in_ms','fit','motion','playback_rate','source_audio'}, set(), 'video event')
        st, n = event_base(c); text(c['shot_id'],'shot_id')
        require(st == cursor, f'{c["clip_id"]}: 画面有空隙/重叠/倒序，当前只支持连续硬切'); cursor += n
        require(c['kind'] in ('image','video'), '画面 kind 仅 image/video')
        require(c['fit'] in ('contain','cover'), 'fit 仅 contain/cover')
        require(c['motion'] == 'none' and type(c['playback_rate']) in (int,float) and c['playback_rate'] == 1 and c['source_audio'] == 'drop', '当前预览器不支持运镜、变速或自动视频原声混入；必须显式简化/扩展')
        if c['kind']=='image':
            require(c['source_in_ms']==0, '静图 source_in_ms 必须为0')
        allowed = {'.png','.jpg','.jpeg','.webp'} if c['kind']=='image' else {'.mp4','.mov','.mkv','.webm'}
        p=file_ref(root,c,check_files,allowed)
        if check_files:
            info=media_info(p)
            require(any(s.get('codec_type')=='video' and not s.get('disposition',{}).get('attached_pic') for s in info.get('streams',[])), f'{c["path"]}: 没有有效画面流')
            if c['kind']=='video':
                seconds=stream_duration(info,'video')
                require(seconds is not None, f'{c["path"]}: 无可靠视频流时长，先正规化/实测再导入')
                require(c['source_in_ms']/1000+n/float(fps) <= seconds+1/float(fps), f'{c["clip_id"]}: 采用区间超过源视频时长')
    require(cursor == total, '画面事件没有覆盖总帧数')
    for c in tl['audio']:
        fields(c, {'clip_id','asset_id','kind','path','sha256','start_frame','duration_frames','source_in_ms','gain_db','fade_in_frames','fade_out_frames'}, {'line_id'}, 'audio event')
        st,n=event_base(c)
        require(c['kind'] in ('dialogue','music','sfx','ambience'), '未知声音类型')
        if c.get('line_id') is not None: text(c['line_id'],'line_id')
        number(c['gain_db'],'gain_db',-60,12)
        fi=integer(c['fade_in_frames'],'fade_in_frames');fo=integer(c['fade_out_frames'],'fade_out_frames')
        require(fi+fo<=n,'声音淡入淡出不能超过片段长度')
        p=file_ref(root,c,check_files,{'.wav','.mp3','.flac','.m4a','.aac','.ogg','.mp4','.mov','.mkv','.webm'})
        if check_files:
            info=media_info(p);seconds=stream_duration(info,'audio')
            require(seconds is not None, f'{c["path"]}: 没有可靠音频流时长，先实测/正规化')
            require(c['source_in_ms']/1000+n/float(fps)<=seconds+1/float(fps),f'{c["clip_id"]}: 采用区间超出真实音频，不能靠补静音假装台词完整')
    if not tl['audio']:
        warnings.append('没有配音/声音事件；渲染只会增加静音轨，不代表已配音。')
    if tl['subtitles'] is not None:
        sub=tl['subtitles']
        fields(sub, {'path','sha256','mode','language'}, set(), 'subtitles')
        require(sub['mode'] in ('sidecar','soft'), '字幕仅支持外挂/软字幕，未接烧录')
        require(isinstance(sub['language'],str) and re.fullmatch('[a-z]{3}',sub['language']) is not None,'字幕 language 使用三位语言标记，如 zho')
        p=file_ref(root,sub,check_files,{'.srt'})
        if check_files:
            parse_srt(p.read_text(encoding='utf-8-sig'),round(duration*1000))
    return {'valid':True,'duration_s':duration,'frames':total,'fps':str(fps),'files_checked':check_files,'warnings':warnings,'timing_sha256':timing_fingerprint(tl)}


def validate_alignment(obj: Any, tl: dict, root: Path) -> dict:
    validate_timeline(tl,root,False)
    fields(obj, {'schema_version','episode_id','status','timing_source','timeline_timing_sha256','review_reference','cues'}, set(), 'alignment')
    require(obj['schema_version']=='2.0' and obj['episode_id']==tl['episode_id'],'对齐版本/集号不匹配')
    require(obj['status']=='verified' and obj['timing_source'] in ('manual_verified','provider_verified','aligner_verified'),'估算/草稿对齐不能导出正式SRT；先用真实音频验证')
    text(obj['review_reference'],'review_reference')
    require(obj['timeline_timing_sha256']==timing_fingerprint(tl),'对齐已失效：时间线或音频变化，请重新核验，不要直接伪改指纹')
    require(isinstance(obj['cues'],list) and bool(obj['cues']),'没有实际cue')
    limit=round(tl['duration_frames']*tl['fps_den']/tl['fps_num']*1000)
    audio_ids={a['asset_id'] for a in tl['audio']}
    ids=set();previous=0
    for cue in obj['cues']:
        fields(cue,{'cue_id','line_id','speaker_id','audio_asset_id','start_ms','end_ms','text'},set(),'cue')
        for name in ('cue_id','line_id','speaker_id','audio_asset_id','text'):text(cue[name],name)
        require(cue['cue_id'] not in ids,'重复 cue_id');ids.add(cue['cue_id'])
        require(cue['audio_asset_id'] in audio_ids,'cue 指向未采用的音频素材')
        st=integer(cue['start_ms'],'start_ms');end=integer(cue['end_ms'],'end_ms',1)
        require(st>=previous and st<end<=limit,'cue 重叠、倒序、零长或超出时间线')
        require('\n\n' not in cue['text'] and '\r' not in cue['text'],'字幕正文不能含空段或 CR')
        candidates=[a for a in tl['audio'] if a['asset_id']==cue['audio_asset_id']]
        frame_ms=tl['fps_den']/tl['fps_num']*1000
        require(any(st >= a['start_frame']*frame_ms-1 and end <= (a['start_frame']+a['duration_frames'])*frame_ms+1 for a in candidates),'cue 超出该采用音频事件的范围')
        previous=end
    return {'valid':True,'cue_count':len(obj['cues']),'note':'格式/版本一致性通过，不替代听检'}


def srt_text(obj: dict) -> str:
    def stamp(ms: int) -> str:
        sec,frac=divmod(ms,1000);minute,s=divmod(sec,60);h,m=divmod(minute,60)
        return f'{h:02d}:{m:02d}:{s:02d},{frac:03d}'
    return '\n\n'.join(f'{i}\n{stamp(c["start_ms"])} --> {stamp(c["end_ms"])}\n{c["text"]}' for i,c in enumerate(obj['cues'],1))+'\n'


def validate_job(job: Any, root: Path, check_files: bool = False) -> dict:
    fields(job, {'schema_version','job_id','episode_id','type','status','provider','model','input_refs','parameters','request_fingerprint','approval_ref','budget','attempt','max_attempts','provider_job_id','outputs','error','review_status','depends_on'}, set(), 'job')
    require(job['schema_version']=='2.0','job版本不支持')
    for k in ('job_id','episode_id'):text(job[k],k)
    require(job['type'] in ('image','tts','video','alignment','music','sfx','lipsync'),'job类型不支持')
    statuses={'planned','awaiting_approval','ready','submitted','running','succeeded','failed','cancelled','needs_reconciliation','stale'}
    require(job['status'] in statuses,'未知job状态')
    require(job['review_status'] in ('not_reviewed','approved','rejected'),'未知review_status')
    require(isinstance(job['input_refs'],list) and isinstance(job['outputs'],list) and isinstance(job['parameters'],dict) and isinstance(job['depends_on'],list),'job refs/parameters/depends_on类型错误')
    attempt=integer(job['attempt'],'attempt');maximum=integer(job['max_attempts'],'max_attempts',1)
    require(attempt<=maximum,'已超出批准/计划尝试次数')
    for ref in job['input_refs']:file_ref(root,ref,check_files)
    b=job['budget'];fields(b,{'currency','max_cost','estimated_cost','estimate_source','actual_cost'},set(),'budget')
    text(b['currency'],'currency');cap=number(b['max_cost'],'max_cost',0,10**9)
    for k in ('estimated_cost','actual_cost'):
        if b[k] is not None:
            require(number(b[k],k,0,10**9)<=cap,f'{k} 超出该job费用上限；停止并核账')
    active=job['status'] in ('ready','submitted','running','succeeded','needs_reconciliation')
    if active:
        text(job['provider'],'provider');text(job['model'],'model')
        require(job['request_fingerprint']==request_fingerprint(job),'请求指纹未锁定或输入已变化')
        if job['provider']!='manual_import':
            require(b['estimated_cost'] is not None and b['estimate_source'] is not None,'外部任务缺少费用估算和来源')
            ap=safe_path(root,job['approval_ref'],True)
            approval=read_json(ap)
            require(approval.get('status')=='approved' and bool(approval.get('user_statement')) and bool(approval.get('confirmed_at')),'没有有效用户批准记录')
            require(job['job_id'] in approval.get('scope_job_ids',[]) and job['request_fingerprint'] in approval.get('scope_request_fingerprints',[]),'批准不覆盖该任务及请求版本')
            require(approval.get('provider')==job['provider'] and approval.get('model')==job['model'] and approval.get('currency')==b['currency'],'批准与服务/模型/币种不匹配')
            require(number(approval.get('max_cost'),'approval.max_cost',0,10**9)>=cap,'job上限高于批次批准')
            require(integer(approval.get('max_attempts_per_job'),'批准尝试上限',1)>=maximum,'job尝试上限超过批准')
    if job['status'] in ('submitted','running','needs_reconciliation'):
        require(attempt>=1,'已提交任务 attempt 至少1')
        # Unknown ID after a submission timeout is deliberately permitted only for reconciliation.
        if job['status']!='needs_reconciliation':text(job['provider_job_id'],'provider_job_id')
    if job['status']=='succeeded':
        require(bool(job['outputs']),'不能没有真实输出就标 succeeded')
        for ref in job['outputs']:
            p=file_ref(root,ref,check_files)
            if ref.get('duration_ms') is not None:integer(ref['duration_ms'],'duration_ms',1)
            if check_files:
                info=probe(p)
                require(bool(info.get('streams')),'输出不是真实媒体')
    return {'valid':True,'status':job['status'],'files_checked':check_files,'request_fingerprint':request_fingerprint(job),'note':'不是批次总账核算、权限沙箱或真实媒体内容验收'}
