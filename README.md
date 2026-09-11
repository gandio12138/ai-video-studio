# AI 漫剧 Harness v2.3｜双入口＋电影式视觉＋主动补全

长期生图提示词入口：先读PROMPT_AUTHORING_STANDARD.md，覆盖人物/全身/母图/场景/道具/关键帧/局部编辑和所有新资产、后续集数。原始写作样例保存在references/prompt_authoring，仅读组织与精度，不执行历史任务。短调用默认完整正文，单项请求不扩大范围。

保留十五个skills和原有声音、视频、字幕、剪辑交接。当前新增电影式视觉规范、单幅提示词模板和校准路由，保留可选设定板；**没有新增云端API、拼版程序或模型**。

有小说：实际原文→source_packet/台词，保留核心剧情和采用原句，不独立打磨剧本。
没有小说：设定/人物/概述→首集剧本，不先写小说。
两路都按CINEMATIC_LOOK.md主动补服饰、外观、空间、道具与局部接续，交详细视觉卡、固定布局、必要独立参考与当前每镜电影式关键帧提示词；设定板仅用户显式要求时启用。核心剧情变化仍需按原规则处理。

## 先看
- START_HERE.md：新项目、旧项目合并和本轮调用。
- CINEMATIC_LOOK.md：当前真人电影式目标、参考用途、校准与完整包范围。
- DESIGN_SHEETS.md：显式要求设定板时使用的辅助标准。
- VISUAL_PRODUCTION.md：补全、审美具体性与原有逐镜标准。
- WORKFLOW_ENTRYPOINTS.md：两种内容入口。
- MIGRATION.md：保留真实作品与批准记录的更新办法。

仅启用设定板时，角色板包含同衣装三视图、表情组、中性脸多角度、衣装/发饰/必要道具细节；特殊状态按故事需要。场景板包含主反视角、固定布局/机位、关键交互区、材质细节；日夜/事件状态按需要。不是四张互不相干的风景拼贴。

更新包附带版式参考已存06_assets/references/layout；默认只借鉴版式，不把参考角色的红黑衣装、脸或能力分发给所有角色。详细记录见04_visual/references/RF_LAYOUT_USER_01.md。

电影式校准用prompts/rebuild_cinematic_visuals.md，默认先写人物/衣装、空景、已有剧情动作或互动三类完整提示词；实际小样需另行授权与查看。完整入口仍full_pack逐镜覆盖，单项请求按明示范围。母图/设定板仅显式要求时启用，可采用正面图直接出整板候选，也可派生独立图、逐图验收后仅排版；不先索要全部侧背/胸像，保留真实源，板不直接当视频首帧。文字全覆盖不等于一次执行全部图像任务。

## 可选设定板目录
`04_visual/sheets/`板规格与源映射；`04_visual/locations/*_layout_*`场景布局；`05_prompts/sheets/`整板正文与单格索引；`06_assets/sheets/`未来真正输出的板。
原`05_prompts/characters/locations/shots`仍保留独立正文，避免只有一张总板却没有可制作素材。

## 边界与验证
实际生图、配音、视频及拼版接口均未因本次更新而接入；Python/FFmpeg既有工具能力见CAPABILITIES.md。缺接口不阻塞文字，实际图不存在就写null。
模板与检查不保证模型审美、一致性或版权适用；批准、文字审校、实际视听验收分别记录。新旧项目不要直接覆盖合并。验证范围见VALIDATION.md。

## 十五个技能
story、script、audit、shots、visual、prompts；新增enrich处理视觉与事件细节缺口；producer统筹；images、voice、video、subtitles、sound、edit、delivery接后续制作。实际名称均以manju-开头，目录位于`.agents/skills/`。

原来十四个技能保留，不需要再造一套配音和剪辑协议。新增技能不是新增模型或接口。

## 原有目录与制作交接
```text
.agents/skills/          十五个技能
prompts/                两入口 + 已有内容补视觉入口
VISUAL_PRODUCTION.md     共同视觉/补全标准
01_story/               事实/设定/CMP台账
02_scripts/             source_packet或原创剧本/台词
03_shots/               镜头与状态接续
04_visual/              STYLE与characters/locations/props详细卡
05_prompts/             characters/locations/props/shots/edits提示词与索引
06_assets/              真实图片/参考
08_audio/、09_video/     声音与动态片段
10_edit/、11_exports/    中立时间线与真实导出
12_runs/                任务、日志、采用与批准
```

## 内容、补全与批准
来源/用户设定与CMP台账、内容依据和原句台词、动作接续、分镜、STYLE及详细人物/场景/道具卡继续保留。普通A/B补充在授权草稿内主动设计，核心变化按入口分级；小说原文只读，已确认内容不覆盖，不把悬念补成答案。
两路G1前可按明示范围交文字草稿，不生图仍须写完整提示词。尚无参考路径null/awaiting_reference，文字完成不是用户批准或媒体完成。服务、上传、数量、预算和重试边界仍逐批授权；不自动发布。

参考片裁片和教学写法见examples/cinematic_look，仅作LOOK分析；不进入正式人物/剧情。原视频未随包提供，历史抽帧记录不冒充本机已复核。当前故事/旧视觉稿和批准保留，harness维护不会自动重建提示词或生成媒体。
