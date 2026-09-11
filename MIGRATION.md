# 当前迁移｜电影式视觉纠偏

本次按cinematic-look-fix/APPLY_WITH_CODEX.md执行：先比较计划，确认后备份受影响规则；当前本地文件与包内v2.3基线不同，采用语义合并，不强制套补丁、不初始化覆盖作品。
主规范CINEMATIC_LOOK.md接到AGENTS/双入口/complete_visual_pack/相关技能/模板/导航；完整入口full_pack，纠偏rebuild_cinematic_visuals默认calibrate_only。设定板仅显式要求时启用DESIGN_SHEETS.md和complete_design_sheets，不新增不存在的ASSET_SHEETS或asset_reference_sheets别名。
人物适配、A/B补全、固定布局、逐镜完整正文与版本/参考真实性必须保留。旧插画媒介目标与新电影式目标冲突时保留旧稿，在STATE列受影响版本待重建；维护轮不开始作品创作。
PROJECT只合并当前look_mode/asset_sheet_mode和真实状态；STATE更新索引并保留历史。故事、台词、分镜、视觉卡、媒体、config、.env、资产登记、批准与旧日志不覆盖；配音/剪辑接口与工具代码不改。
检验两入口均走新规则、optional板面不阻塞电影式任务、full_pack每镜完整、校准三类不冒充整集、引用路径有效；核对原文件哈希和后端原检查。人读字段不塞进严格JSON；媒体权限保持0，缺接口unconfigured。维护报告写新版本后停止。

## 以下为历史v2.2→v2.3设定板迁移记录
历史板面强制要求仅说明当时迁移，当前任务以本页上方电影式规则为准，不据此恢复默认强制板面。

# v2.2 → v2.3合并指南

本更新基于v2.2。老于v2.2的项目先补v2.2基础或逐项核对VISUAL_PRODUCTION/manju-enrich等前置，不把缺失文件当已存在。新项目可用完整版；已有项目使用更新包，由Codex比较后等用户确认再合并。

必须保留：00_source、实际剧本/台词/镜头/视觉卡、所有媒体、assets.json、PROJECT/STATE真实记录、.env、config、批准、任务与日志。MERGE_ONLY提供新字段参考，不覆盖真实文件。

必须同步：DESIGN_SHEETS、AGENTS、两个入口与complete_visual_pack、新complete_design_sheets、producer/visual/prompts/images/shots/video/audit、设计模板与索引。旧“五类/三类”保留为基础，不再误当完整上限；独立图禁止多格只限制单图，不能被当作禁止展示板。

更新包版式参考原文件复制到新的layout子目录并如实登记来源；同名不同哈希先停止或改新版本，不覆盖。原图只layout参考，不写入正式角色资产，不替代用户商业授权。

本版不改工具代码或严格JSON/配置，不给不存在的拼版接口新增假的enabled=true。新manifest是人读说明，不直接传给旧校验器。纯文字更新不等于媒体执行许可。

应用后核对十五个skills以及两路都引用DESIGN_SHEETS；实际引用的新增文件存在；角色与场景整板/分格/布局/manifest齐全；继续保留每镜单幅提示词。harness更新在离线检查与维护报告后结束，不自动初始化/重置作品或补创作。之后只有用户另轮明确要求补设定板时，才按指定范围调用complete_design_sheets；不重做全书。
