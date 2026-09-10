# 初始化检查报告 v01

检查时间：2026-09-10T14:37:13+08:00  
项目根目录：`/Users/chengchengxu/Desktop/ai-video-studio`  
报告文件：`07_reviews/setup_check_v01.md`  
任务状态：`completed`（仅初始化检查）；用户对作品/媒体的批准状态：未批准。  
检查依据：本轮用户明确要求仅初始化；采用 `manju-producer` 技能。

初始化检查通过：六个指定入口文件均存在且已读取，十四个技能文件全部存在且非空，Python、FFmpeg、ffprobe 可运行。本地基础粗剪依赖检查通过；云端生成、自动对齐及剪辑软件原生接口仍为 `unconfigured`。此结论不表示已生成、渲染或验收任何媒体。

## 1. 本轮范围与状态

- 当前运行模式：`plan`。
- `external_generation_allowed=false`；批准的外部生成预算：CNY 0；`approval_ref=null`；自动云端重试关闭。
- 外部生成/API 调用次数：0；上传文件数：0；本轮外部生成/API 费用：CNY 0。Codex 会话费用未由本检查计量，记为 `unknown`。
- 未写故事、提示词或正式制作任务；未生图、配音、生成视频、渲染、安装依赖或修改全局配置。
- 未运行 `render`（含 dry-run）、`smoke_test.py` 或媒体集成测试；未读取/使用 `examples` 内容，未把示例计入正式作品。
- 本轮仅新增此检查报告；原稿、`PROJECT.md`、`STATE.md`、配置、技能和工具代码不变。制作阶段仍以现有 `STATE.md` 为准；该文件的“下一步先运行初始化检查”是检查前文字，本报告记录本次检查已完成，不改变作品采用版本。
- 报告按 `setup_check_vNN.md` 递增，以独占创建方式写入；已有同名文件时使用更高版本，不覆盖。

## 2. 十四个技能文件

检查位置：`.agents/skills/<技能名>/SKILL.md`。逐项核实存在、非空并计算 SHA-256；本轮只完整阅读并应用 `manju-producer`，其余技能没有进入制作执行。

| 技能 | 职责 | 文件检查 |
|---|---|---|
| manju-producer | 初始化、统筹与恢复 | 存在、非空（1816 B） |
| manju-story | 小说事实拆解、大纲与人物 | 存在、非空（2396 B） |
| manju-script | 场景剧本与台词 | 存在、非空（2278 B） |
| manju-audit | 剧情与连续性审校 | 存在、非空（2121 B） |
| manju-shots | 文字镜头表 | 存在、非空（2620 B） |
| manju-visual | 文字视觉设定 | 存在、非空（2087 B） |
| manju-prompts | 图像提示词与任务单 | 存在、非空（2642 B） |
| manju-images | 图像任务、导入与验收 | 存在、非空（1456 B） |
| manju-voice | 音色试音、逐句配音任务与导入 | 存在、非空（1978 B） |
| manju-video | 图生视频任务、导入与取用区间 | 存在、非空（1644 B） |
| manju-subtitles | 真实音频字幕对齐与复核 | 存在、非空（1698 B） |
| manju-sound | 声音设计与混音检查 | 存在、非空（1517 B） |
| manju-edit | 中立时间线与基础粗剪 | 存在、非空（1955 B） |
| manju-delivery | 交付检查与打包 | 存在、非空（1595 B） |

结果：14/14；缺失：0。文件存在仅证明技能文件已提供；doctor 不验证 Codex 对全部技能的运行时加载，也不测试创作质量。

## 3. 本机工具可用性

| 工具 | 实测版本 | 路径 | 结果 |
|---|---|---|---|
| Python | 3.14.5 | 命令入口 `/Users/chengchengxu/.pyenv/shims/python3`；实际解释器 `/usr/local/opt/python@3.14/bin/python3.14` | 可运行，满足 Python ≥ 3.9 |
| FFmpeg | 8.1.1 | `/usr/local/bin/ffmpeg` | 可运行 |
| ffprobe | 8.1.1 | `/usr/local/bin/ffprobe` | 可运行 |

执行命令：

```sh
command -v python3
python3 --version
PYTHONDONTWRITEBYTECODE=1 python3 tools/studio.py doctor --root .
```

doctor 退出码为 0，`local_preview_dependencies_ready=true`。命令级的 `PYTHONDONTWRITEBYTECODE=1` 用于避免导入脚本时新建 Python 字节码缓存，不修改全局配置。

doctor 实际检查了 FFmpeg/ffprobe 版本、编码器 `libx264`、`aac`、`pcm_s16le`，以及以下滤镜：

`scale, pad, crop, fps, format, setsar, tpad, trim, setpts, atrim, asetpts, aresample, aformat, volume, afade, adelay, amix, alimiter, anullsrc`。

这些命令只查询版本与能力列表。基础依赖可用不等于媒体端到端验证通过；软字幕额外编码器 `mov_text`、实际媒体解码/渲染、播放器兼容性、视听质量、响度均为 `not_checked`。

## 4. 已实现与已提供的能力

依据：`CAPABILITIES.md`、`HARNESS.md`、`config/providers.json`、`tools/README.md` 及对应 Python 入口/函数。本轮执行验证范围仅为 doctor；其余为文档与代码结构核对。

| 能力 | 当前状态 | 已实现范围与验证边界 |
|---|---|---|
| 十四个技能与制作交接流程 | 指令已提供 | 文本工作与任务编排；技能本身不是图像、声音或视频模型 |
| doctor 环境检查 | `implemented`，本轮运行通过 | Python、技能文件、工具路径/版本、基础编码器/滤镜检查；不安装 |
| timeline/job/alignment 检查 | `implemented` | 结构、路径、数值、哈希与部分状态检查；不证明内容质量、用户批准或账户限额 |
| 镜头表检查 | `implemented` | 存在 `tools/check_shots.py` 的验证与 CLI 入口；本轮未运行素材/镜头验证 |
| 文件 SHA-256 与时间线/任务指纹 | `implemented` | `studio.py hash` 与对应核心函数；本轮另以标准库计算输入文件与报告哈希 |
| 音视频 probe | `implemented` | 读取真实媒体流和时长；本轮未探测正式媒体 |
| 已核验 alignment JSON → SRT | `implemented` | 导出已经核验的对齐数据，拒绝估算时间；不会执行 ASR 或自动强制对齐 |
| 本地 FFmpeg 基础粗剪 | `implemented_requires_local_binaries`；基础依赖可用 | 单画面轨硬切、静帧保持、片段裁切、contain/cover；音轨定位、增益、淡变、混合和限幅；外挂/软字幕。未渲染验证 |
| 人工导入图片/音频/视频 | `documented` | 仅有 agent 引导的本地导入流程，需用户提供真实文件及来源；没有自动云端生成/下载适配器 |

本地粗剪边界：最长 180 秒；最大边长 1280 像素且总像素不超过 921600；最多 60 个画面片段、64 个音频事件。默认丢弃源视频声音，需显式列入音轨才混入。基础混合/限幅不代表最终响度达标。中立 `timeline.json` 不是剪映、Final Cut 或 Resolve 原生工程。

## 5. 尚未接入与当前不支持的能力

| 能力/接口 | 状态 | 当前证据 |
|---|---|---|
| 实际生图与图像编辑 | `unconfigured` | `active.image=null`；`cloud_image.implementation=null` |
| 配音：MiniMax / OpenAI TTS | `unconfigured` | `active.tts=null`；两项适配器均 `status=unconfigured`、`implementation=null`，模型未选 |
| 图生视频及服务商原生音频 | `unconfigured` | `active.video=null`；`cloud_video.implementation=null`；未接入生成服务 |
| ASR / 自动强制对齐 | `unconfigured` | `active.alignment=null`；`speech_alignment.implementation=null`；JSON → SRT 不能代替自动对齐 |
| 音乐/音效生成及智能混音服务 | `unconfigured` | `active.music=null`；`music_sfx.implementation=null`；基础本地音轨混合已实现 |
| 口型同步 | `unconfigured` | `active.lipsync=null`；`lipsync.implementation=null` |
| 剪映 / Final Cut / Resolve 原生工程、GUI、OTIO/FCPXML/Resolve 脚本接口 | `unconfigured` | `nle_export.implementation=null`；当前 `active.editor=ffmpeg_preview` 只指向本包粗剪后端 |
| 运镜、叠画、转场、变速、自动 ducking、烧录字幕 | `unsupported`（当前预览器） | 现有 FFmpeg 粗剪后端不支持；没有已接入的替代后端 |
| 自动发布、后台排队 | `not_implemented` | 能力文档明确未实现 |

配置文件仅登记能力与约定；环境变量名不是密钥，也不表示 API 已接通。本轮没有读取密钥、连接供应商或新增配置。

## 6. 读取、检查与输出文件

完整阅读：

- `AGENTS.md`、`PROJECT.md`、`STATE.md`、`HARNESS.md`、`CAPABILITIES.md`、`config/runtime.json`。
- `.agents/skills/manju-producer/SKILL.md`。
- `config/providers.json`、`tools/README.md`、`07_reviews/README.md`、`tools/studio.py`。

代码局部阅读/结构检索：`tools/render_preview.py` 的依赖检查与粗剪代码、`tools/harness_core.py` 的路径/哈希/子进程逻辑与函数索引、`tools/check_shots.py` 的函数与入口索引。其余十三个技能只做文件存在性、大小和哈希检查，未全量载入正文。

项目外流程指引：读取 `/Users/chengchengxu/.codex/skills/codex-session-cleanup/SKILL.md`。按全局 AGENTS 指令执行 `~/.agents/skills/codex-session-cleanup/scripts/cleanup_codex_processes.sh --verbose`，退出码 0，返回 `candidates=0 members=0 rss_kib=0`，无需终止进程。

输出：仅 `07_reviews/setup_check_v01.md`；真实图片、配音、视频、字幕、时间线及媒体任务产物数均为 0。报告写入后独立读回并计算 SHA-256；哈希在交接中提供，不将文件自身哈希写入自身。

以下 SHA-256 用于固定本次输入版本；写入前后对全部 27 项已记录输入文件核对，任何差异均停止，不自行选取其他状态版本。

| 输入文件 | SHA-256 |
|---|---|
| `AGENTS.md` | `2b4636d39e10bcc642f554ea9fa08a0ee49c19467f776a4dfb5b636b4c37c6d4` |
| `PROJECT.md` | `6b5b98b83ce842d4d55cdc6015373d923484cbac788c4e6cebe6eefee1495aeb` |
| `STATE.md` | `bd1ea524cc7ddc8833a35830d6cde5782a7711333582038c8ca646a5bd8f6461` |
| `HARNESS.md` | `69c5dfc063cfedfec069b929d9c8c739199a188fc8d6c21e01883d3c853af635` |
| `CAPABILITIES.md` | `45c54e88bdf2d7663e7b260815a8a7c62808d8dd689b10123484718a297405d8` |
| `config/runtime.json` | `41f2e679a13713dea9eded9eada119c0b11c0e62ee8beaeecf719bc8cf29923e` |
| `config/providers.json` | `cb92c6fb330d352d1d3b79e40662856dcbdf1e3c10be3f8edf730533b0f7abae` |
| `tools/README.md` | `f12289601e7086920872fb966bcb69cd1ad0a5e84b8f0076118f49bac290d710` |
| `07_reviews/README.md` | `699f780ee380b0ecf786e93da9f9ccfe6e356674cc84f473652fe6e511fd9e85` |
| `tools/studio.py` | `d5d9e031cd23c1988dcdf8fa2833154f4f06cd290a15a97922eda18dd60e16ee` |
| `tools/harness_core.py` | `74fb425d6b6b35a23467e996ad9f9a0f85f7a0533915b6c1a32d176b51022920` |
| `tools/render_preview.py` | `a732db794b000b3f18bbd274009f6536213b0deda949b1f337e33936713063f2` |
| `tools/check_shots.py` | `0f529497fb3e7db3869897d9c415c73bd73281683eeacff5947fc861e6c2f057` |
| `.agents/skills/manju-producer/SKILL.md` | `79d0609e0d1673980f5b9096351d6c4f9d49308005b57aefb164367b0492396f` |

## 7. doctor 原始结果

```json
{
  "python": "3.14.5",
  "python_minimum": "3.9",
  "platform": "macOS-26.6.2-x86_64-i386-64bit-Mach-O",
  "skill_count": 14,
  "skills": [
    "manju-audit",
    "manju-delivery",
    "manju-edit",
    "manju-images",
    "manju-producer",
    "manju-prompts",
    "manju-script",
    "manju-shots",
    "manju-sound",
    "manju-story",
    "manju-subtitles",
    "manju-video",
    "manju-visual",
    "manju-voice"
  ],
  "required_project_files": {
    "AGENTS.md": true,
    "STATE.md": true,
    "PROJECT.md": true,
    "CAPABILITIES.md": true,
    "config/runtime.json": true,
    "config/providers.json": true
  },
  "binaries": {
    "ffmpeg": "/usr/local/bin/ffmpeg",
    "ffprobe": "/usr/local/bin/ffprobe"
  },
  "versions": {
    "ffmpeg": "ffmpeg version 8.1.1 Copyright (c) 2000-2026 the FFmpeg developers",
    "ffprobe": "ffprobe version 8.1.1 Copyright (c) 2007-2026 the FFmpeg developers"
  },
  "local_preview_dependencies_ready": true,
  "local_preview_blocker": "",
  "cloud_adapters_implemented": false,
  "network_calls_made": false,
  "installed_anything": false,
  "note": "这不是你的生产权限批准，也没有验证 Codex 已加载 skill。"
}
```

## 8. 阻塞与唯一下一步

初始化检查无阻塞。后续外部生成与原生剪辑软件能力的阻塞为相应适配器 `unconfigured`，并且没有本轮费用/上传/制作批准。项目方向、题材与受众、首条时长尚待用户输入；`PROJECT.md` 中默认值仍是未确认模板。以上不影响本次初始化检查完成。

唯一下一步：用户若决定进入制作，先确认项目入口（原创/改编）、题材与受众、首条时长。本轮到此停止，不自动创作或进入 G1。
