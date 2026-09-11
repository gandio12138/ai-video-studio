# 生成提示词文档清理报告 v01

完成时间：2026-09-11T15:49:07.415847+08:00
状态：已清除工作目录中的106份作品提示词及相关索引；当前可用提示词为0。

## 清理范围

- 05_prompts：103份（101份Markdown、2份JSON），含人物、场景、道具、62镜正文、设定板、编辑预案、三条校准稿及其索引。README和目录结构保留。
- 04_visual/locations/L001_layout_v01.md：1份布局绘制提示词。既有场景卡L001_v03及其固定空间设计保留。
- 06_assets/references/C001：2份历史.prompt.txt文件；对应图片保留。长期规范下的原样例副本不在清理范围。

## 恢复与验证

- 恢复包：[prompt_documents_cleanup_v01.zip](/Users/chengchengxu/Desktop/ai-video-studio/12_runs/archives/prompt_documents_cleanup_v01.zip)
- SHA-256：`65783eeee55b9b549cf89f61bafe73b4820cace9e0b04d28daf09e8b3c299d49`；逐文件解压数据哈希及ZIP CRC已验证。
- 归档包含106份原文档和清理前PROJECT/STATE恢复副本；是恢复备份，不是当前采用提示词，不自动加载或恢复。Git历史与既有备份不清除。
- 清单、分类、原哈希及历史版本上限：[prompt_documents_cleanup_v01.json](/Users/chengchengxu/Desktop/ai-video-studio/12_runs/prompt_documents_cleanup_v01.json)
- 除清理目标及PROJECT/STATE必要状态更新，其余268份已有文件哈希不变；无额外删除或修改。

## 保留项目

harness根规范、技能、prompts入口、templates、examples、PROMPT_AUTHORING_STANDARD.md、references/prompt_authoring原始样例及更新包完整保留。原小说、事实/台词、剧本制作依据、分镜、CMP台账、人物/场景/道具卡、板规格与映射、实际图片、服务配置、旧批准和执行/验收记录保留。
历史执行日志中的实际提交正文保留作追溯，不是活动提示词文档，不可在后续任务中自动恢复使用。未销毁审计证据。

## 状态与引用

仅更新PROJECT.md与STATE.md：当前活动提示词为0；旧分镜、卡片、报告中的被清理路径标为历史失效引用，不再代表正文就绪。历史进度不改写成从未发生，G1/G2和既有候选图状态不变。未来用户要求重写时按长期规范，先查清单的历史版本上限再递增；本轮没有重建。

## 实际移除文件

| 原路径 | 类别 | 字节数 |
|---|---|---|
| `04_visual/locations/L001_layout_v01.md` | 布局绘制提示词 | 3507 |
| `05_prompts/C001_design_v01.md` | 作品提示词/索引 | 2867 |
| `05_prompts/C002_design_v01.md` | 作品提示词/索引 | 2871 |
| `05_prompts/C003_design_v01.md` | 作品提示词/索引 | 2989 |
| `05_prompts/C004_design_v01.md` | 作品提示词/索引 | 2725 |
| `05_prompts/C005_design_v01.md` | 作品提示词/索引 | 3002 |
| `05_prompts/EP01_character_tryout_v01.md` | 作品提示词/索引 | 4713 |
| `05_prompts/EP01_prompt_index_v01.md` | 作品提示词/索引 | 2146 |
| `05_prompts/EP01_visual_pack_index_v01.json` | 作品提示词/索引 | 106427 |
| `05_prompts/EP01_visual_pack_index_v01.md` | 作品提示词/索引 | 35188 |
| `05_prompts/EP01_visual_pack_index_v02.json` | 作品提示词/索引 | 419623 |
| `05_prompts/EP01_visual_pack_index_v02.md` | 作品提示词/索引 | 7330 |
| `05_prompts/L001_scene_v01.md` | 作品提示词/索引 | 3206 |
| `05_prompts/P001_stone_v01.md` | 作品提示词/索引 | 1835 |
| `05_prompts/calibration/C001_cinematic_v01.md` | 作品提示词/索引 | 3543 |
| `05_prompts/calibration/EP01_SH012_cinematic_v01.md` | 作品提示词/索引 | 5421 |
| `05_prompts/calibration/L001_cinematic_v01.md` | 作品提示词/索引 | 3751 |
| `05_prompts/characters/C001_v02.md` | 作品提示词/索引 | 16306 |
| `05_prompts/characters/C001_v03.md` | 作品提示词/索引 | 43447 |
| `05_prompts/characters/C002_v02.md` | 作品提示词/索引 | 16522 |
| `05_prompts/characters/C002_v03.md` | 作品提示词/索引 | 44454 |
| `05_prompts/characters/C003_v02.md` | 作品提示词/索引 | 17136 |
| `05_prompts/characters/C003_v03.md` | 作品提示词/索引 | 45157 |
| `05_prompts/characters/C004_v02.md` | 作品提示词/索引 | 15587 |
| `05_prompts/characters/C004_v03.md` | 作品提示词/索引 | 37373 |
| `05_prompts/characters/C005_G1_v03.md` | 作品提示词/索引 | 37469 |
| `05_prompts/characters/C005_G2_v03.md` | 作品提示词/索引 | 37847 |
| `05_prompts/characters/C005_G3_v03.md` | 作品提示词/索引 | 38001 |
| `05_prompts/characters/C005_v02.md` | 作品提示词/索引 | 18201 |
| `05_prompts/edits/EP01_edit_recipes_v01.md` | 作品提示词/索引 | 5458 |
| `05_prompts/edits/EP01_sheet_edit_recipes_v01.md` | 作品提示词/索引 | 4129 |
| `05_prompts/locations/L001_v02.md` | 作品提示词/索引 | 7699 |
| `05_prompts/locations/L001_v03.md` | 作品提示词/索引 | 18778 |
| `05_prompts/props/P001_v02.md` | 作品提示词/索引 | 2311 |
| `05_prompts/sheets/characters/C001_sheet_v01.md` | 作品提示词/索引 | 6849 |
| `05_prompts/sheets/characters/C002_sheet_v01.md` | 作品提示词/索引 | 6648 |
| `05_prompts/sheets/characters/C003_sheet_v01.md` | 作品提示词/索引 | 6988 |
| `05_prompts/sheets/characters/C004_sheet_v01.md` | 作品提示词/索引 | 6237 |
| `05_prompts/sheets/characters/C005_G1_sheet_v01.md` | 作品提示词/索引 | 6102 |
| `05_prompts/sheets/characters/C005_G2_sheet_v01.md` | 作品提示词/索引 | 6195 |
| `05_prompts/sheets/characters/C005_G3_sheet_v01.md` | 作品提示词/索引 | 6315 |
| `05_prompts/sheets/locations/L001_sheet_v01.md` | 作品提示词/索引 | 4864 |
| `05_prompts/shots/EP01_SH001_v02.md` | 作品提示词/索引 | 3081 |
| `05_prompts/shots/EP01_SH002_v02.md` | 作品提示词/索引 | 3084 |
| `05_prompts/shots/EP01_SH003_v02.md` | 作品提示词/索引 | 3643 |
| `05_prompts/shots/EP01_SH004_v02.md` | 作品提示词/索引 | 5247 |
| `05_prompts/shots/EP01_SH005_v02.md` | 作品提示词/索引 | 3272 |
| `05_prompts/shots/EP01_SH006_v02.md` | 作品提示词/索引 | 3083 |
| `05_prompts/shots/EP01_SH007_v02.md` | 作品提示词/索引 | 3367 |
| `05_prompts/shots/EP01_SH008_v02.md` | 作品提示词/索引 | 3169 |
| `05_prompts/shots/EP01_SH009_v02.md` | 作品提示词/索引 | 3080 |
| `05_prompts/shots/EP01_SH010_v02.md` | 作品提示词/索引 | 3281 |
| `05_prompts/shots/EP01_SH011_v02.md` | 作品提示词/索引 | 3893 |
| `05_prompts/shots/EP01_SH012_v02.md` | 作品提示词/索引 | 4213 |
| `05_prompts/shots/EP01_SH013_v02.md` | 作品提示词/索引 | 3866 |
| `05_prompts/shots/EP01_SH014_v02.md` | 作品提示词/索引 | 3343 |
| `05_prompts/shots/EP01_SH015_v02.md` | 作品提示词/索引 | 4649 |
| `05_prompts/shots/EP01_SH016_v02.md` | 作品提示词/索引 | 3395 |
| `05_prompts/shots/EP01_SH017_v02.md` | 作品提示词/索引 | 3429 |
| `05_prompts/shots/EP01_SH018_v02.md` | 作品提示词/索引 | 3650 |
| `05_prompts/shots/EP01_SH019_v02.md` | 作品提示词/索引 | 3218 |
| `05_prompts/shots/EP01_SH020_v02.md` | 作品提示词/索引 | 3997 |
| `05_prompts/shots/EP01_SH021_v02.md` | 作品提示词/索引 | 3804 |
| `05_prompts/shots/EP01_SH022_v02.md` | 作品提示词/索引 | 4296 |
| `05_prompts/shots/EP01_SH023_v02.md` | 作品提示词/索引 | 3194 |
| `05_prompts/shots/EP01_SH024_v02.md` | 作品提示词/索引 | 4278 |
| `05_prompts/shots/EP01_SH025_v02.md` | 作品提示词/索引 | 3187 |
| `05_prompts/shots/EP01_SH026_v02.md` | 作品提示词/索引 | 3687 |
| `05_prompts/shots/EP01_SH027_v02.md` | 作品提示词/索引 | 4604 |
| `05_prompts/shots/EP01_SH028_v02.md` | 作品提示词/索引 | 3233 |
| `05_prompts/shots/EP01_SH029_v02.md` | 作品提示词/索引 | 3130 |
| `05_prompts/shots/EP01_SH030_v02.md` | 作品提示词/索引 | 3268 |
| `05_prompts/shots/EP01_SH031_v02.md` | 作品提示词/索引 | 3287 |
| `05_prompts/shots/EP01_SH032_v02.md` | 作品提示词/索引 | 3245 |
| `05_prompts/shots/EP01_SH033_v02.md` | 作品提示词/索引 | 3081 |
| `05_prompts/shots/EP01_SH034_v02.md` | 作品提示词/索引 | 4242 |
| `05_prompts/shots/EP01_SH035_v02.md` | 作品提示词/索引 | 3862 |
| `05_prompts/shots/EP01_SH036_v02.md` | 作品提示词/索引 | 3206 |
| `05_prompts/shots/EP01_SH037_v02.md` | 作品提示词/索引 | 3346 |
| `05_prompts/shots/EP01_SH038_v02.md` | 作品提示词/索引 | 4249 |
| `05_prompts/shots/EP01_SH039_v02.md` | 作品提示词/索引 | 3247 |
| `05_prompts/shots/EP01_SH040_v02.md` | 作品提示词/索引 | 3452 |
| `05_prompts/shots/EP01_SH041_v02.md` | 作品提示词/索引 | 3121 |
| `05_prompts/shots/EP01_SH042_v02.md` | 作品提示词/索引 | 5320 |
| `05_prompts/shots/EP01_SH043_v02.md` | 作品提示词/索引 | 3983 |
| `05_prompts/shots/EP01_SH044_v02.md` | 作品提示词/索引 | 3162 |
| `05_prompts/shots/EP01_SH045_v02.md` | 作品提示词/索引 | 3517 |
| `05_prompts/shots/EP01_SH046_v02.md` | 作品提示词/索引 | 4180 |
| `05_prompts/shots/EP01_SH047_v02.md` | 作品提示词/索引 | 3624 |
| `05_prompts/shots/EP01_SH048_v02.md` | 作品提示词/索引 | 4163 |
| `05_prompts/shots/EP01_SH049_v02.md` | 作品提示词/索引 | 3233 |
| `05_prompts/shots/EP01_SH050_v02.md` | 作品提示词/索引 | 3292 |
| `05_prompts/shots/EP01_SH051_v02.md` | 作品提示词/索引 | 5298 |
| `05_prompts/shots/EP01_SH052_v02.md` | 作品提示词/索引 | 3685 |
| `05_prompts/shots/EP01_SH053_v02.md` | 作品提示词/索引 | 3468 |
| `05_prompts/shots/EP01_SH054_v02.md` | 作品提示词/索引 | 3466 |
| `05_prompts/shots/EP01_SH055_v02.md` | 作品提示词/索引 | 3477 |
| `05_prompts/shots/EP01_SH056_v02.md` | 作品提示词/索引 | 3496 |
| `05_prompts/shots/EP01_SH057_v02.md` | 作品提示词/索引 | 3475 |
| `05_prompts/shots/EP01_SH058_v02.md` | 作品提示词/索引 | 3209 |
| `05_prompts/shots/EP01_SH059_v02.md` | 作品提示词/索引 | 3455 |
| `05_prompts/shots/EP01_SH060_v02.md` | 作品提示词/索引 | 4697 |
| `05_prompts/shots/EP01_SH061_v02.md` | 作品提示词/索引 | 4202 |
| `05_prompts/shots/EP01_SH062_v02.md` | 作品提示词/索引 | 5409 |
| `06_assets/references/C001/C001_V02_CHARACTER_SHEET.prompt.txt` | 素材旁历史提示词 | 14042 |
| `06_assets/references/C001/C001_V03_FRONT.prompt.txt` | 素材旁历史提示词 | 7285 |

## 执行边界

本轮未生成图片/声音/视频、未渲染、未安装依赖、未调用付费接口、未修改全局配置、未提交或推送Git。费用CNY 0。配音、视频、自动对齐、NLE及项目云端接口保持原unconfigured状态。
仅做文件范围、归档完整性与保留哈希检查；无须运行媒体或创作测试。下一步等待用户指定新的提示词任务。
