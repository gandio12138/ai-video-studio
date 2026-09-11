# 完整生图提示词
先读PROMPT_AUTHORING_STANDARD.md并按本轮类型写完整正文；简短任务、新角色、新场景、后续集数都适用，样例只传递方法。
characters/：身份/衣装主参考及当前需要的全身/角度/表情；locations/：固定空间主参考及需要的反向/交互区；props/：关键道具；shots/：当前每镜独立正文；edits/：与主生成分文件的局部修正，未有底图/问题时标条件式预案。单项请求不扩大为全包。
每条独立可复制，不只写编号/同上。缺参考填null和前置条件，不省略文本。总索引用templates/visual_pack_index.md；检查全部当前镜头，不能仅头两镜示例。默认只文字，不调用生成。

v2.3新增sheets/characters与sheets/locations：整板探索提示词与逐格映射。独立panel正文仍写characters/locations，shot正文仍写shots；单图与镜头不得带板的边框标签。见DESIGN_SHEETS.md。
