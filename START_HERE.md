# 从这里开始｜AI 漫剧 Harness v2.1

本版保留十四个技能与后期预留，增加两个固定入口：A 有小说直接按原文制作，B 无小说直接从剧本开始。不要把两条路串成一条，也不必先写小说。

## 1. 新项目启动
解压完整 ai-manju-studio-v2.1 文件夹，保留隐藏 .agents。在终端进入实际目录：
```bash
cd ~/Desktop/ai-manju-studio-v2.1
codex
```
已有项目不要覆盖解压，先读 MIGRATION.md；也可使用独立的 v2.1-update 更新包并按其合并说明操作。

## 2. 只初始化
在 Codex 输入，不是在普通 shell 执行：
```text
$manju-producer
读取 AGENTS.md、WORKFLOW_ENTRYPOINTS.md、PROJECT.md、STATE.md、CAPABILITIES.md 和 config/runtime.json。
本轮只检查十四个技能、两个入口提示词和本地工具是否存在，不选择故事、不写稿、不安装依赖、不调用付费接口、不生成或渲染媒体。
核对 novel_direct 跳过独立编剧、original_script 不要求小说；两条路共用配音与剪辑。
不把 examples 当正式资料，不用“未提供小说”阻塞原创入口。
输出初始化报告，重名递增，不覆盖。
```
若技能名称没有被识别，可要求读取 `.agents/skills/manju-producer/SKILL.md`；不要盲目改全局配置。

## 3. 有小说，不想再打磨剧本
```text
$manju-producer
读取并执行 prompts/entry_novel_direct.md。
小说路径：00_source/我的小说.txt
本次范围：第一章的指定片段（这里填写实际起止）。
目标：先试做60秒，原文装不下时先提出拆集或延长。
不另写剧本、不润色对白，先做原文制作依据、逐句台词与文字分镜试拆。
```
完整可填写提示词在该文件中。EPUB 没有现成专用导入器；先检查可读性和实际工具，未读成功就停止原文分析，不凭记忆补全。范围尚未选时只选片段，不拆全书。

## 4. 没有小说，用你的设定写剧本
```text
$manju-producer
读取并执行 prompts/entry_original_script.md。
世界设定：……
人物描述：……
故事概述：……
必须保留：……
希望先做一集60秒试写。
不要先写小说，不生图或配音，完成剧本与检查后等我确认。
```
零散输入可以直接在消息里补充，无需编辑系统技能。缺核心方向才问，一次不超过三个问题。

## 5. 两路共用的配音与剪辑
内容确认后，告诉 voice 读取实际采用的内容依据和台词表：A 的依据是 source_packet，B 是剧本。无需为了 A 的配音另造一份剧本。实际 TTS 接口仍待接入，可先手动生成再导入。

真实图像/音视频就绪后，再交 edit 建中立 timeline、检查与 dry-run；确认后才调用已有 FFmpeg 后端粗剪。没有媒体时不生成黑片冒充成片，不说已经控制剪映/Final Cut/Resolve。

入口和文本都只决定怎样工作，不新增外部调用、安装、渲染或发布授权。能力边界见 CAPABILITIES.md。
