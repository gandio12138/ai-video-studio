# 电影式视觉 harness 合并报告 v01

完成时间：2026-09-11T11:54:50.457398+08:00

已按用户“确认按此计划合并”完成本地语义合并。当前视觉目标为 `cinematic_live_action`，指接近真人电影拍摄的观感；本次完成的是工作规则，电影式作品提示词与样张尚未制作。批准记录见 [cinematic_look_merge_v01.md](../12_runs/approvals/cinematic_look_merge_v01.md)。

## 已落地的行为

| 调用入口 | 默认文字范围 | 交付要求 |
|---|---|---|
| entry_novel_direct | full_pack，选定原文范围 | 原文事实/source_packet/原句→主动补全→电影式详细卡、布局、分镜及每镜完整提示词；不另写独立剧本 |
| entry_original_script | full_pack，当前首集 | 沿用原创流程，补全服饰/人物/场景/道具/局部动作，并交每镜完整提示词 |
| complete_visual_pack | full_pack，STATE当前范围 | 补缺，保留采用内容；必要独立参考、关键道具、每镜正文、编辑预案与覆盖索引 |
| rebuild_cinematic_visuals | calibrate_only | 后续另行调用时才写人物、空景、已有动作/互动三类样张正文；明确整集时扩为full_pack |
| complete_design_sheets | 显式要求的板面范围 | 设定板是可选辅助；启用时仍交完整整板/独立分格/映射与检查 |

新规则已经接入AGENTS、双入口、视觉流程、producer/visual/enrich/prompts/shots及相关审校和媒体交接技能，模板与导航同步更新。它要求真人比例、可信衣料受力、具体表演、实体空间、机位/视线/焦点、光源方向与接触遮挡；不能只在旧二维、赛璐璐正文末尾添加“电影感”。

主动补细节、人物适配、A/B补充台账、原文忠实度、固定空间和逐镜完整正文继续保留。“不生图”仍只限制实际生成，不能省掉已请求的提示词。校准的三类正文不能冒充完整集交付；板面数量不能替代真实镜头风格校准。

PROJECT/STATE只更新当前视觉方向、历史稿修订索引与维护状态。人读look字段没有写入runtime/providers或严格JSON，也不代表新增模型参数、执行器或效果保证。

## 合并方式与保护证据

更新包基线比较：16项中1项相同、13项不同、2项在当前项目不存在，因此没有强制应用补丁。缺失名称`ASSET_SHEETS.md`与`prompts/asset_reference_sheets.md`分别落到本项目真实的`DESIGN_SHEETS.md`与`prompts/complete_design_sheets.md`，没有制造重复入口。

备份覆盖合并前345个项目文件（排除.git内部）；本轮修改其中35个，其余310个逐文件SHA-256一致，删除0个。最终新增24个文件，含16个payload文件、1个静态检查文件、1个维护批准记录、2份本机测试日志、doctor/检查/报告/lineage各1份。完整路径见附录，前后哈希见 [检查记录](../tests/reports/cinematic_look_merge_checks_v01.json) 与 [执行日志](../12_runs/lineage/cinematic_look_merge_v01.json)。

- 原EPUB保持SHA-256：`ef2ecadf421b65ecfbc4356e797fe94ee018d9304ff114d504b651900d347d45`。仅读取其字节做保留核验，没有重新解析全书或创作。
- 原故事、source_packet_v02、44条原句、62镜、395.5秒估算与9:16不变；后续是否拆集、实际配音校时仍按原记录。
- 人物、衣装、场景、道具、旧STYLE、全部旧提示词/板/素材登记、媒体、批准和历史日志保持原字节。C006纯旁白不增加视觉任务。
- `config/`、`tools/`、`contracts/`及配音/剪辑相关文件保持原字节。TTS、视频、自动对齐、口型、NLE、拼版与实际生图接口仍为 `unconfigured`。
- G1/G2仍待确认；维护批准没有变成作品采用或媒体授权。PROJECT/STATE是可变索引，历史日志中的旧哈希仍对应旧快照，没有反写历史。
- Git HEAD与index SHA保持一致，未提交、暂存或推送；此检查不访问远端。

备份：`/Users/chengchengxu/Desktop/ai-video-studio/.git/upgrade-backups/cinematic-20260911T114020`；归档`baseline.tar`的SHA-256：`3d479dd0830722e99438edda68fa737c4ab916de61b7ddc4b35b0f6fda293b82`。备份不在Git内容中，含合并前真实项目状态。

## 参考资料的来源边界

16个payload文件中14个逐字节复制；仅`CINEMATIC_LOOK.md`和`examples/cinematic_look/reference_notes.md`做了当前路径/范围与来源说明的语义适配。8张PNG裁片及1张预览JPG均为更新包原文件复制，没有生成、裁切、增强或拼版。

8张PNG均按清单核验SHA-256与448×252尺寸。原始视频未随包提供，原片时长、录屏外框尺寸和抽帧过程仅为上游记录，本机没有复核原视频，也未听音频。参考只用来理解摄影、灯光、材质与写法；examples中的人名、现代衣装和情节没有进入正式作品。参考中的横向内容不改变本项目9:16。

## 实际检查与局限

| 检查 | 本机结果 | 边界 |
|---|---|---|
| `python3 -B -m unittest discover -s tests -v` | 77项通过，0失败 | 数据/文档/引用/参考字节检查；无生成、渲染或真实审美验收 |
| 初次本机测试日志v01 | 76通过、1失败，原日志保留 | 新检查误按代码块提取示例；改为真实段落标题解析，示例文件未改，复验结果存v02 |
| doctor | Python 3.14.5、FFmpeg/ffprobe 8.1.1可用，15技能文件存在 | 工具可用不等于已渲染或接口已配置 |
| 技能前言标准库检查 | 15/15通过 | 只校验本项目实际的name和单行引号description、名称/目录与正文结构，不冒充通用YAML解析或技能已加载 |
| skill-creator通用quick_validate | 未能运行：缺少PyYAML，`ModuleNotFoundError: No module named 'yaml'` | 未安装依赖；用上述有限结构检查补充 |
| 保留、引用与输入校验 | 310个原文件哈希一致，0删除；新引用存在，三入口完整包声明/条件板面一致；9个图片复制与源一致 | 不证明实际模型会遵循规则或成图达到参考水平 |

通过日志：[unit_test_results_cinematic_local_v02.txt](../tests/unit_test_results_cinematic_local_v02.txt)；初次日志：[v01](../tests/unit_test_results_cinematic_local_v01.txt)；[doctor](../tests/reports/doctor_cinematic_local_v01.json)。

## 当前状态与后续范围

本轮外部生成调用0，已知外部费用CNY 0；没有安装、联网、实际生图、裁图、拼版、配音、视频或渲染。9个新图片路径全部是参考输入复制。

`look_status=draft`；电影式提示词`not_started`、实际样张`not_generated`、验收`not_reviewed`。旧`EP01_character_tryout_v01.md`和人物v03仍含插画表达，应作为历史稿；不能用它们试图后认定新电影式规则已生效。旧稿完整保留，相关依赖在STATE标为`needs_visual_revision`。

后续若请求校准，只另写本次选定的人物/空景/已有镜头新版本，复用身份、衣装、布局与动作事实；不因规则升级自动重做110条板面/单图正文或62镜。当前没有已生成的正式媒体，不伪造下游素材失效、重配音或风格批准。

本地`CHATGPT_PROJECT_INSTRUCTIONS.md`已更新；未操作ChatGPT账号或远端项目设置，如在那里使用需自行粘贴本地新版。

本次维护到此结束。唯一下一步：查看本报告；另轮明确执行`prompts/rebuild_cinematic_visuals.md`后才开始电影式校准文字。

## 受影响的历史视觉版本（本轮全部只读）

下列清单用于后续按请求范围定位修订，并非本轮重做列表。更早版本同样完整保留，不能重新成为默认插画目标。当前包共80个提示词文件可能受媒介表达/依赖变化影响，其中62个为逐镜文件；布局文字另列复用。文件与任务数量不同，不将80解释为80条正文。

### 风格总纲：另轮按需写新视觉表达

- `04_visual/STYLE_v01.md`
- `04_visual/STYLE_v02.md`
- `04_visual/EP01_visual_bible_v03.md`

### 人物/衣装/场景/道具：保留身份与几何，仅核对媒介表达

- `04_visual/characters/C001_v03.md`
- `04_visual/characters/C002_v03.md`
- `04_visual/characters/C003_v03.md`
- `04_visual/characters/C004_v03.md`
- `04_visual/characters/C005_v03.md`
- `04_visual/characters/C005_G1_v01.md`
- `04_visual/characters/C005_G2_v01.md`
- `04_visual/characters/C005_G3_v01.md`
- `04_visual/locations/L001_v03.md`
- `04_visual/props/P001_v02.md`

### 当前提示词文件：后续仅重建请求范围，设定板不自动重做

- `05_prompts/shots/EP01_SH001_v02.md` 至 `EP01_SH062_v02.md`，共62个文件；逐个路径与哈希在检查JSON中。
- `05_prompts/characters/C001_v03.md`
- `05_prompts/characters/C002_v03.md`
- `05_prompts/characters/C003_v03.md`
- `05_prompts/characters/C004_v03.md`
- `05_prompts/characters/C005_G1_v03.md`
- `05_prompts/characters/C005_G2_v03.md`
- `05_prompts/characters/C005_G3_v03.md`
- `05_prompts/edits/EP01_sheet_edit_recipes_v01.md`
- `05_prompts/locations/L001_v03.md`
- `05_prompts/props/P001_v02.md`
- `05_prompts/sheets/characters/C001_sheet_v01.md`
- `05_prompts/sheets/characters/C002_sheet_v01.md`
- `05_prompts/sheets/characters/C003_sheet_v01.md`
- `05_prompts/sheets/characters/C004_sheet_v01.md`
- `05_prompts/sheets/characters/C005_G1_sheet_v01.md`
- `05_prompts/sheets/characters/C005_G2_sheet_v01.md`
- `05_prompts/sheets/characters/C005_G3_sheet_v01.md`
- `05_prompts/sheets/locations/L001_sheet_v01.md`

### 旧试图与索引：历史文件，不是电影式提示词入口

- `05_prompts/EP01_character_tryout_v01.md`
- `05_prompts/EP01_visual_pack_index_v02.md`
- `05_prompts/EP01_visual_pack_index_v02.json`
- `03_shots/EP01_sheet_reference_coverage_v01.md`

### 可选板与映射：保留，显式请求才扩展

- `04_visual/sheets/C001_manifest_v01.md`
- `04_visual/sheets/C001_sheet_v01.md`
- `04_visual/sheets/C002_manifest_v01.md`
- `04_visual/sheets/C002_sheet_v01.md`
- `04_visual/sheets/C003_manifest_v01.md`
- `04_visual/sheets/C003_sheet_v01.md`
- `04_visual/sheets/C004_manifest_v01.md`
- `04_visual/sheets/C004_sheet_v01.md`
- `04_visual/sheets/C005_G1_manifest_v01.md`
- `04_visual/sheets/C005_G1_sheet_v01.md`
- `04_visual/sheets/C005_G2_manifest_v01.md`
- `04_visual/sheets/C005_G2_sheet_v01.md`
- `04_visual/sheets/C005_G3_manifest_v01.md`
- `04_visual/sheets/C005_G3_sheet_v01.md`
- `04_visual/sheets/L001_manifest_v01.md`
- `04_visual/sheets/L001_sheet_v01.md`

### 固定布局：复用，不移动原地标

- `04_visual/locations/L001_layout_v01.md`

### 纯旁白：不做视觉重建

- `04_visual/characters/C006_v02.md`

## 附录：本轮修改的35个已有文件

- `.agents/skills/manju-audit/SKILL.md`
- `.agents/skills/manju-enrich/SKILL.md`
- `.agents/skills/manju-images/SKILL.md`
- `.agents/skills/manju-producer/SKILL.md`
- `.agents/skills/manju-prompts/SKILL.md`
- `.agents/skills/manju-script/SKILL.md`
- `.agents/skills/manju-shots/SKILL.md`
- `.agents/skills/manju-video/SKILL.md`
- `.agents/skills/manju-visual/SKILL.md`
- `AGENTS.md`
- `CAPABILITIES.md`
- `CHATGPT_PROJECT_INSTRUCTIONS.md`
- `DESIGN_SHEETS.md`
- `HARNESS.md`
- `MIGRATION.md`
- `PROJECT.md`
- `README.md`
- `START_HERE.md`
- `STATE.md`
- `VISUAL_PRODUCTION.md`
- `WORKFLOW_ENTRYPOINTS.md`
- `prompts/complete_design_sheets.md`
- `prompts/complete_visual_pack.md`
- `prompts/entry_novel_direct.md`
- `prompts/entry_original_script.md`
- `templates/character_design.md`
- `templates/character_sheet.md`
- `templates/location_sheet.md`
- `templates/prompt_job.md`
- `templates/scene_design.md`
- `templates/sheet_manifest.md`
- `templates/shot_fields.md`
- `templates/visual_bible.md`
- `templates/visual_pack_index.md`
- `tests/test_design_sheets_v23.py`

## 附录：本轮新增的24个文件

- `07_reviews/cinematic_look_merge_v01.md`
- `12_runs/approvals/cinematic_look_merge_v01.md`
- `12_runs/lineage/cinematic_look_merge_v01.json`
- `CINEMATIC_LOOK.md`
- `examples/cinematic_look/detailed_prompts.md`
- `examples/cinematic_look/reference_crops/ref_003s.png`
- `examples/cinematic_look/reference_crops/ref_007s.png`
- `examples/cinematic_look/reference_crops/ref_037s.png`
- `examples/cinematic_look/reference_crops/ref_053s.png`
- `examples/cinematic_look/reference_crops/ref_082s.png`
- `examples/cinematic_look/reference_crops/ref_103s.png`
- `examples/cinematic_look/reference_crops/ref_118s.png`
- `examples/cinematic_look/reference_crops/ref_142s.png`
- `examples/cinematic_look/reference_look_contact.jpg`
- `examples/cinematic_look/reference_manifest.json`
- `examples/cinematic_look/reference_notes.md`
- `examples/cinematic_look/review_checklist.md`
- `prompts/rebuild_cinematic_visuals.md`
- `templates/cinematic_image_prompt.md`
- `tests/reports/cinematic_look_merge_checks_v01.json`
- `tests/reports/doctor_cinematic_local_v01.json`
- `tests/test_cinematic_look.py`
- `tests/unit_test_results_cinematic_local_v01.txt`
- `tests/unit_test_results_cinematic_local_v02.txt`
