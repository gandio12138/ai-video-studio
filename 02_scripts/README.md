# 02_scripts：共用内容依据与台词

A（novel_direct）：EP01_source_packet_vNN.md，记录原文范围/事实/分场/声音提取，**不是重写剧本**。
B（original_script）：EP01_vNN.md，为原创场景剧本；按需求附对白打磨对照。
两路都输出 EP01_lines_vNN.json（templates/line_sheet.json），为逐句配音和字幕提供稳定编号与唯一采用文本。

配音任务沿用 script_ref 字段：A 指 source_packet，B 指 script；另记录台词表/声音卡的真实哈希。不能因 A 没有独立剧本就阻塞后期。
全部初稿为 draft，用户明确批准后记录采用版本，勿覆盖旧稿。
