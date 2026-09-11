# v2.3验证范围与本机检查索引

本次合并采用本机实际执行结果，见07_reviews/upgrade_v2_3_v01.md。原v2.2说明归档为docs/archive/VALIDATION_v22.md，原测试与媒体报告保持原样。

## 本机检查
- 单元测试与新增14项设定板静态检查：tests/unit_test_results_v23_local_v01.txt。
- Python/FFmpeg/ffprobe及十五技能探测：tests/reports/doctor_v23_local_v01.json。
- 合并范围、原文件保留、四入口交接和引用/哈希核对：tests/reports/v23_merge_checks_local_v01.json。
执行状态和结果以这些实际文件及维护报告为准；仅有规范或测试文件不算检查通过。

## 更新包历史材料
历史说明为ai-manju-v2.3-update/FILES/VALIDATION.md；原始报告均在该更新包的FILES目录下：tests/unit_test_results_v23.txt、tests/reports/doctor_v23.json、tests/reports/v23_structure_check.json。它们记录的是更新包制作环境，保留在更新目录，不复制成当前项目测试结果，不把其中70项、149项或Linux探测报告当作本机证据。

## 能证明与不能证明的内容
新增测试核对静态规范、技能元数据、入口引用、PNG头部尺寸/哈希与教学示例文本；不是让Codex实际创作的端到端测试，也不证明人物适配、审美、原文忠实度或真实图片一致性。测试中的examples仅教学/测试资料，不作为正式故事。
skill-creator附带的quick_validate.py因本机缺少PyYAML未能运行；未安装依赖。另用Python标准库核对本项目实际使用的简单name/description元数据、命名和占位，结果并入本机合并检查记录；不声称通用YAML校验器通过。
本次不运行媒体渲染集成测试，不生成/编辑/裁图/拼版，不调用声音、视频或外部API。实际生图、拼版、配音、视频、自动对齐及NLE服务仍unconfigured；FFmpeg既有基础工具能力不变。
