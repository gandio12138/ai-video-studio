# 数据交接协议 v2.0
本包 JSON 是中立业务数据，不是任意服务商的 API 请求体/ComfyUI 工作流，也不是 NLE 原生工程。

## 文件边界
`04_visual/assets.json` 沿用 v1 主资产表（允许新增 sha256、duration_ms、source_job_id、license_ref 等字段）；`08_audio/lines` 管理台词/take；`12_runs/jobs` 管理执行；`10_edit/timelines` 管理采用；STATE.md 管理人读进度。不要把四者合并成无法追溯的一张自由文本表。
模板是未完成草稿，null 表示未知，不补假数。所有 path 为项目内相对路径；不得是网址、绝对路径、.. 或越界符号链接。真实输入绑定 sha256。只读原稿、原始媒体不覆盖。

## Job
模板见 job.json。type=image/tts/video/alignment/music/sfx/lipsync；status 见 HARNESS.md。input_refs 是 `{path,sha256}`；parameters 放业务文本、声音版本和已验证服务参数，不能含密钥。request_fingerprint 为 type/provider/model/input_refs/parameters 的规范 JSON SHA-256；不包含状态/重试计数，便于判断同一请求。
`ready` 及之后需填写服务/模型（手工导入 model=manual）、输入文件哈希、request_fingerprint、有效 approval_ref；`manual_import` 可无付费批准但必须有素材来源/权利记录。提交以后保留 provider_job_id；未知/超时不能重建。
`outputs` 每项 `{path,sha256,duration_ms}`（静图 duration_ms=null）。succeeded 需真实非空输出，校验哈希与媒体；review_status 独立 not_reviewed/approved/rejected。此处检查是协作校验，不是不可绕过的审批平台。
budget.max_cost 是该 job 所有尝试的上限，estimated_cost/actual_cost 未知用 null；批次预算还需在审批和账单中汇总，不把逐任务上限误当无限总额。正式 adapter 必须在提交前落实预算预留、查询对账、成功后的文件校验，不能只靠提示词。

## Voice / TTS
voice_bible 固定角色与 voice_version；provider_voice_id 必须真实存在且所选模型支持，不能用 C001 替代。
每条 line_id 稳定；spoken_text 才提交发音，direction 是表演指导，subtitle_text 是显示文本，三者不能混读。pronunciation 用于人名/多音字/数字。takes 记录 path/hash/实际长度/provider job/质量状态；selected_take 指向真实采用版。
服务商的响应可能是音频字节、编码音频或下载地址；adapter 必须按当时官方文档解码/下载，不把 JSON/错误页保存成 .wav。保留原始音频与转换后文件，不能靠改后缀转换格式。

## Timeline：本地预览器实际支持的 v2 字段
顶层 `schema_version="2.0"`, episode_id, status=draft/approved, fps_num, fps_den, width, height, duration_frames, video, audio, subtitles, notes。
video 每项：
```json
{"clip_id":"V001","shot_id":"EP01_SH001","asset_id":"IMG001","kind":"image","path":"06_assets/generated/frame_v01.png","sha256":"真实64位哈希","start_frame":0,"duration_frames":90,"source_in_ms":0,"fit":"contain","motion":"none","playback_rate":1,"source_audio":"drop"}
```
kind=image/video；clip_id 跨视听事件唯一。视频条目按 start_frame 连续排列，不支持空隙、重叠、叠画/转场。image.source_in_ms=0。fit=contain 保持完整加边，cover 填满居中裁切；不能保证人脸永远在安全区。当前 motion 只接受 none，playback_rate 只接受 1，source_audio 只接受 drop。不要写字段后让 renderer 悄悄忽略。
audio 每项：
```json
{"clip_id":"A001","asset_id":"AUD001","line_id":"EP01_DL001","kind":"dialogue","path":"08_audio/takes/line_v01.wav","sha256":"真实64位哈希","start_frame":12,"duration_frames":60,"source_in_ms":0,"gain_db":-3,"fade_in_frames":0,"fade_out_frames":0}
```
kind=dialogue/music/sfx/ambience。音轨可跨镜或彼此重叠；source_in_ms + 所需时长不得超过实际音频（容许最多一帧的帧网格量化差，尾部补静音，不循环/加速）。fade_in+fade_out 不超过长度。当前没有自动跟随人声 ducking、速度变化或自动补音乐循环。
subtitles=null，或 `{path,sha256,mode:"sidecar"/"soft",language:"zho"}`。只接受已验证、非重叠 SRT；显示能力依播放器实测。烧录字幕须另接后端。
字段集严格校验；要扩展到动画/转场，先升级契约和后端测试，不往 JSON 偷塞无效字段。素材尺寸/帧率归一化只在衍生预览进行，不改原件。视频原生声音默认为 drop。

## 对齐 / SRT
line_alignment 包含 schema_version、episode_id、status=draft/verified、timing_source=estimated/manual_verified/provider_verified/aligner_verified、timeline_timing_sha256、review_reference 和 cues。
每个 cue 为 `{cue_id,line_id,speaker_id,audio_asset_id,start_ms,end_ms,text}`，时间是采用时间线绝对毫秒，半开区间；单轨不能重叠。早期稿允许 estimated，但导出 SRT 必须 verified、有真实检查依据。
`timing_fingerprint` 取 fps、总帧数、video 与 audio 的结构/素材哈希，不含字幕自身，避免循环哈希。剪辑/音频变化后须重新核验，更新指纹；脚本只查数据一致性，不验证人是否真的听过。

## 变更影响
- 改一条 spoken_text：该句 TTS、对齐/字幕、相关 audio 时间线；若影响镜长则相关画面时间线、混音/导出；需要口型的对应镜头也失效。
- 只改字幕标点：字幕与字幕成片派生失效，不自动重做 TTS。
- 改声音版本：该角色采用 TTS、对齐、混音、口型素材失效；无关人物图不失效。
- 改脸/服装：对应参考、关键帧、动态镜头/口型输出、导出失效；对白文本不自动失效。
- 调整镜长/顺序：时间线、字幕对齐、音效点位、成片失效；不代表所有源素材都要重生成。

## 适配器将来要提供的最小接口
`capabilities()`：实际支持参数/限制/计价来源日期。
`estimate(job)`：币种、量、费用范围，不确定则阻止批量。
`submit(job, approval)`：显式授权、预留预算、返回 provider_job_id。
`poll(provider_job_id)`：恢复与查账；超时不能默认新建。
`fetch(result)`：只接收允许媒体，安全下载并检验文件/哈希/实际规格。
`cancel()`：仅当服务实际支持，取消不等于免单。
用户手动网页生成也是一种合法入口：导入时记录 provenance=manual_import、模型/版本已知项、费用已知值或 unknown、权利来源；不谎称是自动接口执行。

## 本地工具限制
validate 检查格式与部分状态，不是通用 JSON Schema 引擎；不验证故事、完整依赖图或账单总额。renderer 的 dry-run 不联网，不渲染，但可读取本地媒体测量。render --execute 真正生成本地文件并输出报告；不自动调用云端。

## v2.1 双入口内容与逐句台词
入口规范见 WORKFLOW_ENTRYPOINTS.md。G1 的内容依据在 novel_direct 是 source_packet，在 original_script 是原创剧本；不要求 A 新建独立润色剧本。
新增 `templates/line_sheet.json` 是 agent 用的逐句文本模板，不是服务商 API，也没有新增自动执行器或完整 JSON Schema 校验器。document_type=line_sheet；entry_mode=novel_direct/original_script；status=draft/approved。content_ref 指 G1 内容依据及真实哈希，approval_ref 只记录真实批准。
每句含 line_id、speaker_id、kind=dialogue/voiceover、spoken_text、direction、subtitle_text、source_refs、provenance=source_exact/user_given/ai_proposal/pending、normalization_notes、shot_ids、recorded_audio_duration_s。模板的 null/pending 是未知，不是合格任务。
A 的对白/旁白选自实际原文，source_refs 可追溯；改词不再属于 source_exact，需单独批准并记录。B 的创作提案标 ai_proposal/user_given，不虚构原文出处。旁白沿用稳定台词 ID，并登记声音角色，不能因此往画面增加出镜人物。
沿用 tts_job.script_ref 字段名避免破坏 v2 任务模板；A 可指 source_packet，B 指剧本。Job.input_refs 还需记录采用台词表、声音卡与必要参考哈希。当前工具并不自动验证 line_sheet 与剧本/原文的语义一致性，需审校与人工确认。
本次不改变 timeline/job/alignment 的 schema_version=2.0，也不改变原 shotlist 的 schema_version=1.0；模板包版本号与不同数据契约版本不要混为一谈。
