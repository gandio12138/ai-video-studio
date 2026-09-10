# Harness 固定入口

同一个故事一次只选一条，选择记录在 PROJECT.md，进度记录在 STATE.md。

- `entry_novel_direct.md`：有小说，跳过独立编剧/润色，直接按原文整理并试拆镜头。
- `entry_original_script.md`：没有小说，用设定、人物、概述开发原创首集剧本。

在 Codex 中说“读取 prompts/entry_novel_direct.md，小说路径……，范围……”或“读取 prompts/entry_original_script.md，我的设定……”。占位输入可在消息里补充，不必每次编辑系统技能。

两条路都保留 G1 内容确认，再接现有配音、视觉、视频、字幕、混音和剪辑。小说路线的 source_packet 不是额外的改写剧本。详细规则见根目录 WORKFLOW_ENTRYPOINTS.md。
