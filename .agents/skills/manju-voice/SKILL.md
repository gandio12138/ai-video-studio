---
name: manju-voice
description: "用于角色试音、声音设定、逐句 TTS 任务、配音导入、重做与实测时长；没有配音适配器时只生成任务单，不用文字冒充音频。"
---

# 声音定妆与逐句配音

先遵守根目录 AGENTS.md；路径相对项目根目录。


## 输入
已确认剧本/台词版本、人物目标、分镜初稿、providers、批准范围。读 templates/voice_bible.json、tts_job.json 与 contracts/PRODUCTION.md。
## 步骤
1. 建声音定妆卡：角色 ID、声音版本、音域/质感/口音/速度倾向、禁变项、允许情绪幅度、服务商真实 voice_id、授权来源。不杜撰 voice_id。
2. 抽中性、冲突、低声三种短句试音；先确认音色再批量。默认内置许可音色；克隆需明确授权及服务商要求，不把演员名字当授权。
3. 给每条稳定 line_id；spoken_text、direction、subtitle_text 分开。人名/多音字/数字读法建 pronunciation 表。只有服务支持的参数才映射；不支持的情绪参数保留为指导而非伪造 API 字段。
4. 每句可有多个 take。依模板生成任务，输入包含剧本/声音卡/参考哈希。未配置接口就 planned/blocked；用户也可在网页生成后手动导入。
5. 真实文件先留原件，再用 probe 实测；统一格式是单独转换步骤。听检漏字/错字/情绪/音色/停顿，有能力才标通过。ASR 回读辅助比对但不自动替代剧本原句。
6. 回写 recorded_audio_duration_s 或独立跨镜音轨计划；声音过长先提出删词、延长镜头或拆镜，不私改已确认对白、不默认加速。
7. 重做仅影响该 line/take 及相关字幕、时间线/口型同步；没有影响画面的改动不重生成所有图像。
## 输出
08_audio/voices/voice_bible_vNN.json、08_audio/lines/EP01_tts_vNN.json、真实 takes（接入/导入后）、配音检查、实际时长和依赖。配音完成不等于口型同步完成。
