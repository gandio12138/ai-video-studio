# 固定入口提示词｜v2.3

- entry_novel_direct.md：有小说，保留核心剧情与原句，补充制作细节，交人物/场景/逐镜提示词。
- entry_original_script.md：无小说，从用户创意写首集剧本，同批交补全、分镜与完整视觉提示词。
- complete_visual_pack.md：已有内容不从头重写，补齐遗漏的视觉与衔接工作。

共同必读：根目录PROMPT_AUTHORING_STANDARD.md、CINEMATIC_LOOK.md与VISUAL_PRODUCTION.md。全部生图提示词入口遵守同一结构/材料/空间/逐格/验收精度，新角色、新场景和后续集数同样适用。缺细节要主动写具体候选；短任务不缩成摘要，也不扩大任务范围。
“不生图”只限制真正调用生图模型，不限制写提示词。全部文字草案不自动构成G1/G2或付费授权。

complete_design_sheets.md：仅用户明确要求母图/设定板时补整板、单格正文与映射；两个完整入口和complete_visual_pack保留可选分支，电影式单幅默认不交板。
rebuild_cinematic_visuals.md：已有内容的电影式校准，默认三类样张文字；“完整提示词”不自动变为整集full_pack。
expand_character_masters.md：已有图片保留身份/造型的通用扩展；C001预填任务仅明确选用时适用。允许采用正面图直接整板候选，也保留独立图审核后拼版。
场景扩展无独立入口文件，由manju-visual/manju-prompts按共享规范第7节固定空间、换机位；道具/单镜/编辑分别按第7.3/8/9节。不为使用长期标准新建同义技能或强行重跑整集。
