# 专利检索查询集（M1）

## 1. 检索目标
- 覆盖地区：`CN + US + WO`
- 覆盖主题：双模型/多模型分歧检测、结构化解耦、证据裁决、融合生成、可解释输出。
- 检索来源：Google Patents、WIPO Patentscope、Espacenet、CNIPA 公布信息入口。

## 2. 中文查询（建议组合）
- `("大语言模型" OR "LLM") AND ("分歧检测" OR "矛盾检测" OR "一致性校验") AND ("结构化解耦" OR "子问题分解")`
- `("双模型" OR "多模型") AND ("自动裁决" OR "证据聚合" OR "融合回答")`
- `("论点单元" OR "语义单元") AND ("对齐匹配" OR "蕴含矛盾判定")`
- `("可解释生成" OR "可追溯输出") AND ("大模型" OR "问答系统")`
- `("分歧图谱" OR "冲突图") AND ("最小冲突集" OR "MUS")`

## 3. 英文查询（建议组合）
- `"LLM disagreement detection" AND ("structured decomposition" OR "decoupling") patent`
- `"multi-model contradiction detection" AND ("alignment" OR "entailment") patent`
- `"LLM-as-a-judge" AND ("evidence retrieval" OR "evidence aggregation") patent`
- `"argument graph" AND ("conflict set" OR "minimal unsat subset") patent`
- `"answer fusion" AND ("provenance" OR "traceable output") AND patent`

## 4. 渠道定向检索语法
- Google Patents：`site:patents.google.com <query>`
- WIPO：`site:patentscope.wipo.int <query>`
- Espacenet：`site:worldwide.espacenet.com <query>`
- CN：`site:pss-system.cponline.cnipa.gov.cn <query>`

## 5. 初筛规则（用于 Top20）
- 时间优先：近 8 年优先，但保留关键早期基础专利。
- 文献质量：优先有完整权利要求文本和法律状态信息。
- 相似性维度：
  - 是否包含“双模型或多模型输出比较”
  - 是否包含“矛盾/蕴含判定”
  - 是否包含“证据检索/裁决”
  - 是否包含“融合输出与可解释追溯”
- 排除项：
  - 仅通用打分/投票且不涉及结构化分歧解耦
  - 仅业务规则引擎，不含可执行技术流程

## 6. Top5 深读筛选规则
- 必须覆盖至少一个核心环节：分歧识别、子问题裁决、证据回填、融合输出。
- 与拟申请方案的独立权利要求特征重叠度高于中等水平。
- 可形成清晰的“规避式改写”路径。

## 7. 检索产出文件映射
- `patent_cn/01_prior_art/patent_list_top20.md`
- `patent_cn/01_prior_art/closest5_claim_chart.xlsx`
- `patent_cn/01_prior_art/novelty_strategy.md`

