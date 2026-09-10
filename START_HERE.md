# 从这里开始｜AI 漫剧 Harness v2

这是 v1 的扩展版：保留六个前期技能，新增八个制作/后期/统筹技能，共十四个。
默认只规划，不接云端、不配音、不生图、不渲染。你可以现在写小说，以后再接配音和视频服务。

## 1. 放到 Mac 桌面并启动
解压后保留完整 `ai-manju-studio-v2` 文件夹，包括隐藏 `.agents`。
```bash
cd ~/Desktop/ai-manju-studio-v2
codex
```
不要在已有小说项目上直接覆盖解压，升级旧项目先读 MIGRATION.md。

## 2. 第一条消息：只初始化
下面内容在 Codex 交互输入框粘贴，不是在普通 shell 执行：
```text
$manju-producer
读取 AGENTS.md、PROJECT.md、STATE.md、HARNESS.md、CAPABILITIES.md 和 config/runtime.json。
检查 .agents/skills 中的十四个技能是否存在，检查本机 Python/FFmpeg/ffprobe 的可用性。
只做初始化，不写故事、不生成图片/音频/视频、不安装依赖、不改全局配置、不调用付费接口。
没有配置的配音、视频、对齐、剪辑软件接口都明确标 unconfigured，不写成已接通。
不要把 examples 的故事和测试素材当成我的正式项目。
输出 07_reviews/setup_check_v01.md，同名则递增版本；列出真正能执行的能力和待配置项。
我稍后再提供小说与配音/剪辑服务选择。
```
`/skills` 可用于检查发现到的技能；没有出现时重启 Codex。仍未识别则明确让它读取 `.agents/skills/manju-producer/SKILL.md` 执行本轮检查，不盲目改全局配置。

## 3. 日后要做配音时
```text
$manju-voice
按已确认剧本给角色做声音定妆卡和逐句任务单。
先安排两个角色各一小组试音，不批量生成。
区分可朗读台词、表演指导与字幕文本。
先确认所用服务、音色许可、要上传的内容、费用上限和输出路径。
接口未配置就只交任务单和接入清单，不假装生成音频。
```

## 4. 日后要让 AI 剪视频时
```text
$manju-edit
读取当前采用镜头表、真实音视频文件、实测配音和素材哈希。
先检查缺失/失效素材，建立中立 timeline.json，做本地低分辨率粗剪计划。
不修改原件，不覆盖已有导出；不支持的效果明确列出，不静默忽略。
先 dry-run，列出输出位置和命令，等我确认后再 --execute。
不要把中立 timeline.json 说成剪映/Final Cut/Resolve 原生工程。
```

## 5. 你现在不需要装齐全部工具
文字阶段不要求 FFmpeg。真正剪辑时才需要已安装的 FFmpeg/ffprobe；本包不会自动安装。
配音与视频的 API 集成尚未实现；先手动生成后导入也能接入时间线。真实工具边界见 CAPABILITIES.md。
