# AI 漫剧工作室 Harness v2.1

支持“有小说原文直制”与“无小说原创剧本”的 **Codex 驱动项目骨架**：技能说明、项目状态、媒体任务协议、逐句声音与分镜交接、可重建时间线，以及一个可运行的本地基础粗剪后端。
这不是官方漫剧产品，不是已经接通全部服务的自动出片系统，也不保证商业回报。

**先读 START_HERE.md。只需把整个文件夹解压到桌面，在目录里启动 Codex。**
先选一个入口：`prompts/entry_novel_direct.md` 或 `prompts/entry_original_script.md`。前者跳过独立剧本打磨，后者不要求小说。配音/视频厂商无需现在确定。

## 能力清单
| 阶段 | Skill | 主要产物 |
|---|---|---|
| 统筹 | manju-producer | 当前阶段、关卡、预算、阻塞、恢复/变更影响 |
| 故事 | manju-story | A 原文事实提取 / B 创意简报、大纲、人物目标 |
| 剧本 | manju-script | B 原创场景剧本、对白打磨；A 默认跳过 |
| 审校 | manju-audit | 剧情、动机、信息与连续性检查 |
| 分镜 | manju-shots | 景别、机位、动作、台词、时长、素材 |
| 视觉 | manju-visual | 角色/服装/场景定妆 |
| 提示词 | manju-prompts | 生图、多参考、局部修改任务说明 |
| 图像制作 | manju-images | 关键帧任务、实际图像导入与验收 |
| 配音 | manju-voice | 声音定妆、逐句 TTS、take 与真实时长 |
| 视频 | manju-video | 逐镜视频任务、候选 take、可用区间 |
| 字幕 | manju-subtitles | 实际对齐、字幕断句与 SRT |
| 声音后期 | manju-sound | 音乐/音效 cue、分轨、混音与检查 |
| 剪辑 | manju-edit | 时间线、dry-run、本地粗剪 |
| 交付 | manju-delivery | 技术/视听/授权检查、交付清单 |

## 最重要的区分
Skill 教 AI 怎么工作，adapter 才真正连接生成/剪辑工具。本包八个新 skill 都已写入；云端图像、TTS、视频、自动对齐、口型同步、音乐生成接口仍未接入。
本地真实实现：环境检查、文件/哈希/时间线检查、音视频探测、已验证对齐转 SRT、FFmpeg 基础粗剪。
本地后端不是智能审美模型，不会仅凭一条小说自动作出满意的电影级剪辑；它执行经你/AI 形成的明确时间线。
完整状态与限制见 CAPABILITIES.md。没有程序级后台调度/自动云端恢复引擎，恢复与缓存由 agent 按协议执行/未来适配器实现。

## 目录
```text
.agents/skills/     十四个项目级 skill
AGENTS.md          每轮规则、版本、权限、真实性
PROJECT.md         创作与制作约束
STATE.md           人读阶段与采用版本
HARNESS.md         全流程、反馈环与确认关卡
WORKFLOW_ENTRYPOINTS.md  双入口路由、G1 内容依据与共用台词接口
prompts/           两个固定入口提示词
CAPABILITIES.md    已实现/预留/不支持
config/            模式、供应商预留、预览/交付规格
contracts/         数据字段、依赖和适配器协议
00_source/         原文与来源（只读）
01_story/          人物、大纲
02_scripts/        剧本、台词
03_shots/          文字镜头表
04_visual/         视觉设定与资产登记
05_prompts/        生图/修改提示词
06_assets/         实际图像、参考素材
07_reviews/        审校、初始化、交付检查
08_audio/          声音定妆、逐句 take、对齐、混音、许可
09_video/          视频任务与真实片段
10_edit/           中立时间线、代理
11_exports/        预览与最终交付
12_runs/           任务、批准、日志、依赖
examples/          教学故事与声音交接示例，不是用户正式项目
templates/         未完成草案，null 不是已测数值
tools/             Python 标准库工具、FFmpeg 粗剪后端
tests/             原镜头校验与 v2 工具单元测试
```

## 三种使用方式
**现在做文字：** A 原文直制用事实提取/分镜/保真检查，B 原创剧本用 story/script/audit；不必接任何音视频接口。
**半自动制作：** 在网页上生成图片/语音/视频，把真实文件导入，按协议登记、测时长、剪辑。不要把手动导入伪记为 API 调用。
**后续自动化：** 明确供应商后，按 contracts/PRODUCTION.md 加适配器，先单个任务测试，再处理批准范围内的批量。不要把聊天订阅、语音通话功能和可批量下载角色配音文件的外部接口混作一种工具。

## 配音先实测，再锁剪辑
文字分镜阶段只估时；先做音色试音，再逐句配音。真实时长返回后修订镜头节奏，优先低成本有声分镜，再批量做动态镜头。
口型同步单列为可选接口，不属于“有 TTS 就自然完成”的步骤。
一条台词改了，只重做该句以及真正受影响的对齐、镜头、混音和导出，不因为换一个字重做全剧所有图片。

## 本地工具起步
这些是终端命令。Python 需要3.9或更新，渲染需要本机已有 FFmpeg/ffprobe；不自动安装、不联网。
```bash
python3 tools/studio.py doctor --root .
python3 -m unittest discover -s tests -v
```
真实媒体就绪后：
```bash
python3 tools/studio.py validate timeline 10_edit/timelines/EP01_v01.json --root . --check-files
python3 tools/studio.py render 10_edit/timelines/EP01_v01.json --output 11_exports/previews/EP01_v01.mp4 --root .
```
第二条默认只做媒体预检/计划，不输出视频。用户确认后加 `--execute` 才真正渲染。输入文件需存在且哈希匹配；模板不能直接冒充就绪时间线。
完整命令、测试方式、限制见 tools/README.md。

## 版本与安全
默认运行模式 plan、外部生成未授权金额0、不自动重试、不自动发布。此配置是工作约定，不是系统权限边界或账户硬限额。账户预算/Codex权限审批须独立设置。
输出不覆盖旧版本，原始媒体不改写。未知远端状态先查询/核账，不盲目重发。仅有 `succeeded` 不代表用户批准。
旧项目升级见 MIGRATION.md。ChatGPT 端可以参考更新后的 CHATGPT_PROJECT_INSTRUCTIONS.md，但本包没有自动同步两边的文件，也不会让网页聊天凭空访问 Mac。

## 验证
v2.1 是入口提示词、路由、交接模板与文档更新，媒体后端未变。本轮重跑原有56项单元测试的结果与新文件结构检查见 VALIDATION.md；不把静态检查当作 Codex 已按路线成功执行。v2 的合成媒体测试保留为历史记录，本轮未重新渲染，也未在你的 Mac 或付费接口上测试。
资料来源与查阅日期见 SOURCES.md。前期 v1 说明只作为历史归档，不是本版当前规范。
