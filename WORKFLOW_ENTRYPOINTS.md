# 两种入口与共同视觉交付｜v2.3

两条路的区别在内容起点，不在有没有生图提示词。**两条路都必须主动补齐视觉/衔接细节，产出详细人物、场景和逐镜提示词。**共同标准为 CINEMATIC_LOOK.md 与 VISUAL_PRODUCTION.md；当前电影式完整批次交必要独立参考和每镜正文，设定板仅显式要求时按DESIGN_SHEETS.md启用。

## 入口设置
所有生图提示词入口先读PROMPT_AUTHORING_STANDARD.md，按本轮资产类型交完整正文与可见验收；两条内容路线、新角色、新地点和后续集数统一适用。短指令不降低正文精度，也不扩大本轮范围。

已有图片扩展使用prompts/expand_character_masters.md的通用分支及manju-visual/manju-prompts；任务内的C001预填资料仅属于该批次，不是默认人物。场景扩展目前无独立入口文件，直接由同两技能按共享规范第7节固定空间、换机位；道具/单镜/局部编辑分别按第7.3/8/9节，不必重新执行整集入口。
`entry_mode` 沿用 novel_direct / original_script / undecided，存 PROJECT.md；实际进度、采用版本和确认存 STATE.md。新增人读设置 `visual_pack_required: true` 与 `completion_policy: visual_and_local_bridge_draft`，不是 runtime/API 参数，不往严格工具JSON中乱加字段。

| 模式 | 输入与内容依据 | 跳过的步骤 | 首轮完整文字范围 |
|---|---|---|---|
| novel_direct | 实际小说片段 → 原文事实/source_packet/台词 | 独立编剧、对白润色、重写大纲 | 制作依据 + 细节补全 + 定妆/场景 + 试拆分镜 + 完整生图提示词 + 保真/视觉检查 |
| original_script | 设定/人物/概述 → 简报/人物/首集剧本/台词 | 索要小说、先写小说正文 | 首集试写/审校 + 细节补全 + 定妆/场景 + 试拆分镜 + 完整生图提示词 + 视觉检查 |
| undecided | 用户尚未选择 | 不因目录有EPUB自动选路 | 只问入口，不自行创作 |

入口文件：prompts/entry_novel_direct.md、prompts/entry_original_script.md。两完整入口与prompts/complete_visual_pack.md默认full_pack；已有内容只纠正电影观感用prompts/rebuild_cinematic_visuals.md，默认calibrate_only；显式要求设定板用prompts/complete_design_sheets.md。用户本轮明确范围优先，只维护/初始化不创作。

## A：有小说，跳过独立剧本打磨

原文只读，列实际读取范围；来源与补充分开。片段未定先给最多两个候选并停；EPUB不可读先报告缺工具/需TXT或经允许补导入器，本包未新增EPUB解析。

范围明确后：story提取原文事实；producer/source_packet整理分场与逐句台词；enrich补A视觉/B局部衔接；visual详细设计；shots试拆；prompts展开全部图像提示词；audit审查原文忠实度、补全边界与连续性。

不调用独立script润色；source_packet不是空剧本占位。保留选中对白/旁白原句，实质改词/删句/并句/新增对白需单独批准。允许补服饰、外貌、空间、表演和连到原有终点的动作；不能把“按原文”误解成普通制作细节都不准补。

核心新事件/新主角/能力/关系/信息与反转不属于视觉许可；列C提案，未批准不混入A主版本。故意悬念不要补成答案。原文装不下目标时长先延长/拆集，不强行删因果。

## B：没有小说，直接原创并做视觉开发

保留用户原始输入，story建立简报/人物目标/大纲；script写首集剧本/台词；enrich把外观/服饰/空间/事件桥接补入新草稿；audit查因果/人物/时长；visual、shots与prompts继续产出详细视觉和镜头提示词。

未给定剧情可在用户方向内创作，不把所有新事件都当需要逐项询问的禁区。核心空白可列最多两个方案，按明示临时方案试写；不改用户已经指定的硬设定，不用巧合或降智解决因果。没有大纲批准也可完成授权的draft批次。

**v2.3两个入口都明确允许G1前的文字试拆、设计与提示词草稿**。不能按旧B入口在剧本审校后提前停止。实际生成依旧需内容/设计范围与工具/预算授权；文本草稿不自动转批准。

## 共同交接

G1内容依据：A `02_scripts/EP01_source_packet_vNN.md`；B `02_scripts/EP01_vNN.md`。共用 `EP01_lines_vNN.json`，spoken_text/direction/subtitle_text分开。TTS模板沿用script_ref字段，但A可以指source_packet；不为配音另写剧本。

图像交付按CINEMATIC_LOOK.md与VISUAL_PRODUCTION.md第9节：补全台账、状态接续、电影式风格、详细卡、布局/机位、分镜，必要身份/衣装/空间参考、关键道具、每镜单幅正文、人物/场景局部编辑预案、总索引和检查。完整批次full_pack逐镜覆盖，不能以calibrate_only三类样张代替整集；只有显式启用设定板时追加整板/逐格/拼版映射。允许集合文件，但每条须独立完整可定位。

补全采用CMP编号；人物C、地点L、道具P、镜号SH、台词DL和衣装/状态版本连续可追溯。世界布局固定，画面左右按机位变化。缺参考仅阻塞相关实际派生，不阻塞提示词草稿。

G1锁内容/台词/叙事补充，G2锁视觉/衣装/场景/声音身份。小样生成另有明确授权；后续声音实测/关键帧 → 有声小样与批量预算G3 → 视频 → 粗剪/定剪G4 → 字幕/混音/交付G5。

## 边界

只初始化/只选片段/局部任务按实际范围，不强制做完整包。原文未成功读取不虚构；缺小说只阻塞A，不阻塞B；缺云服务不阻塞文字。

原文与已批准版本不覆盖。G1/G2前产物标draft，提示词prompt_only，实际资产未有文件时planned/path=null。用户已确认内容要变更先列影响，不把批次写稿许可当最终批准。

v2.3在原十五个技能上扩展设定板文字规范/模板，不新增媒体API、EPUB解析或自动调度。AI审校、文件格式检查和真实图像/声音验收是不同层次。

## 两路共同的电影式目标与可选设定板
按PROJECT当前look_mode使用CINEMATIC_LOOK.md。两路保留各自内容边界，均主动补齐可穿衣装、可信人物、固定空间与局部动作；单幅正文写具体表演、摄影机、光源、景深/焦点和接触遮挡，不混入旧插画风格词。
calibrate_only只在风格纠偏或用户明示的小范围任务中使用；full_pack继续当前片段/集全部镜头。未有样张时只记录not_generated/not_reviewed，不自动锁风格或冒充用户认可。
asset_sheet_mode=optional。仅用户显式要求时执行DESIGN_SHEETS.md与complete_design_sheets：同版锚点、整板探索提示词、独立单格、固定布局/机位、拼版映射和逐格检查。保留旧板与独立图，不让板面数量替代实际镜头风格校准。
母图可由一张采用正面图直接准备整板候选，也可走独立图审核后拼版；未知结构标最小补充，两路均保留且不新增媒体授权。
