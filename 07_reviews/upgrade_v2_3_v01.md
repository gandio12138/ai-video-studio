# Harness v2.3合并检查报告 v01

状态：已完成本次授权的harness合并；仅规则、技能、模板、参考登记和离线验证。故事与设定板创作未开始，没有生成、编辑、裁图、拼版或渲染。
时间：2026-09-11T10:48:10.859937+08:00。用户确认：“确认按此计划合并”；范围见[harness_v2_3_merge_v01.md](../12_runs/approvals/harness_v2_3_merge_v01.md)。

## 读取与基线
读取当前AGENTS、PROJECT、STATE、WORKFLOW_ENTRYPOINTS、VISUAL_PRODUCTION、HARNESS、CAPABILITIES、runtime、相关技能与模板；更新包APPLY_WITH_CODEX、UPDATE_MANIFEST、DESIGN_SHEETS、MERGE_ONLY及拟合并文件已比较。原小说只做保留哈希核对，本轮没有重新分析正文。实际读取/比较的更新载荷及输出清单在12_runs/lineage/harness_v2_3_merge_v01.json。
清单32项merge匹配v2.2基线，19个新增目标起初不存在，PROJECT/STATE为实际定制内容；55项载荷哈希匹配。十五技能及v2.2前置齐全。
修改前备份247个已有文件：`.git/upgrade-backups/v2.3-20260911T104157/baseline.tar`；SHA-256 `7c94c0b0a701d42d6916d2f51dd7230727ba23171eed218a81de835b9ea85a33`。

## 合并后的实际行为约定
- 两条内容入口与complete_visual_pack、complete_design_sheets均接到DESIGN_SHEETS。完整文字批次必须交每资产整板正文、逐格独立正文、锚点、布局/机位、拼版映射、索引及检查；缺格或缺正文要明确未完成。
- 角色保留身份/全身主图并扩展同衣装三视图、主要/常驻角色五种适配表情、中性脸三角度、至少三类实用细节。小角色缩减须有理由，特殊状态按内容需要。
- 场景交主反视角、固定布局/机位、交互区、至少三类材质细节；状态变化有依据。反向机位不能以水平翻转或另造空间代替。
- concept_sheet整板探索与production_sheet独立图验收后拼版分开；纯拼版不重绘源图。每格可追溯，源图复用不虚报生成次数。
- 每镜关键帧仍独立单幅，多格板不得默认作为视频首帧。所有媒体权限与原声音/字幕/剪辑协议保持原边界。

## 语义修正与自定义保留
1. 直接更新入口最终清单、producer/prompts/visual/audit方法及VISUAL_PRODUCTION完成表，避免只在末尾增加文档引用。补上更新清单遗漏的templates/visual_bible.md。
2. PROJECT/STATE仅调整harness版本标题并追加缺少的设置/阶段/维护记录；此前正文、采用索引和批准记录经前缀比对完整保留。旧93条提示词、44条原句、62镜和395.5秒估算不改写，v2.3设定板阶段明确未开始。
3. 现有STYLE及其draft/G2状态原样保留；新参考或尚未G2不能触发自动换成半写实风格。
4. 版式PNG从更新包原样复制，900×900头部尺寸与哈希核对；来源写随更新包附带，layout_only，未把包内转述当本轮用户上传/批准。不写入正式C001资产，不报告新图像目检。
5. 三份包内历史测试报告留在更新目录；VALIDATION指向本机新报告。旧v2.2说明另存archive且与备份一致。
6. MIGRATION在维护检查后停止；补一人一景或执行complete_design_sheets属于以后另轮明确创作请求。

## 实际检查
| 检查 | 结果与证据 |
|---|---|
| 单元测试 | 70/70通过：原56项加新14项静态规则检查；`tests/unit_test_results_v23_local_v01.txt` |
| 本机doctor | Python 3.14.5，FFmpeg/ffprobe 8.1.1，15技能文件；`tests/reports/doctor_v23_local_v01.json` |
| 文件保留 | 35个已有文件在批准范围内修改，其他212个已有文件哈希完全不变，无删除；`tests/reports/v23_merge_checks_local_v01.json` |
| 配置/工具/契约/作品 | 既有config、tools、contracts、严格JSON模板、原文、台词、镜头、人物/场景/道具卡、STYLE、素材登记与旧批准/日志均保持原字节 |
| 四入口与下游 | 规范引用、整板/独立正文/布局/映射、停止条件检查通过；技能元数据、代码块闭合及JSON解析检查通过 |
| Git | HEAD和暂存区保持不变，git diff --check通过；没有提交或推送 |

skill-creator的quick_validate.py在当前Python下因缺少PyYAML未能运行，未安装依赖；另以标准库核对15个技能实际使用的简单name/description元数据。不能把替代检查说成原通用YAML校验器通过。
上述检查是静态文本、文件与离线工具验证，不是Codex实际创作端到端测试，也不是图像审美、逐格一致性或作品批准。示例只作教学/测试，没有成为正式内容。

## 实际修改的已有文件（35）
- `.agents/skills/manju-audit/SKILL.md`
- `.agents/skills/manju-images/SKILL.md`
- `.agents/skills/manju-producer/SKILL.md`
- `.agents/skills/manju-prompts/SKILL.md`
- `.agents/skills/manju-script/SKILL.md`
- `.agents/skills/manju-shots/SKILL.md`
- `.agents/skills/manju-video/SKILL.md`
- `.agents/skills/manju-visual/SKILL.md`
- `04_visual/README.md`
- `05_prompts/README.md`
- `AGENTS.md`
- `CAPABILITIES.md`
- `CHANGELOG.md`
- `CHATGPT_PROJECT_INSTRUCTIONS.md`
- `HARNESS.md`
- `MIGRATION.md`
- `PROJECT.md`
- `PROMPT_LIBRARY.md`
- `README.md`
- `SOURCES.md`
- `START_HERE.md`
- `STATE.md`
- `VALIDATION.md`
- `VISUAL_PRODUCTION.md`
- `WORKFLOW_ENTRYPOINTS.md`
- `prompts/README.md`
- `prompts/complete_visual_pack.md`
- `prompts/entry_novel_direct.md`
- `prompts/entry_original_script.md`
- `templates/character_design.md`
- `templates/prompt_job.md`
- `templates/scene_design.md`
- `templates/shot_fields.md`
- `templates/visual_bible.md`
- `templates/visual_pack_index.md`

## 新增文件（22）
- `04_visual/references/RF_LAYOUT_USER_01.md`
- `06_assets/references/layout/character_sheet_layout_user_01.png`
- `06_assets/sheets/README.md`
- `07_reviews/upgrade_v2_3_v01.md`
- `12_runs/approvals/harness_v2_3_merge_v01.md`
- `12_runs/lineage/harness_v2_3_merge_v01.json`
- `DESIGN_SHEETS.md`
- `docs/archive/MIGRATION_v22.md`
- `docs/archive/README_v22.md`
- `docs/archive/START_HERE_v22.md`
- `docs/archive/VALIDATION_v22.md`
- `examples/design_sheets/README.md`
- `examples/design_sheets/location_layout.md`
- `examples/design_sheets/worked_prompts.md`
- `prompts/complete_design_sheets.md`
- `templates/character_sheet.md`
- `templates/location_sheet.md`
- `templates/sheet_manifest.md`
- `tests/reports/doctor_v23_local_v01.json`
- `tests/reports/v23_merge_checks_local_v01.json`
- `tests/test_design_sheets_v23.py`
- `tests/unit_test_results_v23_local_v01.txt`

其中只有layout_only参考PNG是原文件复制；其余新增项为文字、模板、教学示例、测试或维护记录。没有新增正式角色/场景生成图。

## 未执行与下一步
外部调用0，已知费用CNY 0；不安装依赖、不改全局配置。生图、拼版、配音、视频、自动对齐及NLE服务仍unconfigured；FFmpeg基础预览依赖可用不代表本轮渲染授权。
本次harness合并已完成，无需继续修改或创作。唯一下一步：用户审阅本报告；之后若另行要求补设定板，再按STATE当前范围和新版本执行文字批次。
