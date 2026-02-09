# 最终交付清单（Manifest）

## A. 申请正文文件

- `patent_cn/03_claims/claims_final.docx`：权利要求书（提交主文档）  
- `patent_cn/04_spec/spec_final.docx`：说明书（提交主文档）  
- `patent_cn/04_spec/abstract_final.docx`：说明书摘要（提交主文档）  

## B. 检索与避撞文件

- `patent_cn/01_prior_art/patent_list_top20.md`：Top20 相关专利清单  
- `patent_cn/01_prior_art/closest5_claim_chart.xlsx`：Top5 要素对比表  
- `patent_cn/01_prior_art/novelty_strategy.md`：差异化路线与风险策略  

## C. 技术方案设计文件

- `patent_cn/02_invention_design/problem_solution_effect.md`  
- `patent_cn/02_invention_design/system_architecture.md`  
- `patent_cn/02_invention_design/data_structures.md`  
- `patent_cn/02_invention_design/algorithm_steps.md`  
- `patent_cn/02_invention_design/embodiments_outline.md`  

## D. 附图文件

- `patent_cn/05_drawings/fig1_system_architecture.png`  
- `patent_cn/05_drawings/fig2_method_flow.png`  
- `patent_cn/05_drawings/fig3_disagreement_graph.png`  
- `patent_cn/05_drawings/fig4_decoupling_subquestions.png`  
- `patent_cn/05_drawings/fig5_iteration_feedback_loop.png`  
- `patent_cn/05_drawings/fig6_data_structure.png`  
- `patent_cn/05_drawings/drawings_list.md`

## E. 格式检查与提交辅助

- `patent_cn/06_packaging/submission_checklist.md`  
- `patent_cn/06_packaging/placeholder_map.md`  
- `patent_cn/06_packaging/cnipa_format_check.md`  
- `patent_cn/06_packaging/claim_support_map.md`  
- `patent_cn/06_packaging/abstract_len_check.md`  
- `patent_cn/06_packaging/export_pdf.log`

## F. 评审与计划文档

- `patent_cn/00_admin/technical_scheme_review_2026-02-09.md`  
- `patent_cn/02_invention_design/engineering_plan_v2.md`  
- `patent_cn/00_admin/current_status_and_next_steps.md`

## G. 工程骨架（阶段1）

- `dual_model_divergence_project/main.py`  
- `dual_model_divergence_project/modules/database.py`  
- `dual_model_divergence_project/modules/model_invoker.py`  
- `dual_model_divergence_project/modules/divergence_detector.py`  
- `dual_model_divergence_project/modules/decoupler.py`  
- `dual_model_divergence_project/modules/fusion_generator.py`  
- `dual_model_divergence_project/modules/evidence_retriever.py`  
- `dual_model_divergence_project/modules/knowledge_graph.py`  
- `dual_model_divergence_project/tests/test_basic_flow.py`  
- `dual_model_divergence_project/README.md`  
- `dual_model_divergence_project/requirements.txt`

## H. 阶段2增强与测试

- `dual_model_divergence_project/modules/evidence_retriever.py`  
- `dual_model_divergence_project/data/evidence_catalog.json`  
- `dual_model_divergence_project/tests/test_stage2_cases_unittest.py`  
- `dual_model_divergence_project/tests/TEST_CASES.md`  
- `dual_model_divergence_project/run_test_cases.py`

## I. 阶段3实验与回归增强

- `dual_model_divergence_project/tests/test_basic_flow.py`
- `dual_model_divergence_project/experiments/benchmark_cases.json`
- `dual_model_divergence_project/experiments/run_benchmark.py`
- `dual_model_divergence_project/experiments/benchmark_report.md`

## J. 阶段4真实样本分层评测

- `dual_model_divergence_project/experiments/realworld_cases.json`
- `dual_model_divergence_project/experiments/realworld_evidence_catalog.json`
- `dual_model_divergence_project/experiments/run_realworld_benchmark.py`
- `dual_model_divergence_project/experiments/realworld_benchmark_report.md`
- `dual_model_divergence_project/tests/test_stage3_realworld_benchmark_unittest.py`
