# 镜头数据约定 v1.0

JSON 是结构化主文件；Markdown 是便于阅读的副本。两者必须来自同一版本。不是 ComfyUI 工作流 JSON，也不是任何视频接口的请求体。

## 顶层
`schema_version`、`episode_id`、`status`（draft/approved）、`target_duration_s`、`duration_tolerance_s`、`speech_rate_assumption_chars_per_s`、`pause_allowance_s`、`shots`。
目标时长、语速与停顿是本项目可调整的工作假设，不是模型参数或行业标准。

## 每镜必填
| 字段 | 含义 |
|---|---|
| shot_id | 唯一镜号，如 EP01_SH001 |
| scene_id | 剧本场次，如 SC01 |
| source_refs | 字符串列表：来源文件与段落/剧本节拍；原创补充注明 |
| purpose | 本镜只承担的主要叙事任务 |
| framing | 远景 / 全景 / 中景 / 近景 / 特写 / 大特写 |
| angle | 平视、俯视、低机位等可执行描述 |
| camera_move | 固定、缓推、横移等；区分真实运镜和后期裁切 |
| action | 单镜可见动作，主体+动作+结果，不塞多个地点与跳时 |
| dialogue | 列表，每项 {speaker_id: C001, text: 台词}；无对白 [] |
| voiceover | 旁白，未使用为空字符串 |
| sfx | 音效说明，未使用为空字符串 |
| edit_duration_s | 剪辑采用秒数，正数 |
| generation_duration_s | 计划生成秒数；未选模型或纯静帧用 null |
| recorded_audio_duration_s | 本镜完整对白/旁白实际音频秒数；未录音用 null |
| asset_ids | 素材编号列表，须在 assets.json 存在，可为 planned |
| continuity_in | 人物/道具/位置/信息的镜头起始状态 |
| continuity_out | 结束状态，供下一镜接续 |
| production_method | 静帧运镜 / 图生视频 / 后期合成 / 实拍 |
| post_notes | 字幕、纸条文字等后期说明；没有则空字符串 |

## 示例镜头对象
```json
{
  "shot_id": "EP01_SH001",
  "scene_id": "SC01",
  "source_refs": ["02_scripts/EP01_v01.md#B01"],
  "purpose": "建立主角准备关店的处境",
  "framing": "中景",
  "angle": "平视",
  "camera_move": "静帧后期轻推",
  "action": "C001 将旧表放在柜台，手指仍搭在表边。",
  "dialogue": [],
  "voiceover": "",
  "sfx": "店内时钟声",
  "edit_duration_s": 5,
  "generation_duration_s": null,
  "recorded_audio_duration_s": null,
  "asset_ids": ["C001", "L001", "P001"],
  "continuity_in": "旧表在 C001 手中",
  "continuity_out": "旧表在柜台，C001 的手搭在表边",
  "production_method": "静帧运镜",
  "post_notes": ""
}
```

## 素材登记
assets.json 顶层为 `schema_version` 和 `assets` 列表。每项必填 `asset_id`、`kind`、`label`、`status`、`path`。kind 为 character / scene / prop / sound / music / voice / image / video；status 为 planned / generated / approved / rejected。尚未生成时 path 为 null。
`path` 相对于项目根目录；示例校验时，使用 examples/watch_note 作为根目录。禁止写密钥或项目外私人文件路径。

## 时间线与声音
时间线由 edit_duration_s 顺序累计，不让模型再写另一套可能矛盾的总数。若存在跨镜旁白/声音桥，在 post_notes 写清覆盖镜号；校验脚本只做逐镜串行粗估，不会自动理解跨镜混音。录音实测字段优先于字符估算。

## 校验脚本的边界
检查字段、类型、编号、时长总和、素材引用、已生成文件存在性、对白时长粗估。不能核验原文引用是否真的支持结论、空间/剧情是否合理、画面好不好看或是否拥有商用权。以上仍由 manju-audit 和人工确认处理。

## v2.1 双入口兼容字段
`source_refs` 在 A 引用原文与 source_packet，在 B 引用剧本节拍，不强制 02_scripts/EP01_vNN.md 存在。
对白对象可追加 `line_id`，旁白对应 `voiceover_line_ids` 列表；跨镜声音在 post_notes 写覆盖关系。逐句文本唯一采用源是 EP01_lines_vNN.json，镜头只引用同版内容。
原 v1 校验器仍只检查原有字段及逐镜时长粗估，不验证新台词引用、原文忠实度或跨镜去重；这些由 agent/audit 和人工核对。本次没有声称新增字段已获程序级校验。

## v2.3 视觉与补充交接（非新增程序校验）
source_refs可引用原文/source_packet/原创剧本以及补全台账CMP。可另加completion_refs、wardrobe_versions、visual_prompt_refs用于agent追踪；它们不是生成服务参数，原check_shots未增加对此的完整验证。
每镜需要完整关键帧提示词文件，正文不能用资产编号替代外观。动作/持物/视线/衣装湿破状态与接续表一致，B桥接计入时长；G1前在两个入口明示许可下均可draft试拆。

电影式视觉交接先读CINEMATIC_LOOK.md：记录实际光源、摄影位置/距离/透视/焦点、视线和接触遮挡。所需独立参考、身份/衣装/状态、场景LAYOUT及机位版本写在文字说明/sidecar；设定板仅显式需要时使用；实际路径未有则null。剧情关键帧为单幅，不把多格板直接作视频首帧。原JSON契约及校验能力不因这些说明改变。
