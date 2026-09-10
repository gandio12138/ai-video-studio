---
name: manju-producer
description: "在用户要初始化、继续制作、检查进度或定位阻塞时使用；编排小说到成片的技能、版本、审批、预算与依赖，不代替各工种且不擅自付费。"
---

# 全流程统筹与恢复

先遵守根目录 AGENTS.md；路径相对项目根目录。


## 输入
读 AGENTS.md、PROJECT.md、STATE.md、CAPABILITIES.md、HARNESS.md、config/runtime.json；只读取当前阶段相关产物与任务日志。
## 执行
1. 初始化时运行 `python3 tools/studio.py doctor --root .`（有 Python 时），报告缺项，不安装任何东西；未接通的服务标 unconfigured。
2. 把用户要求拆成一批有明确终点的工作：输入版本、输出文件、采用的 skill、费用/上传范围、是否需要真实媒体、验收条件。
3. 按 G1–G5 检查用户确认；不把审校报告当成批准。计划生成、待服务配置、实际执行分开。
4. 保持关键链：确认台词 → 试音/配音 → 实测 → 有声分镜 → 动态镜头 → 粗剪 → 定剪 → 对齐字幕与混音复核。声音与视觉允许并行。
5. 变更影响按 contracts/PRODUCTION.md 定位；只让相关 take/字幕/镜头/时间线 stale。缓存复用需输入与输出哈希吻合，不能仅因文件名相同就复用。
6. 恢复云任务必须先查已提交 ID，超时/未知状态禁止重建任务；没有适配器时给出接入清单或手动导入路线，不假装调用。
7. 返回下一项最小可执行动作；只有用户要求才继续到下一关。不要在本轮未调用支持工具的情况下承诺后台跑完通知。
## 输出
07_reviews/setup_check_vNN.md 或 run_plan_vNN.md；必要时更新 STATE.md 的草稿/阻塞信息。任务单放 12_runs/jobs；真实用户批准放 approvals。
