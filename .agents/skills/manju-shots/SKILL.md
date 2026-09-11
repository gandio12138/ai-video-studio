---
name: manju-shots
description: "用于把小说原文制作依据或原创剧本拆成可制作的文字镜头表，填写景别、机位、动作、对白、音效、采用时长和素材编号。不生成图片或冒充视频接口工作流。"
---

# 文字分镜与镜头表

## 当前视觉目标与范围
先读CINEMATIC_LOOK.md与PROJECT/STATE的当前视觉设置。cinematic_live_action使用真人电影式单幅目标；完整入口/complete_visual_pack按full_pack，已有内容的风格纠偏按rebuild_cinematic_visuals的calibrate_only，用户明示范围优先。设定板只在用户显式要求时读DESIGN_SHEETS.md并启用；它不替代实际剧情镜头校准。维护或初始化任务不进入创作/媒体执行。


## 输入
读 AGENTS.md、WORKFLOW_ENTRYPOINTS.md、PROJECT.md、STATE.md。novel_direct 读本轮 source_packet、事实表、原文定位与逐句台词，不要求独立剧本；original_script 读采用剧本和逐句台词。读 templates/shot_fields.md、templates/shotlist.json、04_visual/assets.json 及已有视觉设定。无G1确认时仅按明确授权试拆；v2.3两个入口均含当前集文字试拆授权，输出必须draft。另读VISUAL_PRODUCTION.md、本轮CMP补全台账与详细视觉卡，不能每镜另造造型。

## 步骤
1. 先列本集信息节拍，再决定镜头。一个镜头承担一个主要叙事任务，非必要不为凑数拆镜。
2. 将人物、场景、道具、声音需求登记为稳定资产编号。缺少 assets.json 条目时可新增 planned 且 path=null 的需求项；不得改已确认资产或伪造素材文件。
3. 电影式镜头按CINEMATIC_LOOK.md写摄影机世界位置/距离与透视、叙事焦点/景深、人物视线/重心/手部、接触遮挡及主光来源。每镜写景别、角度、运镜/后期裁切、可见动作、对白、旁白、音效、原文/source_packet/剧本节拍定位。静态关键帧只容纳一个明确瞬间，过程另在 action 描述，不混进一张图的要求。
4. 给 edit_duration_s；未选视频模型时 generation_duration_s=null。纯静帧也用 null。生成时长与采用时长不同；有意慢放等处理在 post_notes 解释。
5. 给 continuity_in/out，检查关键道具从哪来、在谁哪只手、视线和相对位置是否接续。将场次 SC01 与地点资产 L001 分开。
6. 素材需求不只写“人物图”：写具体 C001/L001/P001，以及必要的角度、表情、服装/道具状态与声音。制作方法优先考虑静帧运镜或简单后期，复杂动态图给替代方案。
7. 数值合计采用时长，与目标比较；估算台词后标注需朗读。存在跨镜旁白/声音桥时写清，不重复计时。生成 JSON 后再从同版数据写 Markdown 镜头表。
8. 环境有 Python 3 时运行 `python3 tools/check_shots.py 03_shots/EP01_shots_v01.json --assets 04_visual/assets.json --root .`，版本路径按实际修改。修复错误，解释未解决警告；没运行就如实说明。

## 输出
03_shots/EP01_shots_v01.json、EP01_shots_v01.md、素材需求摘要；必要时仅新增 04_visual/assets.json 计划条目。宽表可以拆成“镜头创意表”和“声音/素材表”，以镜号关联，不能丢字段。
镜头状态仍为draft，交audit复核；与visual/enrich局部回查后必须交prompts输出本轮每镜独立关键帧提示词，不以镜头表已完成代替视觉提示词已完成。

## v2 生产交接
此表是创意/计划层，不等于剪辑时间线。对白可增加 line_id 字段，跨镜音轨在独立 timeline 仅放一次；后续 manju-voice 实测后再修订帧时长。保留原 v1 字段兼容 check_shots。

## v2.1 保真与台词交接
A路线不改选中对白；允许按VISUAL_PRODUCTION.md把已登记A/B制作补充写入草稿动作/镜头，连接原文既有起止状态，不得偷加C核心事件。补充动作和新增镜头计入总时长，已确认镜头变更先列影响。每个 dialogue 对象带 line_id，旁白在 voiceover_line_ids 和 post_notes 中关联台词表，跨镜覆盖清楚标记。原有 check_shots 对新增关联字段不做完整校验，另人工核对引用及重复计时，不夸称其已验证。
source_refs可同时引用原文/source_packet与补全台账CMP；B引用采用剧本或明确授权草稿。可追加completion_refs、wardrobe_versions、visual_prompt_refs等交接信息，但原check_shots不验证这些扩展。原文没写的拍法/动作是制作补充，不是小说事实。镜头时间不够时先提出延长/拆镜/拆集，不擅自删台词或把缺失剧本当阻塞。

## 独立参考与可选设定板的使用
电影式镜头先读CINEMATIC_LOOK.md和采用视觉卡/布局；仅需要使用设定板资料时读DESIGN_SHEETS.md。镜头绑定具体衣装/状态、场景布局和机位，参考需求指向相关独立单图而非笼统“用整张设定板”。
设定板多格不是连续剧情镜头，特殊状态格不等于故事已经发生；人物三视图不产生多个角色。每镜关键帧仍独立单幅。反打从同一布局换机位，不镜像重造房间。
