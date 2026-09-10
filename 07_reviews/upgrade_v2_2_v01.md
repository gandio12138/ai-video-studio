# Harness v2.2 升级检查报告 v01

检查时间：2026-09-10T15:51:02+08:00。任务状态：规则、技能、模板与索引合并完成；plan；本轮外部媒体调用费用 CNY 0。

## 升级来源与备份

- 用户指定下载目录的 `ai-manju-studio-v2.2.zip` 更新当前项目；本次使用完整包做差异合并。原先的 GitHub harness 提交授权沿用，作品原文及衍生草稿继续保留本地。
- 实际读取：`/Users/chengchengxu/Downloads/ai-manju-studio-v2.2.zip`，196240 字节，SHA-256 `0e8cc47d208453c7ac0424384fa20a805321ed6fe39ed89d2944ac36eb9a9553`。
- 压缩包 128 个文件、8 个显式目录；清单覆盖其中 127 个文件（不含清单本身），全部 SHA-256 与 ZIP 解压读取校验通过。未发现路径越界、重复路径、符号链接或加密条目。
- 升级前基线：`c2e0754630de4f1ab8efc3f9bc1cfd533cb23172`。备份 `.git/upgrade-backups/v2.2-20260910T154729/baseline.tar` 覆盖升级前 139 个本地文件，含尚未提交的文件；每个归档成员已回读核验。
- 备份 SHA-256：`7fc957c5105160f3b0314626ecad42c87e3133f6bf85794b5d2897bbdee02cbe`；逐文件哈希、原 Git 状态与合并记录保存在同一备份目录的 `baseline.json`、`merge_plan_and_result.json`。备份位于 `.git`，不随 harness 推送。

## 合并结果

- 31 个已有包文件更新、15 个包文件新增；PROJECT.md / STATE.md 两份索引按已有状态合并，另新增本报告。没有删除文件。
- 原 14 个技能保留，新增 `manju-enrich`；加入 `VISUAL_PRODUCTION.md`、`prompts/complete_visual_pack.md`、人物/场景设计、CMP 补全、接续与覆盖索引模板。
- 两个完整入口、路由、producer/story/script/audit/shots/visual/prompts、交接协议同步至 v2.2。新规范提供完整多视角和逐镜提示词的文字工作流程；本次没有执行这些创作步骤。
- 8 个空目录已在本地建立。Git 不单独保存空目录；未来写入真实卡片/提示词时随文件进入版本管理，未为此添加占位作品。
- 106 个升级前文件保持逐字节一致，包括原稿、已有台词/分镜/提示词、素材登记表、批准与任务日志、历史检查报告、tools、tests 的 Python 文件、config 和 .gitignore。另 33 个已有文件的变化全部属于已列出的规则更新或两份索引合并。

## 冲突与状态处理

- 包内 PROJECT.md / STATE.md 是初始化模板，不能覆盖本地已有入口、范围、时长建议、画幅、采用索引和用户限制；仅合并版本及缺少的文字视觉设置/阶段。
- 包内 `04_visual/assets.json` 是空模板，保留本地真实登记表。现有设计与提示词继续保持原草稿状态，没有自动批准、重写、改词或新增剧情。
- 本地 completion_policy 保留用户更严格的原文约束，完整视觉包记录为 `not_started_by_scope`。升级不是重新调用创作入口，也不把旧版交付宣称为已符合 v2.2 全量要求。
- 新 package manifest 保留上游原文，表示发行包哈希。当前 124/127 个清单文件与包一致；PROJECT.md、STATE.md、04_visual/assets.json 三项差异均是刻意保留/合并，不伪造整项目与模板完全相同。
- 历史任务日志原样保留；其 PROJECT/STATE 哈希对应此前批次结束时的可变索引快照，本次索引变化由升级基线单独记录。作品正文和媒体依赖未变，不据此全量标记失效。
- 旧 v2.1 历史记录与 `docs/archive` 保留；活动入口的旧规则已更新。examples 仅作为教学/测试包文件更新，未用作正式作品。
- Git 提交中的 PROJECT/STATE 使用已提交的通用模板合并 v2.2 新字段，工作区继续保留个性化作品索引；作品正文、原稿、资产登记改动和本地批准日志不进入本次提交。

## 本机离线验证

| 检查 | 结果 |
|---|---|
| Python / FFmpeg / ffprobe | Python 3.14.5；FFmpeg 8.1.1；ffprobe 8.1.1 可用 |
| doctor | 15 个技能、所需项目文件、本地预览依赖就绪；未安装任何软件 |
| 单元测试 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`：56/56 通过 |
| 新流程结构 | 三入口、共同规范、新模板和8个目录存在；项目JSON均可解析 |
| 已有作品兼容 | 原分镜调用check_shots通过格式/数值检查；不代表语义、视觉或用户批准 |
| 文件保护 | 升级前后哈希比对通过；没有删除或覆盖作品版本 |
| 配置与实现 | runtime/providers/delivery和tools字节未变，严格JSON契约版本未改 |

本机执行输出位于 `.git/upgrade-backups/v2.2-20260910T154729/unit_tests_local.txt`、`doctor_local.json`、`local_structure_check.json`。包内 `tests/unit_test_results.txt` 和 `tests/reports/v22_structure_check.json` 是随包的上游历史证据，不冒充本次执行结果。
本轮未执行 smoke_test 或任何渲染。离线测试不验证真实图像/音频质量、云端账号或媒体服务可用性。

## 已实现与尚未接入

| 能力 | 状态与边界 |
|---|---|
| 双入口、补全、详细视觉与提示词 | 指令/模板已提供；不是自动程序或模型接口 |
| doctor、probe、timeline/job/alignment结构与哈希校验 | 本地已实现 |
| verified alignment JSON转SRT | 本地已实现；不做自动对齐，拒绝estimated |
| FFmpeg基础粗剪 | 已实现，依赖本机工具；单次180秒/60画面等限制保留，本轮未渲染 |
| 实际生图/编辑 | unconfigured |
| 配音：MiniMax / OpenAI TTS | unconfigured |
| 视频生成 / 口型同步 | unconfigured |
| 自动对齐 / ASR | unconfigured |
| 音乐音效生成 | unconfigured |
| 剪映 / Final Cut / Resolve接口与原生工程导出 | unconfigured |
| EPUB专用导入器 / 自动发布与后台调度 | 未实现；本次未添加 |

运行配置保持 plan、external_generation_allowed=false、预算 CNY 0、cloud_auto_retry=false。未安装依赖、修改全局配置、调用付费API或生成媒体。

唯一下一步：继续审阅项目 STATE.md 中已有草稿；后续需要补齐视觉时再按明确范围使用 `prompts/complete_visual_pack.md`。

## 实际修改与新增文件

实际读取了项目入口/状态/配置/能力、相关技能、包内迁移/变更/视觉规范与受影响模板；原稿只做字节哈希与备份，没有重新提取或阅读后续正文。以下仅列本次写入的48个包内路径与新报告：

- `.agents/skills/manju-audit/SKILL.md`
- `.agents/skills/manju-enrich/SKILL.md`
- `.agents/skills/manju-producer/SKILL.md`
- `.agents/skills/manju-prompts/SKILL.md`
- `.agents/skills/manju-script/SKILL.md`
- `.agents/skills/manju-shots/SKILL.md`
- `.agents/skills/manju-story/SKILL.md`
- `.agents/skills/manju-visual/SKILL.md`
- `04_visual/README.md`
- `05_prompts/README.md`
- `07_reviews/upgrade_v2_2_v01.md`
- `AGENTS.md`
- `CAPABILITIES.md`
- `CHANGELOG.md`
- `CHATGPT_PROJECT_INSTRUCTIONS.md`
- `HARNESS.md`
- `MIGRATION.md`
- `PACKAGE_MANIFEST.json`
- `PROJECT.md`
- `PROMPT_LIBRARY.md`
- `README.md`
- `SOURCES.md`
- `START_HERE.md`
- `STATE.md`
- `VALIDATION.md`
- `VISUAL_PRODUCTION.md`
- `WORKFLOW_ENTRYPOINTS.md`
- `contracts/PRODUCTION.md`
- `docs/archive/PROMPT_LIBRARY_v21.md`
- `docs/archive/README_v21.md`
- `docs/archive/VALIDATION_v21.md`
- `examples/visual_completion/README.md`
- `examples/visual_completion/source.md`
- `examples/visual_completion/worked_example.md`
- `prompts/README.md`
- `prompts/complete_visual_pack.md`
- `prompts/entry_novel_direct.md`
- `prompts/entry_original_script.md`
- `templates/character_design.md`
- `templates/completion_ledger.md`
- `templates/continuity_sheet.md`
- `templates/prompt_job.md`
- `templates/scene_design.md`
- `templates/shot_fields.md`
- `templates/source_packet.md`
- `templates/visual_bible.md`
- `templates/visual_pack_index.md`
- `tests/reports/v22_structure_check.json`
- `tests/unit_test_results.txt`
