# 从这里开始｜双入口与电影式视觉

长期生图提示词共同必读PROMPT_AUTHORING_STANDARD.md，所有内容入口、直接技能调用和后续集数都适用。短请求默认交完整制作正文与可见验收；采用参考、当前身份/衣装/空间和任务范围优先，原样例只作写作参考。此规范已经合并时无需再次执行安装包。

## 已有项目只更新harness
读取用户本次指定的实际更新包说明，比较当前文件并先给计划，用户确认后语义合并。长期提示词规范的来源为prompt-authoring-standard/INSTALL_WITH_CODEX.md；历史电影式更新不自动重跑。保留原故事、素材、PROJECT/STATE真实进度、服务配置和批准；规则/模板/引用同步后做离线检查，报告并停止，不自动运行新入口。

## 新项目只初始化
保留.agents目录，进入实际项目目录。让manju-producer读取AGENTS、PROJECT、STATE、CINEMATIC_LOOK、WORKFLOW_ENTRYPOINTS、VISUAL_PRODUCTION、CAPABILITIES与runtime；检查十五个技能及两入口、complete_visual_pack、rebuild_cinematic_visuals、可选complete_design_sheets是否存在。不选择故事、不写稿、不安装、不调用接口、不生图或拼版。

## 两条内容入口
有小说：执行prompts/entry_novel_direct.md并提供实际原文和片段；没有小说：执行prompts/entry_original_script.md并提供设定/人物/概述。两者默认full_pack，按当前电影式目标主动补细节、固定人物/空间、交完整当前逐镜提示词，不在剧本/分镜之后提前停止。范围未选时先选片段，EPUB不可读不凭记忆补文。

## 已有内容纠正摄影观感
执行prompts/rebuild_cinematic_visuals.md，沿用STATE内容，默认calibrate_only，只写人物、空景和已有动作/互动三类完整样张提示词与对照标准。旧插画稿保留，新稿不能混用旧插画表达。实际试图另行授权，未见真实图不宣称达标；整集需求改full_pack并覆盖每镜。

## 完整补视觉与可选设定板
补当前全部视觉文字用prompts/complete_visual_pack.md（full_pack）。仅明确需要角色/场景板时才执行prompts/complete_design_sheets.md及DESIGN_SHEETS.md，交该范围整板/独立格/布局/映射。电影模式默认不要求板面数量，板不能替代剧情镜头风格校准。

## 示例与参考
examples/cinematic_look为视频裁片分析与教学写法，examples/design_sheets为可选板面教学；06_assets/references/layout中的原图仍只是版式参考。这些不自动成为正式角色、故事、衣装或可发布素材。LOOK与身份/衣装/空间/构图用途分开，已定9:16不因录屏画幅改变。
