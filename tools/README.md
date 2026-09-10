# 本地工具使用
Python3.9+，标准库；渲染需要已经安装的 FFmpeg/ffprobe 与必需编码器/滤镜。不安装依赖、不联网、不读取密钥。
在项目根目录运行。命令中的 EP01 文件应替换为你实际已有版本，模板中的空素材不会通过校验。

## 环境、测试、媒体检查
```bash
python3 tools/studio.py doctor --root .
python3 -m unittest discover -s tests -v
python3 tools/studio.py probe 08_audio/takes/EP01_DL001_take01.wav --root .
python3 tools/studio.py hash 08_audio/takes/EP01_DL001_take01.wav --root .
```
doctor 检查工具和文件，不测试 Codex 是否已经加载 skills。probe 是技术媒体信息，不是听检/剧情判断。

## 结构与真实文件
```bash
python3 tools/studio.py validate timeline 10_edit/timelines/EP01_v01.json --root .
python3 tools/studio.py validate timeline 10_edit/timelines/EP01_v01.json --root . --check-files
python3 tools/studio.py validate job 12_runs/jobs/EP01_JOB_001.json --root . --check-files
```
不加 check-files 只检查结构/路径形式/部分状态；加上才检查真实存在、哈希与相关媒体流/时长。job 检查不核算全批次账单、不执行状态机、不证明用户批准不可伪造。

## 实际对齐 → SRT
```bash
python3 tools/studio.py hash 10_edit/timelines/EP01_v01.json --kind timing --root .
python3 tools/studio.py srt 08_audio/alignment/EP01_v01.json --timeline 10_edit/timelines/EP01_v01.json --output 08_audio/alignment/EP01_v01.srt --root .
```
第一条是当前时序指纹。对齐真实音频并复核之后才能填写；不可单改指纹以绕过 stale。
SRT 导出器不做 ASR/强制对齐。估算/草稿、重复cue、重叠、越界或指向未采用音频会失败。

## 本地粗剪
```bash
python3 tools/studio.py render 10_edit/timelines/EP01_v01.json --output 11_exports/previews/EP01_v01.mp4 --root .
```
默认只检查真实输入与工具，返回计划，不渲染。确认后：
```bash
python3 tools/studio.py render 10_edit/timelines/EP01_v01.json --output 11_exports/previews/EP01_v01.mp4 --root . --execute
```
输出 MP4 和 `.render.json`；外挂字幕模式还输出同名 SRT。重复文件/报告会被拒绝，请递增版本。
中间文件在本次输出目录的 `.render_*` 暂存，完成/失败后清理本轮临时文件；只保留本轮结果/失败报告，不删原件。
支持单画面轨连续硬切、静帧保持、源片段裁切、contain/cover；音轨定位/固定增益/淡入淡出/相加限幅；外挂或软字幕。原视频声音默认丢弃，需要时显式作为音轨引用。
不支持静帧运镜、叠画、转场、变速、自动ducking、烧录字幕、NLE工程导出。遇到不支持字段会拒绝，不静默渲染成另一种效果。
基础限幅不是最终LUFS/真峰值验收。音频采用区间只容許最多一帧量化差；不要用尾部补静音掩盖对白缺失。完整解码也不等于视听质量检查。

## 可选：合成素材集成测试
下面会真的生成几个4秒测试视频，但只有纯色/测试图形和测试音，没有真人或模型配音，不调用云端。使用全新空目录：
```bash
python3 tools/smoke_test.py --root /tmp/manju-v2-smoke
```
如果目录已存在且非空，换一个新名字，不删除未知文件。测试覆盖 dry-run、裁切/硬切、声轨定位、外挂/软字幕、静音行为、完整解码和不覆盖，以及切点前后像素变化/音量入点。
本次结果见 tests/reports。没有在你的Mac、你的Codex或任何付费供应商上验证；先运行 doctor 再用一小段真实素材试做。
