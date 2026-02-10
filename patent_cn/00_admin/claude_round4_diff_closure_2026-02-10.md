# Claude 第四轮评审对比闭环（2026-02-10）

## 1. 处理范围
- 对比基线：`.claude.md` 第四轮 Findings（#66~#77）与“最小补丁集 Patch 1~6”。
- 本轮执行目标：先完成可独立并行的 6 个最小补丁，并给出验证证据。

## 2. 对比矩阵（评审意见 -> 代码处置）

| Finding | 评审问题 | 处置状态 | 代码变更 | 验证 |
|---:|---|---|---|---|
| #66 | 图谱矛盾检测死逻辑（无法抽取“不是”） | 已修复 | `modules/knowledge_graph.py` 增加 `(r"(.+?)不是(.+)", "不是")`，且优先于“是” | `tests.test_basic_flow.test_graph_extractor_should_capture_negated_relation` |
| #67 | realworld benchmark 全英文，F1 不可信 | 已修复 | `experiments/realworld_cases.json` 增加3个中文自然表述用例；`realworld_evidence_catalog.json` 增加对应证据 | `python experiments/run_realworld_benchmark.py` -> `10/10` |
| #69 | 否定词“ 不 ”匹配过宽 | 已修复 | `modules/divergence_detector.py` 将单字“不”替换为短语模式 `不(?:是|会|能|可|应|要|对|好|行|利|宜)` | `tests.test_basic_flow.test_negation_pattern_should_not_match_non_negative_phrase` |
| #71 | 图谱冲突与检测器冲突无去重 | 已修复 | `main.py` 追加图谱冲突前按 `(type, model_a_claim, model_b_claim)` 去重（含反向签名） | `tests.test_basic_flow.test_pipeline_graph_conflict_should_be_deduplicated` |
| #73 | `_normalize_subject` 全文替换“技术” | 已修复 | `modules/evidence_retriever.py` 改为 `re.sub(r"技术$", "", ...)` 仅删后缀 | `tests.test_basic_flow.test_normalize_subject_should_only_strip_suffix_technology` |
| #74 | 缓存 `LIKE` 通配符理论误匹配 | 已修复 | `modules/database.py` 从 `LIKE mode=...%` 改为 `= mode=...` 精确匹配 | `tests.test_stage2_cases_unittest.test_cache_mode_query_should_use_exact_match` |

## 3. 与 #68 的关系说明（遗留P1影响评估）
- #68 指向的是“仍有遗留 P1/P2 影响代码-专利对齐度”的综合问题，不是单一补丁可一次性清零。
- 本轮已把其中可最小补丁化的 6 项全部落地，降低了 #68 的风险暴露面。
- 仍待下一轮处理的核心差距：
  1. 多类型证据裁决（当前 evidence 自动裁决仍集中在 `numeric_difference`）
  2. provenance 细粒度追溯（段落/证据ID级）
  3. 迭代收敛与预算调度代码化实现

## 4. 本轮回归结果
- 命令：`python run_test_cases.py`
- 结果：
  - `tests.test_basic_flow`: 11/11 PASS
  - `tests.test_stage2_cases_unittest`: 6/6 PASS
  - `tests.test_stage3_realworld_benchmark_unittest`: 1/1 PASS
  - `experiments/run_benchmark.py`: 6/6 case PASS
  - `experiments/run_realworld_benchmark.py`: 10/10 case PASS

## 5. 结论
- Claude 第四轮建议中的“可最小化独立补丁”已全部闭环。
- 下一轮可进入“遗留P1体系化补强”（非最小补丁）阶段。
