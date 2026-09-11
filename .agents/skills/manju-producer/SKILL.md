---
name: manju-producer
description: "用于初始化、双入口创作、已有内容的电影式风格校准与完整视觉交付；统筹补全、独立参考、逐镜正文与后期，设定板仅显式启用，不擅自生成媒体。"
---
# 全流程统筹与恢复

## 当前视觉目标与范围
先读CINEMATIC_LOOK.md与PROJECT/STATE的当前视觉设置。cinematic_live_action使用真人电影式单幅目标；完整入口/complete_visual_pack按full_pack，已有内容的风格纠偏按rebuild_cinematic_visuals的calibrate_only，用户明示范围优先。设定板只在用户显式要求时读DESIGN_SHEETS.md并启用；它不替代实际剧情镜头校准。维护或初始化任务不进入创作/媒体执行。


先读AGENTS.md、PROJECT.md、STATE.md、CINEMATIC_LOOK.md、WORKFLOW_ENTRYPOINTS.md、VISUAL_PRODUCTION.md、CAPABILITIES.md、HARNESS.md和config/runtime.json；显式启用设定板时再读DESIGN_SHEETS.md；只取本轮相关资料，不读全书或未经指定的examples。

## 路由与文字批次
涉及生图提示词时先读取项目根PROMPT_AUTHORING_STANDARD.md，覆盖所有人物/场景/道具/集数。按本轮类型交任务单、完整正文和可见验收；短指令不缩成概要，单个资产不扩成全包。样例只用于写作方法，不继承其人物或历史修改任务。
- 已有图片扩展走prompts/expand_character_masters.md的通用分支，角色与参考来自本轮输入，不默认C001预填批次；场景扩展由visual/prompts按共享标准第7节完成。直接索要道具、单镜或局部编辑分别走第7.3/8/9节；无参考的初设照常写具体候选，不虚构附件。
- novel_direct：story原文事实→source_packet/台词→enrich细节/桥接→visual详细设计↔shots文字镜头→prompts完整正文→audit保真/连续性。跳过独立script润色，缺独立剧本不阻塞。
- original_script：story简报/人物/大纲→script首集试写/台词→enrich细节/桥接→audit剧情→visual详细设计↔shots试拆→prompts完整正文→audit视觉与接续。缺小说不阻塞，入口已授权draft试写/试拆。
- 已有内容调用complete_visual_pack时按当前范围full_pack补缺，保留已确认剧情/台词/素材，不机械重写全部。
- 用户纠正视频摄影观感时路由prompts/rebuild_cinematic_visuals.md，默认calibrate_only；明示整集则full_pack。用户索要版式/设定板时才路由prompts/complete_design_sheets.md；不把风格纠偏当作增加板格。
- 未选入口只问入口；小说范围未定先选片段；只初始化不创作。

完整v2.3入口首轮包含文字视觉提示词；不是在剧本/镜头表后停下另问“是否需要提示词”。用户只要求局部则按局部。普通A/B补充已获草稿批次许可；C核心提案依入口处理。缺实际参考/模型不阻塞文字，只标条件和未就绪执行。

## 操作
1. 初始化可运行 `python3 tools/studio.py doctor --root .`，缺工具报告，不自动安装；外部服务未接入如实记unconfigured。
2. 明确本批输入版本、范围、skill、真实文件交付清单、停止条件与媒体权限。plan下只文本/离线检查。
3. 按CINEMATIC_LOOK.md、VISUAL_PRODUCTION.md和本轮scope检查：full_pack含补全台账、详细卡/布局/灯位、接续表/镜头、必要独立参考、关键道具、每镜单幅正文、人物/场景编辑预案与索引/审查；calibrate_only检查人物/空景/已有动作或互动三类正文与校准验收。仅显式启用设定板时另查DESIGN_SHEETS.md的整板/分格/manifest。缺本轮必需条目列ID，三类样张不能宣布整集完成。
4. 记录draft、prompt_only、awaiting_reference和真实资产状态，分开内容/视觉方案批准与媒体执行批准。没实际看到/听到的媒体不宣称验收。
5. G1内容/台词/叙事补充；G2视觉/衣装/场景/声音身份；先少量试音和定妆小样，再实测配音/关键帧/有声小样，按G3预算进入动态镜头，G4剪辑，G5交付。不得默认全季批量。
6. 按contracts/PRODUCTION.md追踪变更；CMP→卡→提示词→参考/镜头→时间线，只标真正受影响部分stale。缓存校验输入输出哈希，不仅文件名。
7. 有外部任务ID先查询或人工核账，未知状态不重复付费；无适配器给接入清单/手动导入，不装作调用成功。没有后台工具不承诺离线跑完通知。

## 输出
07_reviews的初始化/执行报告；本轮实际创作文件；STATE的采用与草稿索引。新版本不覆盖，批准只记录真实消息。最后给已写文件、覆盖缺项、实际检查、未执行媒体与最多三个关键决定。

## 电影校准与可选设定板交接
真实小样顺序建议身份/衣装→空景→已有剧情动作或互动；未有工具/上传/预算授权时只写提示词。先看实际图是否真人电影拍摄观感、角色适配、接触遮挡与空间可信，再查具体脸/手/衣装/灯向；文字完成不等于look达标。
只有显式要求设定板时按DESIGN_SHEETS.md交完整整板与适用独立分格、布局和映射。保留独立原图、复用来源和真实状态，纯拼版不重绘；unconfigured不能冒称执行成功。多格板不可默认当单镜首帧。
维护合并后报告并停止；不能自动执行刚加入的rebuild_cinematic_visuals或更改配音/剪辑接口。
母图允许采用正面图直接出整板候选，或独立图审核后拼版；缺全部侧背/胸像不阻塞整板正文，未知部分明确最小补全。两路均逐格检查，不强制改换用户选择的路线。
