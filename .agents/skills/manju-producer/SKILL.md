---
name: manju-producer
description: "用于初始化、双入口创作、补视觉、继续制作与恢复；统筹内容、主动补全、人物/场景/逐镜提示词和后期，检查交付覆盖、版本、审批与预算，不擅自生成媒体。"
---
# 全流程统筹与恢复

先读AGENTS.md、PROJECT.md、STATE.md、WORKFLOW_ENTRYPOINTS.md、VISUAL_PRODUCTION.md、CAPABILITIES.md、HARNESS.md和config/runtime.json；只取本轮相关资料，不读全书或未经指定的examples。

## 路由与文字批次
- novel_direct：story原文事实→source_packet/台词→enrich细节/桥接→visual详细设计↔shots文字镜头→prompts完整正文→audit保真/连续性。跳过独立script润色，缺独立剧本不阻塞。
- original_script：story简报/人物/大纲→script首集试写/台词→enrich细节/桥接→audit剧情→visual详细设计↔shots试拆→prompts完整正文→audit视觉与接续。缺小说不阻塞，入口已授权draft试写/试拆。
- 已有内容调用complete_visual_pack时只补缺，保留已确认剧情/台词/素材，不机械重写全部。
- 未选入口只问入口；小说范围未定先选片段；只初始化不创作。

完整v2.2入口首轮包含文字视觉提示词；不是在剧本/镜头表后停下另问“是否需要提示词”。用户只要求局部则按局部。普通A/B补充已获草稿批次许可；C核心提案依入口处理。缺实际参考/模型不阻塞文字，只标条件和未就绪执行。

## 操作
1. 初始化可运行 `python3 tools/studio.py doctor --root .`，缺工具报告，不自动安装；外部服务未接入如实记unconfigured。
2. 明确本批输入版本、范围、skill、真实文件交付清单、停止条件与媒体权限。plan下只文本/离线检查。
3. 覆盖检查按VISUAL_PRODUCTION.md：补全台账、人物/场景/道具详细卡、接续表/镜头、人物五类/场景三类/关键道具/逐镜/两类编辑预案和索引。不能仅列清单代替正文；不能只示例部分却标整包完成。
4. 记录draft、prompt_only、awaiting_reference和真实资产状态，分开内容/视觉方案批准与媒体执行批准。没实际看到/听到的媒体不宣称验收。
5. G1内容/台词/叙事补充；G2视觉/衣装/场景/声音身份；先少量试音和定妆小样，再实测配音/关键帧/有声小样，按G3预算进入动态镜头，G4剪辑，G5交付。不得默认全季批量。
6. 按contracts/PRODUCTION.md追踪变更；CMP→卡→提示词→参考/镜头→时间线，只标真正受影响部分stale。缓存校验输入输出哈希，不仅文件名。
7. 有外部任务ID先查询或人工核账，未知状态不重复付费；无适配器给接入清单/手动导入，不装作调用成功。没有后台工具不承诺离线跑完通知。

## 输出
07_reviews的初始化/执行报告；本轮实际创作文件；STATE的采用与草稿索引。新版本不覆盖，批准只记录真实消息。最后给已写文件、覆盖缺项、实际检查、未执行媒体与最多三个关键决定。
