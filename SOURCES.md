# v2.2资料说明
本次新增的细节补全、审美要求、分类与示例是为本项目撰写的创作规则，不是模型官方效果保证。本轮未为新增文字规范调用外网；以下技术资料链接与查阅记录继承自v2.1，不表示本轮重新核实了服务、模型或价格。实际接入时需要重新核实当前官方文档。

# 官方资料与实现依据
查阅日期：2026-09-10。以下用于技能发现、项目规则、TTS/视频接口边界与FFmpeg实现；本包的角色流程、JSON契约、预算默认值和审批关卡是本项目设计，不是官方统一规范。

1. OpenAI：Build skills（项目级 .agents/skills、SKILL.md、显式调用与发现）
   https://developers.openai.com/codex/skills/
   当前访问会跳转至 https://learn.chatgpt.com/docs/build-skills
2. OpenAI：Custom instructions with AGENTS.md（项目指令发现与覆盖）
   https://developers.openai.com/codex/guides/agents-md/
3. OpenAI：Text to speech（speech接口、音色、语音生成提示、AI声音披露、自定义声音许可要求）
   https://developers.openai.com/api/docs/guides/text-to-speech
4. MiniMax：接口概览（视频异步任务、语音/TTS/音色能力、不同模态接口）
   https://platform.minimaxi.com/docs/api-reference/api-overview
   本包没有实现或绑定某个具体模型；接入时需再查具体API、账户支持、区域、计价与响应格式。
5. FFmpeg：命令行工具文档（媒体输入/输出、映射与编解码）
   https://ffmpeg.org/ffmpeg.html
6. FFmpeg：滤镜文档（scale/pad/crop、音频裁切/延时/混合、字幕、限幅/响度工具）
   https://ffmpeg.org/ffmpeg-filters.html
7. FFmpeg：ffprobe（媒体流/容器信息、机器可读输出）
   https://ffmpeg.org/ffprobe.html

包内工具和文档不是上述项目的官方作品。模型参数、价格、平台规定可能改变；未核实项不硬编码。字幕显示、字体许可、发布规格、最终响度仍需按用户实际目标核实。

## v2.3新增内容的来源说明
本次设定板规则、场景机位教学示例和模板来自ai-manju-v2.3-update更新包；版式参考的包内来源说明另附，不将该说明当本轮用户上传或批准记录。没有为本轮重新联网核对厂商接口，上面旧链接保留为历史参考，不据此宣称新模型、API参数或拼版能力可用。用户原图来源/用途/哈希见04_visual/references/RF_LAYOUT_USER_01.md。模板计数与版式是本项目约定，不是行业或服务商强制标准。
