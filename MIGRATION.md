# 升级到 v2.1：保留已有故事与进度

## 尚未开始正式创作
另解压 v2.1 完整包，在新目录启动，保留旧目录作备份。不要解压覆盖旧项目。

## 正在用 v2 harness
使用独立 `ai-manju-v2.1-update` 更新包。它将新增文件和参考改稿放在分开的子目录，不是直接覆盖补丁。把整个更新包文件夹放到旧项目根目录，先让 Codex 读取其中的 APPLY_WITH_CODEX.md，按清单提议差异；确认后再合并。

必须新增：WORKFLOW_ENTRYPOINTS.md、prompts 两个入口、templates/source_packet.md、templates/line_sheet.json。
必须合并：AGENTS.md 与 producer 的路由，story/script/audit/shots/visual/voice 的输入条件。删除或替换旧“所有内容必须先写独立剧本”的冲突，不只在末尾堆新规则。
PROJECT.md / STATE.md 保留你真实的项目名、原文路径、创意、确认版本和进度，只新增入口/内容依据/台词字段；无用户依据不得把任何状态改成 approved 或 completed。

旧的未指定“原创”值可能表示原创小说，也可能表示原创剧本，不能自动猜；只有新用户要求明确时设置对应 entry_mode。切换不同故事建议新目录，禁止默默混入人物与旧小说。

不覆盖 00_source–12_runs 内的正式文件、实际资产表、所有媒体、config 密钥/预算/许可与批准日志。不复制 examples 到正式目录。不运行任何媒体工具。

完整包包含用于新项目的 PROJECT/STATE 初始化模板，**不是已有项目迁移后的真实状态**。

## 验证
核对两个入口都能被当前项目指令找到：A 缺独立剧本不阻塞，B 缺小说不阻塞；十四个技能仍在。源文件/媒体/用户确认记录未改。Python 可用时重跑现有单元测试；测试通过不代表 Codex 的自然语言路由已做端到端验证。

旧 v1→v2 迁移说明保留在 docs/archive/MIGRATION_v1_v2.md。本次不更改媒体后端与运行时默认权限。
