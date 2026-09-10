# 版本记录
## v2.1｜2026-09-10
- 增加 novel_direct / original_script 两个固定入口提示词与 WORKFLOW_ENTRYPOINTS 路由。
- 小说入口跳过独立编剧/润色，保留原文制作整理和忠实度检查；原创入口直接写剧本，不要求小说。
- G1 从只认剧本扩展为对应入口的内容依据与采用台词，更新 producer/story/script/shots/audit/visual/voice 交接。
- 新增 source_packet 与 line_sheet 模板；沿用 v2 TTS 字段和原媒体后端，保留十四个技能。
- 未新增 EPUB 导入器、云端接口、NLE 控制或自动化调度；只改入口指令、模板与文档。
- 现有项目采用差异合并，不能覆盖原 PROJECT/STATE、小说、剧本、媒体与批准记录。
## v2.0｜2026-09-10
- 保留六个前期skill，新增producer/images/voice/video/subtitles/sound/edit/delivery八个，共十四个。
- 将项目从只做前期扩展为Codex驱动的制作harness骨架：阶段关卡、声音/视觉并行、小样先行、依赖变更、状态/预算/重试协议。
- 增加声音定妆、逐句TTS、视频任务、对齐、混音cue、timeline、批准/任务模板。
- 增加本地doctor、媒体probe、SHA-256/时序/请求指纹、结构/真实文件校验、已验证对齐导出SRT。
- 实现受限的FFmpeg基础粗剪：硬切、静帧保持、素材裁切、多轨声音、外挂/软字幕、完整解码验证、拒绝覆盖。
- 外部生图/TTS/视频/ASR/音乐/口型和NLE原生工程只预留接口；没有云调用、自动安装、后台调度或自动发布。
- 56项单元测试通过；4秒合成素材集成测试通过，未验证用户Mac或付费API。
## v1.0
前期六个skill、中文提示词、镜头表/素材协议及check_shots。
