# 长期生图提示词标准包

这不是 C001 的新提示词，也不是一套新 harness。它把用户两份详细提示词的写法提炼成项目级默认规则，供现有技能和两条故事入口共同使用。

## 内容

- `PROMPT_AUTHORING_STANDARD.md`：通用编写规则，涵盖人物、全身、母图、场景、道具、剧情关键帧和局部编辑。
- `INSTALL_WITH_CODEX.md`：保留用户项目与版本的合并步骤，以及应写入 AGENTS.md 的引用块。
- `references/prompt_authoring/*.prompt.txt`：用户提供的两份原始示例，原文不改，作为写作参考而不是待执行任务。
- `references/prompt_authoring/SOURCE_NOTES.md`：哪些方法来自示例，哪些是为通用场景新增的规则。

## 使用

将整个 `prompt-authoring-standard` 文件夹放到现有项目根目录，进入该项目的 Codex，发送：

```text
读取 prompt-authoring-standard/INSTALL_WITH_CODEX.md。
我要把这两份样例的写法和细节精度变成以后的默认规范，不是改这次C001。
先比较现有规则，给合并计划；我确认后再更新根AGENTS、相关技能和所有生图提示词入口。
保留项目内容与状态，不生图，不改故事，不调用付费接口。
```

合并到 Mac 项目之前，这个包本身不会让现有技能自动生效。没有修改用户电脑，也没有运行新图生成。
