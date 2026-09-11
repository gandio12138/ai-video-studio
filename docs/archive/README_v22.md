# AI漫剧工作室 Harness v2.2

**两个内容入口，共同交详细视觉包。**有小说：保留核心剧情和采用原句，不做独立剧本打磨；没有小说：从设定、人物和概述试写首集剧本。两路都主动补足服饰、人物、场景、道具和必要事件接续，继续交人物/场景/逐镜生图提示词，而不是停在剧本或镜头表。

## 先看哪些文件
START_HERE.md：初始化和三种实际调用。
WORKFLOW_ENTRYPOINTS.md：两路区别与汇合。
VISUAL_PRODUCTION.md：主动补全、审美细节、提示词完整覆盖的共同标准。
MIGRATION.md：已有项目如何合并，不覆盖创作内容。

## 十五个技能
story、script、audit、shots、visual、prompts；新增enrich处理视觉与事件细节缺口；producer统筹；images、voice、video、subtitles、sound、edit、delivery接后续制作。实际名称均以manju-开头，目录位于`.agents/skills/`。

原来十四个技能保留，不需要再造一套配音和剪辑协议。新增技能不是新增模型或接口。

## 必交文字成果
来源/用户设定与CMP补全台账；本轮内容依据和台词；接续表与镜头；统一美术及角色/衣装/场景/道具详细卡；每独立角色五类参考提示词、每场景三类、关键道具、每镜完整正文和两类局部编辑预案；真实文件索引和检查报告。范围限定在选定片段/首集，不设计全书。

普通视觉/局部桥接缺口主动填成草案，不逐项追问；核心变化分级提案。原文事实与补充明确分开。故事有意悬念不当漏洞解释。人物造型需符合身份、财力、时代、任务与天气，不能统一年轻美颜或给所有人华服。

## 目录
```text
.agents/skills/          十五个技能
prompts/                两入口 + 已有内容补视觉入口
VISUAL_PRODUCTION.md     共同视觉/补全标准
01_story/               事实/设定/CMP台账
02_scripts/             source_packet或原创剧本/台词
03_shots/               镜头与状态接续
04_visual/              STYLE与characters/locations/props详细卡
05_prompts/             characters/locations/props/shots/edits提示词与索引
06_assets/              真实图片/参考
08_audio/、09_video/     声音与动态片段
10_edit/、11_exports/    中立时间线与真实导出
12_runs/                任务、日志、采用与批准
```

## 已有工具和边界
继承v2的Python/FFmpeg基础本地粗剪与媒体检查工具；实际支持范围以CAPABILITIES.md为准。本次不改执行工具，不新增生图/TTS/视频/口型/剪辑软件API，也不新增EPUB解析。

缺API或参考图不阻塞文字草稿；依赖参考标awaiting_reference，路径未有真实文件时为null。不生图不等于不写提示词。草稿不等于用户批准，提示词不等于图片，文件存在不等于视听质量合格。

两路在G1前可以按明示批次做文字试写/试拆/视觉提示词；实际生成仍需要具体范围、参考条件与服务/上传/预算授权。项目规则是协作协议，不是不可绕过的系统沙箱或硬限额。

## 验证
见VALIDATION.md和tests/reports/v22_structure_check.json。结构/单元测试不能证明审美、原文忠实度或Codex真实端到端制作已经通过。示例只是原创教学片段，无实际图片/声音/视频。
