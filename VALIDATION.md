# v2.1 验证记录｜2026-09-10

## 本轮实际执行
- 在本次容器重跑 `python -m unittest discover -s tests -v`，原有56项测试通过；详见 tests/unit_test_results.txt。
- 确认十四个技能文件存在，并检查 name/description 元数据；解析现有 JSON 文件；核对双入口提示词、路由和制作依据/台词模板存在。
- 对比上传的 v2 压缩包，tools/ 的所有后端文件逐字节未变。
- 默认 plan、外部生成未授权、预算0保持不变。
- 结构检查结果见 tests/reports/v21_structure_check.json；PACKAGE_MANIFEST.json 记录本包文件哈希。

## 本轮没有执行
没有调用 Codex CLI 做真实路由测试，没有访问用户 Mac，没有导入实际小说，没有生成剧本/图像/声音/视频，没有调用云端 API，没有新实现 EPUB 导入器，没有重跑 FFmpeg 渲染。
56项单元测试验证的是原有镜头/媒体数据后端，不是本次自然语言入口会被模型百分之百遵循。新 line_sheet 模板没有新增完整程序级校验器；原文忠实度、台词一致性和 G1 人工确认仍需真实任务验证。

## 继承记录
v2 的原验证说明保存在 docs/archive/VALIDATION_v2.md；tests/reports/smoke_summary.json 是随 v2 继承的合成媒体测试报告，不是本轮再次完成的渲染。旧原文/教学样例也不代表用户项目。

## 本次改动范围
新增两种入口指令、分流规则、source_packet/line_sheet 模板，调整前后期交接与文档；保留十四个技能、运行时和媒体后端。项目中的权限/批准是协作约定，不是系统沙箱或不可绕过的预算机制。
