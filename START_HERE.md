# 从这里开始｜AI漫剧Harness v2.2

本版保留原十四个技能，新增manju-enrich，共十五个。两入口的完整文字批次现在都包括：补细节与衔接、人物/场景详细卡、分镜和完整生图提示词。没有调用任何生成模型。

## 已经在用旧harness
不要用完整版覆盖旧目录。把解压后的`ai-manju-v2.2-update`整个文件夹放进旧项目根目录，在原项目Codex中输入：

```text
读取ai-manju-v2.2-update/APPLY_WITH_CODEX.md。
先列合并计划，等我确认后更新规则/技能/模板。
保留原小说、剧本、PROJECT/STATE的真实内容、配置、素材与批准记录。
本次只更新harness，不开始创作或生成媒体。
```

## 新项目
使用完整`ai-manju-studio-v2.2`目录，保留隐藏`.agents`。

```bash
cd ~/Desktop/ai-manju-studio-v2.2
codex
```

之后的文字在Codex对话输入，不是在普通shell执行：

```text
$manju-producer
只做初始化：读取AGENTS.md、WORKFLOW_ENTRYPOINTS.md、VISUAL_PRODUCTION.md、PROJECT.md、STATE.md和CAPABILITIES.md。
检查十五个技能、两个入口与complete_visual_pack入口存在。
核对两路都主动补A/B细节，并必交人物/场景/逐镜提示词。
不选故事、不写稿、不安装、不调用接口、不生成或渲染媒体。
输出检查报告，已有版本递增。
```

## 有小说
```text
$manju-producer
执行prompts/entry_novel_direct.md。
原文：00_source/我的小说.txt
范围：填写实际片段起止。
目标：首集60秒，9:16。
保留核心剧情与原句，不另打磨剧本；主动补服饰、人物、场景和必要动作衔接。
本轮交详细视觉卡、分镜、人物/场景/逐镜生图提示词，不真正生图。
```
没有指定片段先选片段；EPUB不可读先解决本地导入，不凭记忆分析。本版没有新增EPUB导入器。

## 没有小说
```text
$manju-producer
执行prompts/entry_original_script.md。
设定：……
人物：……
故事概述：……
必须保留：……
画风偏好：……（无偏好可先推荐）
先做一集60秒；不先写小说。
同批写首集剧本、补细节、试拆分镜与完整人物/场景/逐镜生图提示词。
全部先为草稿，不真正生成媒体。
```

## 已有稿子，只缺视觉
```text
$manju-producer
执行prompts/complete_visual_pack.md。
沿用STATE里的当前版本；不从头重写故事。
补细节、接续表、详细视觉卡和完整提示词，保留已确认内容。
```

完整标准见VISUAL_PRODUCTION.md；演示见examples/visual_completion/worked_example.md。示例不自动作为正式素材。
