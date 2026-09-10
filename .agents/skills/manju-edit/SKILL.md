---
name: manju-edit
description: "用于把实际图像/视频/声音剪成粗剪，生成中立 timeline 并调用已实现后端；没有原生工程适配器时不承诺剪映/Final Cut/Resolve 项目。"
---

# 可重建时间线与本地剪辑

先遵守根目录 AGENTS.md；路径相对项目根目录。


## 输入
已确认镜头、真实素材和 SHA-256、实测配音、对齐字幕、剪辑范围授权。读 templates/timeline.json、contracts/PRODUCTION.md、CAPABILITIES.md。
## 步骤
1. 根据真实对白与节奏建时间线，视频帧计时、源入点毫秒；保留 shot_id、asset_id、path、sha256。不能把 planned 资产当实际输入。
2. 先做可重建的低分辨率有声分镜/粗剪，反馈修改最小范围。当前后端支持单画面轨顺序硬切、静帧保持、片段裁切、contain/cover、多音轨定位/固定增益/淡变、外挂或软字幕。
3. 运镜、叠画、转场、速度变化、自动 ducking、烧录字幕、原生工程目前不能直接渲染。按需求选择扩展适配器或经用户同意简化，不静默忽略。
4. 默认保留原片只读，默认不混入视频原声；需要原声时提取/显式作为 audio 条目。检查重叠对白与跨镜声音桥，不把它们强行逐镜裁断。
5. 先 `python3 tools/studio.py validate timeline ... --check-files --root .`，然后 `python3 tools/studio.py render ... --output 11_exports/previews/EP01_vNN.mp4 --root .`。默认只预检/计划。
6. 用户确认本地渲染范围后，同命令加 `--execute`。依赖缺失只报告，不自行安装。不同版本输出，不覆盖已有成片。
7. 根据真正生成的文件与报告记录 render_success；目检/听检独立。粗剪确认后再另定发布规格，不能把 smoke test 当作品验收。
## 输出
10_edit/timelines/EP01_vNN.json、11_exports/previews 实际视频与 render.json、修改单。缺失素材时只交时间线草稿+阻塞。
