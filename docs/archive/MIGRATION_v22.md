# 升级到v2.2：保留已有作品，只合并规则与新模板

新项目可以用完整包；已有作品使用ai-manju-v2.2-update更新包，让Codex先读APPLY_WITH_CODEX.md，比较并提出合并计划，用户确认后再改。

不得用新PROJECT.md/STATE.md初始化内容覆盖真实状态，不覆盖00_source、剧本、分镜、assets.json、媒体、.env、provider/runtime/delivery配置或批准记录。MERGE_ONLY中的两份文件仅提供新增设置/进度行示例；保留原值，只添加缺少字段。

重点合并：AGENTS/WORKFLOW_ENTRYPOINTS/VISUAL_PRODUCTION、producer/enrich/story/script/audit/shots/visual/prompts、两个完整入口和complete_visual_pack、详细模板。改掉旧“A不允许任何桥接”“B首轮剧本后必须停”“视觉缺细节全等确认”“只接受已确认视觉才写提示词”等冲突，不保留互相打架的规则。

不改变原工具后端和严格JSON契约；新补全/视觉字段是文字工作约定。保留已有主角色/场景/声音与剧情批准，新草案不能自动替换。当前项目已到后期也不要重跑前期，只对指定缺口补稿。

核对十五个技能、三个入口文件和共同规范存在；检查当前两路完整批次都有视觉交付、A/B草稿补全、C核心边界、参考条件与无媒体默认权限。最后报告实际改动/冲突和未改文件。示例不得自动当作用户故事。
