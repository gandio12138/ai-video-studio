# Harness v2 → v2.1 升级检查报告 v01

检查时间：2026-09-10T15:10:19+08:00

任务状态：completed（项目升级和本地离线检查）；创作尚未开始；entry_mode=undecided。用户授权范围为更新当前 harness；不视为故事、G1、媒体生成或渲染批准。

## 来源与升级前快照

- 来源：用户指定的 /Users/chengchengxu/Downloads/ai-manju-studio-v2.1.zip。
- 压缩包 SHA-256：`a30dabd54f13781624fa7600038c443369087221046893e01e2b3e3b4d3e34de`；大小 157525 字节。
- 压缩包内 113 个文件，总解压大小 269821 字节；逐项读取、CRC 校验，无绝对路径、目录穿越、符号链接、Git 元数据或加密文件。
- 上游 PACKAGE_MANIFEST.json：version=2.1；112 项内容文件哈希全部匹配，无清单外文件（清单自身除外）。
- 升级前 Git HEAD：`c13497c0714600fee1e5f94c9594f435bde919b3`；main 与 origin/main 一致，工作区干净。
- 旧包清单中的现有文件全部与 v2 原始哈希一致；额外本地产物为初始化报告。没有已开始的小说、剧本或实际媒体。
- 本地升级前快照：`/Users/chengchengxu/Desktop/ai-video-studio/.git/upgrade-backups/v2.1-20260910T150812/baseline.tar`，包含 105 个原有跟踪文件；同目录 baseline.json 保存升级前哈希与应用范围。
- 快照 SHA-256：`ab1256605394038b956a8a8081026ce176456783b424309163631bfcf2024d17`。备份位于 .git 内，不提交到 GitHub；旧版本也保存在上述 Git 提交中。

## 本次采用的变化

26 个已有文件更新，9 个文件新增，78 个包内文件保持一致；额外保留旧初始化报告。另新增本报告，最终提交预期为 36 个变更文件（26 修改、10 新增），不删除文件。

- 新增 WORKFLOW_ENTRYPOINTS.md 与两个固定入口提示词：novel_direct 按原文整理制作依据、台词和分镜，默认跳过独立编剧；original_script 从设定、人物与概述直接试写剧本，无需小说。
- 新增 templates/source_packet.md、templates/line_sheet.json；G1 同时覆盖对应入口的内容依据、范围、采用台词与补充。
- 合入 producer、story、script、audit、shots、visual、voice 的双入口规则，共保留十四个技能。
- 同步 README、启动/迁移说明、后期交接协议、目录说明与上游验证归档。
- PROJECT.md 采用内容合并：保留未命名、简体中文、9:16、60±2 秒、最多 2 人/1 场景等原有临时建议、服务未选择状态及许可边界；新增 entry_mode=undecided、输入范围、内容依据和逐句台词字段。原静帧运镜建议标明当前后端未支持。
- STATE.md 按双入口调整阶段名称，所有创作阶段仍未开始；记录真实初始化/升级检查结果，未添加任何作品批准。
- 00_source 仅更新随包 README 说明；RIGHTS.md 未变，没有改写用户原稿。examples 仍是教学/测试资料，未复制进正式作品。
- tools/ 六个脚本及两份测试代码逐字节未变；config/ 三个文件、资产表、许可记录及原初始化报告保持原哈希。

## 清单与本地合并的关系

PACKAGE_MANIFEST.json 原样保留为上游 v2.1 发布包清单，不能把它当成迁移后用户项目的全量清单。本项目与其 112 个文件哈希相比，110 项一致，2 项差异明确为保留本地设置与进度的 PROJECT.md、STATE.md。113 个包文件都存在；另有本地检查报告，不写回上游清单冒充原始包。

VALIDATION.md、tests/unit_test_results.txt、tests/reports/v21_structure_check.json 是压缩包随附的上游记录，描述其原测试环境，不是本机执行日志。docs/archive 下为历史材料。本机验证以本报告为准；上游报告中“没有访问用户 Mac”等表述不用于描述本次本机离线检查。

## 本机验证

执行：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`，退出码 0。

```text

----------------------------------------------------------------------
Ran 56 tests in 0.065s

OK
```

执行：`PYTHONDONTWRITEBYTECODE=1 python3 tools/studio.py doctor --root .`，退出码 0。

- Python 3.14.5；FFmpeg 8.1.1；ffprobe 8.1.1。
- 十四技能文件存在；name/description 基础元数据检查通过。
- 基础粗剪依赖 local_preview_dependencies_ready=true；本轮只查询版本、编码器和滤镜，未渲染。
- 21 个 JSON 文件均能解析，并检查重复键/非标准数值；这不代表新增台词模板获得完整语义校验。
- 双入口文件和引用存在；检查了 A 缺独立剧本不阻塞、B 不要求小说的静态表述。
- 临时结构检查最初要求文档包含固定措辞“不要求小说”，与路由表实际措辞不符而触发断言。已改为核对路由表和 B 入口中的实际约束，复查通过；未为通过检查修改上游入口文档。
- 最终状态与 PROJECT 中入口均为 undecided，现有创作采用文件仍为无。未改变用户预算与权限。
- 自然语言路由真实任务、故事质量、新台词表的原文一致性、媒体端到端行为均为 not_checked。

本机结构检查结果：

```json
{
  "skill_count": 14,
  "frontmatter_name_description_check": "passed",
  "route_static_checks": {
    "required_files": true,
    "three_modes_documented": true,
    "novel_direct_script_optional": true,
    "original_script_novel_not_required": true,
    "entry_documents_linked": true
  },
  "json_files_parsed": 21,
  "protected_files_unchanged": 27,
  "runtime_mode": "plan",
  "external_generation_budget": 0,
  "unconfigured": [
    "minimax_speech",
    "openai_speech",
    "cloud_image",
    "cloud_video",
    "speech_alignment",
    "music_sfx",
    "lipsync",
    "nle_export"
  ],
  "natural_language_route_e2e": "not_checked",
  "media_rendered": false
}
```

doctor 结果：

```json
{
  "python": "3.14.5",
  "python_minimum": "3.9",
  "platform": "macOS-26.6.2-x86_64-i386-64bit-Mach-O",
  "skill_count": 14,
  "skills": [
    "manju-audit",
    "manju-delivery",
    "manju-edit",
    "manju-images",
    "manju-producer",
    "manju-prompts",
    "manju-script",
    "manju-shots",
    "manju-sound",
    "manju-story",
    "manju-subtitles",
    "manju-video",
    "manju-visual",
    "manju-voice"
  ],
  "required_project_files": {
    "AGENTS.md": true,
    "STATE.md": true,
    "PROJECT.md": true,
    "CAPABILITIES.md": true,
    "config/runtime.json": true,
    "config/providers.json": true
  },
  "binaries": {
    "ffmpeg": "/usr/local/bin/ffmpeg",
    "ffprobe": "/usr/local/bin/ffprobe"
  },
  "versions": {
    "ffmpeg": "ffmpeg version 8.1.1 Copyright (c) 2000-2026 the FFmpeg developers",
    "ffprobe": "ffprobe version 8.1.1 Copyright (c) 2007-2026 the FFmpeg developers"
  },
  "local_preview_dependencies_ready": true,
  "local_preview_blocker": "",
  "cloud_adapters_implemented": false,
  "network_calls_made": false,
  "installed_anything": false,
  "note": "这不是你的生产权限批准，也没有验证 Codex 已加载 skill。"
}
```

## 文件变更与最终哈希

本轮阅读了原有项目入口、最新 AGENTS/producer、迁移说明、双入口提示词/路由、相关技能和文档差异、模板及包清单；对包内其他文件做字节/哈希比较，未把读取模板视为创作执行。

| 文件 | 操作 | 升级后 SHA-256 |
|---|---|---|
| `.agents/skills/manju-audit/SKILL.md` | 更新 | `c7f6bfc2051198376e77449d4596989d018046b08b5293a8f660fe76543a559a` |
| `.agents/skills/manju-producer/SKILL.md` | 更新 | `80872fef5f508f77f3a5c414f1b82d101f60bf986fa528951bcd5333244c51c4` |
| `.agents/skills/manju-script/SKILL.md` | 更新 | `75aea18e84660e87d8a51e85ba5687527b68ff43acd107714d28fe433e0a1afa` |
| `.agents/skills/manju-shots/SKILL.md` | 更新 | `9a9991aa48e1065cf99a410815a243d733646201a42430a4ca81e6edec5a283a` |
| `.agents/skills/manju-story/SKILL.md` | 更新 | `649fddd04519c30acd6ca95b884a56cf5ac76e8fd3b913fcd49ac03a23ce0138` |
| `.agents/skills/manju-visual/SKILL.md` | 更新 | `77bfd26739d4b1b339de4b49d34fee913fc59302eb5b84a7f63858dbd5348b6d` |
| `.agents/skills/manju-voice/SKILL.md` | 更新 | `ee9811dce44786b6b3d84712b019cd82c1552875d386cf9ef333f4861220bcd9` |
| `00_source/README.md` | 更新 | `ee1ab63e2871ade6f1701500cd701d30e9d1324b4b36507a069a37847eda97e8` |
| `01_story/README.md` | 更新 | `ef2ed9b9bb34b9776bb1a7e83e84304ecbf6ee859fe6c8586d5013bd0993a077` |
| `02_scripts/README.md` | 更新 | `6238328c3e85ebf93d193388dd133827f2145f32898119752ee0015809a8548e` |
| `AGENTS.md` | 更新 | `b85dd6001590936e566b3e01553e09620e737d1045dec6119e0dbf1a07c84347` |
| `CAPABILITIES.md` | 更新 | `e5f0fa32ab949824b0bacaf2e46320960d7a9811896ec0797133dba45f49ce54` |
| `CHANGELOG.md` | 更新 | `d63ae650c780e165a0fc39337c30cd366913f329c32704be5c9772614ba8afb1` |
| `CHATGPT_PROJECT_INSTRUCTIONS.md` | 更新 | `6f02117ff05e0797318252edff6cc048d5f7f14789dc897091f7fd721521a7c8` |
| `HARNESS.md` | 更新 | `4d540b95da057d0c49bebea3128d874e07133f930f65c41f4389998874c5fba5` |
| `MIGRATION.md` | 更新 | `31db7034c6b2df7c586a8a762d45aa7fd1249eb6b6c3c7f22069d452022a75c6` |
| `PACKAGE_MANIFEST.json` | 更新 | `afc6ae03fc35cab573f0c320f7d703e959f5929d327ce2d7b19ca39f1ec5e46d` |
| `PROJECT.md` | 合并 | `1523aee99574095a8bfaa64e3e7b823a87c994cb886db83a4cdbd0b7dbf2fa30` |
| `PROMPT_LIBRARY.md` | 更新 | `7ab9f6dd52498d71b5da63732a858a896dcbca64947ce545be7569b5785400c6` |
| `README.md` | 更新 | `183cd45f1a98a8305f9fc832fdf931ab315aedef322b4ad198c611c66893764e` |
| `START_HERE.md` | 更新 | `548449254b721383886a173e95a2d7855731750331a7f576cbee8e10730acabe` |
| `STATE.md` | 合并 | `376c30298685f664ace150240dafa5e6e64702d0fd65334aebf8cea6a1f22d2c` |
| `VALIDATION.md` | 更新 | `a2b603e7ba12dabc26919ed052163ec4237348effac3d6252adb63ad4e099427` |
| `WORKFLOW_ENTRYPOINTS.md` | 新增 | `b9a85e5d51e6b421271c85734b978304983a71c0bfb5549ac465a8d1b89d4965` |
| `contracts/PRODUCTION.md` | 更新 | `a41d6be91266713fd0cd68a7202682b60fc27ff614d64d9e39d278c2b2c29052` |
| `docs/archive/MIGRATION_v1_v2.md` | 新增 | `ea28227258a9a1e68290cc19d965486dd6a0ffc0c9e64119f6eb41cac7f7de19` |
| `docs/archive/VALIDATION_v2.md` | 新增 | `fd72381cc86779809ba7a1f7d069e83961eaaa972ceb852db2b2461a73344284` |
| `prompts/README.md` | 新增 | `a85aeb065d09eea7a8243db39e51d960ed2e389c91ee1a14d144a94388f7cfed` |
| `prompts/entry_novel_direct.md` | 新增 | `fe12947deb7427a103c2d0c9b71914e7f0741aa96f9ef6206e1d223b6d717ac1` |
| `prompts/entry_original_script.md` | 新增 | `95861f31bd7deac39934e45e43ae7acc89f3b396bdb4912404adee175f9094ef` |
| `templates/line_sheet.json` | 新增 | `983f44b5de84dcc35af5425abb10f64f8105c379d074f291204c47dd21386934` |
| `templates/shot_fields.md` | 更新 | `61578ac3ef8716c44d5acff6f5b9017cfcf3960b36e5531ff01522fdb1208605` |
| `templates/source_packet.md` | 新增 | `93aa92c10f834cd22421210eb99b84d36289351702fad14327b9ff397b7e799a` |
| `tests/reports/v21_structure_check.json` | 新增 | `8eb07c6d978a26f9a7f55111ea1bc8fe1b4f59f279bb25997db698cc6893a94c` |
| `tests/unit_test_results.txt` | 更新 | `916118e4843ab7e7e4350817273a319b69850452ada96847cab3424f09cdd7b6` |

旧初始化报告保持不变：`07_reviews/setup_check_v01.md`，SHA-256：`9a9ab328aad597ceda0f8650b1af961293ce471d2ebd92c7ce7cb06504fb0784`。未改动的 79 个原有文件（78 个包文件和此报告）逐项复核通过。报告自身哈希在写入后计算，随最终核验输出。

## 费用、阻塞与交接

运行模式 plan；外部生成预算 CNY 0；生图、TTS、图生视频、ASR/自动对齐、音乐音效、口型同步、剪辑软件原生接口保持 unconfigured。EPUB 专用导入器未内置。未安装依赖、修改全局配置、调用媒体服务或渲染；外部生成费用 CNY 0，Codex 会话费用 unknown。

升级与离线检查无阻塞。GitHub 交付沿用用户此前授权的私有仓库 gandio12138/ai-video-studio；本报告随升级提交，实际提交号和推送结果以本轮交接为准。

唯一下一步：用户需要进入创作时选择 novel_direct 或 original_script 并提供对应输入；本轮不代选入口，不写故事或生成媒体。
