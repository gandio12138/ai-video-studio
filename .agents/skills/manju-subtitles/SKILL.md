---
name: manju-subtitles
description: "用于依据真实配音或定剪音轨做字幕、断句与同步检查；不把字数估时当成真实时间戳，也不把 ASR 错字自动写回剧本。"
---

# 对白对齐与字幕

先遵守根目录 AGENTS.md；路径相对项目根目录。


## 输入
采用台词、实际配音及时间线、审核记录。读 templates/line_alignment.json。
## 步骤
1. 优先基于实际采用音轨和确认台词对齐；可用服务返回时间戳、已接入强制对齐或人工定位，说明粒度与误差。接口未接入时列待人工步骤，不编造对齐结果。
2. spoken_text 与 subtitle_text 分开；人名、数字、断句按确认文本复核。ASR 只是证据，发现冲突要听检，不能按识别结果擅改剧情。
3. 时间戳是时间线绝对毫秒、半开区间 [start,end)；与音频文件相对时间区别写清。记录 timeline_timing_sha256 防止剪辑改后仍使用旧字幕。
4. 按真实停顿/阅读节奏断句；同时说话、画外音和纸条文字分别规划。初版 SRT 单轨不支持重叠 cue，需合并或转交另一个已实现字幕方案。
5. 未验证的结果 status=draft、timing_source=estimated。只有实际检查后改 verified，并写 review_reference。
6. 用 `python3 tools/studio.py srt ... --timeline ... --output 08_audio/alignment/EP01_vNN.srt --root .` 导出。脚本校验时间线指纹，但无法听懂声音判断是否真的对齐。
7. 软字幕/外挂字幕不是烧录；烧录与字体检查另接工具，不能承诺所有播放器一致显示。
## 输出
对齐 JSON、SRT、字幕复核报告；定剪或音频变化时标 stale 后重新对齐。
