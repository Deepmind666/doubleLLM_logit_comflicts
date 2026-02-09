# Top20 相关专利清单（M1）

> 检索日期：2026-02-09  
> 检索来源：Google Patents（覆盖 CN / US / WO）

| # | 公开号 | 标题 | 申请人/权利人 | 公开日 | 核心权利要求点（改写） | 与本方案相似点 | 初步规避策略 | 链接 |
|---:|---|---|---|---|---|---|---|---|
| 1 | US20250200392A1 | Large language model verification | Cx360, Inc. | 2025-06-19 | 将第一LLM输出转换为逻辑表示并由第二模型执行一致性校验。 | 高：双模型+一致性验证主链路接近。 | 独权加入“分歧图谱+最小冲突集+子问题裁决记录”。 | [Link](https://patents.google.com/patent/US20250200392A1/en) |
| 2 | WO2025128894A1 | Large language model verification | AIble Inc. | 2025-06-19 | 与US同族，PCT路径覆盖逻辑化验证与结果修正。 | 高：国际布局与核心链路接近。 | 将逻辑映射写为可选分支，主链路强调分歧解耦。 | [Link](https://patents.google.com/patent/WO2025128894A1/en) |
| 3 | US12353469B1 | Verification and citation for language model outputs | Autodesk, Inc. | 2025-07-08 | 结构化查询+检索+答案生成+证据引用验证。 | 高：证据裁决与可追溯输出接近。 | 限定为“分歧点级局部裁决”，非文档级统一引用。 | [Link](https://patents.google.com/patent/US12353469B1/en) |
| 4 | US20250077777A1 | Semantic aware hallucination detection for large language models | Bitvore Corp. | 2025-03-06 | 通过语义感知流程识别LLM幻觉并触发纠偏。 | 中高：与分歧识别阶段局部相似。 | 增加“分歧点->子问题树->裁决记录”完整链路。 | [Link](https://patents.google.com/patent/US20250077777A1/en) |
| 5 | US20250094866A1 | Responding to hallucinations in generative large language models | Unlikely Artificial Intelligence Limited | 2025-03-20 | 对输出片段执行幻觉识别与替换/重写。 | 中高：分歧片段级处理相邻。 | 主张“多解保留+结构化融合输出”，避免单一重写路径。 | [Link](https://patents.google.com/patent/US20250094866A1/en) |
| 6 | WO2025059626A1 | Responding to hallucinations in generative large language models | 浙江蚂蚁密算科技有限公司 | 2025-03-20 | 与US20250094866A1同族，覆盖国际申请。 | 中高：国际同族覆盖。 | 增加“证据优先级队列+信息增益调度”。 | [Link](https://patents.google.com/patent/WO2025059626A1/en) |
| 7 | US20240419912A1 | Detecting hallucination in a language model | T-Mobile Innovations Llc | 2024-12-19 | 评估one-shot/few-shot上下文中的幻觉概率。 | 中：检测导向，未覆盖分歧解耦。 | 明确“对齐匹配M+四分类判定+子问题化”。 | [Link](https://patents.google.com/patent/US20240419912A1/en) |
| 8 | US20240394512A1 | Hallucination Detection | Promoted.ai, Inc. | 2024-11-28 | 通过追加提示识别输出中的不受支持陈述。 | 中：检测机制相关。 | 加入provenance字段与审计日志结构。 | [Link](https://patents.google.com/patent/US20240394512A1/en) |
| 9 | US20240378400A1 | Hallucination prevention for natural language insights | Noblis, Inc. | 2024-11-14 | 基于模板事实对生成洞察进行一致性校验。 | 中：事实一致性路径相邻。 | 采用论点单元图而非模板事实引擎。 | [Link](https://patents.google.com/patent/US20240378400A1/en) |
| 10 | US20250165890A1 | Automated software development workflows via multi-agent computational framework | Sap Se | 2025-05-22 | 多Agent角色协同，含评审代理与反馈迭代。 | 中：迭代收敛思想接近。 | 限定“同题双模型分歧解耦”应用边界。 | [Link](https://patents.google.com/patent/US20250165890A1/en) |
| 11 | WO2024243265A1 | Generative artificial intelligence | 四川乐为科技有限公司 | 2024-11-28 | 对生成式AI施加约束集限制输出域。 | 中：约束生成相邻。 | 将约束限定到“子问题可验证性约束”。 | [Link](https://patents.google.com/patent/WO2024243265A1/en) |
| 12 | WO2024254203A2 | Value-based large language model teaming | Intuit Inc. | 2024-12-12 | Creator/Editor 双模型协同编辑与筛选。 | 中：双角色LLM协同接近。 | 主张事实一致性裁决，不主张价值偏好编辑。 | [Link](https://patents.google.com/patent/WO2024254203A2/en) |
| 13 | CN119493841A | Hallucination Detection and Handling for Domain-Specific Dialogue Systems Based on Large Language Models | Robert Bosch Gmbh | 2025-02-21 | 领域对话系统中的幻觉检测与处置流程。 | 中高：国内同向布局。 | 强化“分歧映射表+最小冲突集”差异。 | [Link](https://patents.google.com/patent/CN119493841A/en) |
| 14 | CN119961628A | Model hallucination detection method and device, storage medium and electronic device | 浙江蚂蚁密算科技有限公司 | 2025-05-09 | 幻觉检测方法/装置/介质一体化布局。 | 中高：与四件套布局相邻。 | 加入资源受限调度、停止条件和分歧类型多级分类。 | [Link](https://patents.google.com/patent/CN119961628A/en) |
| 15 | CN117931983A | A method and system for generating accurate answers using a large model | 中科星图数字地球合肥有限公司 | 2024-04-26 | 检索增强并校验回答准确性。 | 中：与证据引导部分相邻。 | 独权不走单模型RAG路径，突出双模型分歧裁决。 | [Link](https://patents.google.com/patent/CN117931983A/en) |
| 16 | CN117216205A | Method, device, system and medium for constructing question-answer library by large language model | 湖北公众信息产业有限责任公司 | 2023-12-12 | 构建问答库并进行质量筛选。 | 中低：偏离在线分歧裁决。 | 限定在线推理融合，不覆盖知识库构建主流程。 | [Link](https://patents.google.com/patent/CN117216205A/en) |
| 17 | CN117076607A | Method, device and query system for establishing logical expressions using large language models | 山东和信智能科技有限公司 | 2023-11-17 | 自然语言到逻辑表达的转换与查询。 | 中：逻辑中间表示相邻。 | 将逻辑映射作为可选实现，不作为核心发明点。 | [Link](https://patents.google.com/patent/CN117076607A/en) |
| 18 | CN118863098B | Large model combination system crossing knowledge field | 清华大学 | 2024-10-29 | 跨知识域多模型组合与协同。 | 中：多模型协同相邻。 | 强化“分歧识别-解耦-裁决-融合”链路与字段。 | [Link](https://patents.google.com/patent/CN118863098B/en) |
| 19 | CN119829038B | Code generation method, system and electronic device based on heterogeneous multi-agent collaboration | 苏州元脑智能科技有限公司 | 2025-04-15 | 异构多Agent协作并引入评论代理。 | 中：评审代理思想相邻。 | 场景限定为问答一致性，不落入代码生成框架。 | [Link](https://patents.google.com/patent/CN119829038B/en) |
| 20 | US20240289561A1 | Large language model artificial intelligence text evaluation system | Microsoft Technology Licensing, Llc | 2024-08-29 | 对文本片段相关性评分以评估AI输出质量。 | 中低：通用评估。 | 新增冲突类型、最小冲突集与证据计划三重限定。 | [Link](https://patents.google.com/patent/US20240289561A1/en) |

## Top5 最接近专利（用于 claim chart 深度比对）

1. `US20250200392A1`
2. `US12353469B1`
3. `US20250077777A1`
4. `CN119961628A`
5. `WO2024254203A2`

