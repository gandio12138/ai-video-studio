---
name: manju-shots
description: "用于把已确认的场景剧本拆成可制作的文字镜头表，填写景别、机位、动作、对白、音效、采用时长和素材编号。不生成图片或冒充视频接口工作流。"
---

# 文字分镜与镜头表

## 输入
读 AGENTS.md、PROJECT.md、STATE.md 与已确认剧本；读 templates/shot_fields.md 和 templates/shotlist.json。读取 04_visual/assets.json 及已有视觉设定。无确认剧本时先说明，只按用户授权做试拆。

## 步骤
1. 先列本集信息节拍，再决定镜头。一个镜头承担一个主要叙事任务，非必要不为凑数拆镜。
2. 将人物、场景、道具、声音需求登记为稳定资产编号。缺少 assets.json 条目时可新增 planned 且 path=null 的需求项；不得改已确认资产或伪造素材文件。
3. 每镜写景别、角度、运镜/后期裁切、可见动作、对白、旁白、音效、源剧本节拍。静态关键帧只容纳一个明确瞬间，过程另在 action 描述，不混进一张图的要求。
4. 给 edit_duration_s；未选视频模型时 generation_duration_s=null。纯静帧也用 null。生成时长与采用时长不同；有意慢放等处理在 post_notes 解释。
5. 给 continuity_in/out，检查关键道具从哪来、在谁哪只手、视线和相对位置是否接续。将场次 SC01 与地点资产 L001 分开。
6. 素材需求不只写“人物图”：写具体 C001/L001/P001，以及必要的角度、表情、服装/道具状态与声音。制作方法优先考虑静帧运镜或简单后期，复杂动态图给替代方案。
7. 数值合计采用时长，与目标比较；估算台词后标注需朗读。存在跨镜旁白/声音桥时写清，不重复计时。生成 JSON 后再从同版数据写 Markdown 镜头表。
8. 环境有 Python 3 时运行 `python3 tools/check_shots.py 03_shots/EP01_shots_v01.json --assets 04_visual/assets.json --root .`，版本路径按实际修改。修复错误，解释未解决警告；没运行就如实说明。

## 输出
03_shots/EP01_shots_v01.json、EP01_shots_v01.md、素材需求摘要；必要时仅新增 04_visual/assets.json 计划条目。宽表可以拆成“镜头创意表”和“声音/素材表”，以镜号关联，不能丢字段。
镜头状态仍为 draft，随后交 manju-audit 复核，再制作视觉设定。

## v2 生产交接
此表是创意/计划层，不等于剪辑时间线。对白可增加 line_id 字段，跨镜音轨在独立 timeline 仅放一次；后续 manju-voice 实测后再修订帧时长。保留原 v1 字段兼容 check_shots。
