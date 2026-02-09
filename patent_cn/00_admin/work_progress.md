# 项目进展日志（审计版）

## 2026-02-09 14:36:54 +08:00 | 阶段：M0 启动

### 本次完成
- 读取并解析主任务文档 `gptdeepsearch2_9.md`，确认里程碑 M0~M5 与强约束。
- 创建项目根交接规范文件 `.claude.md`，固化交付标准、检查项与脚本入口。
- 初始化目录结构 `patent_cn/00_admin` 至 `patent_cn/06_packaging` 及 `patent_cn/scripts`。
- 建立申请人/发明人占位数据文件 `applicant_inventor.json`。
- 建立占位符总表 `placeholder_map.md`，定义替换点与文件映射。

### 风险与修正动作
- 风险：任务文档初始读取出现编码乱码，可能导致约束误读。
- 修正：已切换 UTF-8 重新读取并确认完整内容。
- 风险：尚未完成 M1 的真实专利检索，当前仅完成结构化准备。
- 修正：下一步将执行中英文检索并输出 Top20/Top5 对比。

### 文件评审清单
- 完整性：已创建 M0 基础目录与管理员配置文件。
- 术语一致性：已统一“模型A/模型B/分歧点/论点单元”等术语。
- 可实现性：保留脚本入口，后续将以 Python 自动化生成 docx 与附图。
- 合规性：已约束原创改写与可授权性风险检查机制。

### 本次新增/更新文件
- `.claude.md`
- `patent_cn/00_admin/applicant_inventor.json`
- `patent_cn/00_admin/placeholder_map.md`
- `patent_cn/00_admin/work_progress.md`

---

## 2026-02-09 14:54:18 +08:00 | 阶段：M1 完成

### 本次完成
- 完成中英文关键词检索，覆盖 `CN + US + WO` 专利公开文本。
- 抓取并整理 20 条高相关专利元数据（标题、申请人、公开日、摘要/权项线索）。
- 形成 `Top20` 清单并给出每条文献的相似点与规避策略。
- 选定 Top5 最接近专利并输出要素对比表（`closest5_claim_chart.xlsx`）。
- 输出差异化规避路线 `A/B/C`，明确独权写法与风险边界。

### 风险与修正动作
- 风险：终端编码导致早期自动生成文本出现乱码。
- 修正：关键产物改为手工校对重写（Markdown）+ 重新导出 xlsx，避免问号污染。
- 风险：Top20 以公开文本初筛为主，法律稳定性与授权文本仍需代理人复核。
- 修正：已在各条目加入“规避写法”，后续权利要求落地时继续加限定词。

### 文件评审清单
- 完整性：Top20、Top5 claim chart、A/B/C 差异化路线齐全。
- 术语一致性：围绕“分歧点、论点单元、子问题裁决、融合输出”统一表述。
- 可实现性：规避策略可直接映射到独立权利要求和从属权利要求。
- 合规性：未复制专利原文，均为改写摘要级描述。

### 本次新增/更新文件
- `patent_cn/01_prior_art/_raw_patent_meta.json`
- `patent_cn/01_prior_art/patent_list_top20.md`
- `patent_cn/01_prior_art/closest5_claim_chart.xlsx`
- `patent_cn/01_prior_art/novelty_strategy.md`

---

## 2026-02-09 14:58:17 +08:00 | 阶段：M2 完成

### 本次完成
- 输出技术方案定稿文档：问题-方案-效果、系统架构、数据结构、算法步骤、实施例提纲。
- 建立三路线权利要求草案：`A/B/C`，并分别绑定差异化保护重点。
- 在文档中显式固化至少 10 个差异化技术特征，可直接映射从属权利要求。

### 风险与修正动作
- 风险：若独权写成“通用一致性验证”会与近似专利重叠。
- 修正：三路线已分别引入图谱、子问题可验证、预算收敛与合规模块等限定。
- 风险：从属条款若缺参数限定易被质疑不清楚。
- 修正：已在算法与实施例中加入阈值、停止条件、字段结构支撑。

### 文件评审清单
- 完整性：M2 指定文件已全部创建。
- 术语一致性：模型A/B、论点单元、分歧点、结构化解耦、J_d、provenance 已统一。
- 可实现性：每个步骤均有输入/输出与数据结构定义。
- 合规性：避免“思考/理解”措辞，使用可执行技术步骤表达。

### 本次新增/更新文件
- `patent_cn/02_invention_design/problem_solution_effect.md`
- `patent_cn/02_invention_design/system_architecture.md`
- `patent_cn/02_invention_design/data_structures.md`
- `patent_cn/02_invention_design/algorithm_steps.md`
- `patent_cn/02_invention_design/embodiments_outline.md`
- `patent_cn/03_claims/claims_route_A.md`
- `patent_cn/03_claims/claims_route_B.md`
- `patent_cn/03_claims/claims_route_C.md`

---

## 2026-02-09 15:00:23 +08:00 | 阶段：M3 完成

### 本次完成
- 完成说明书草案 `spec_draft.md`，包含技术领域、背景技术、发明内容、附图说明、具体实施方式。
- 在说明书中补齐术语定义、模块标记（101~110）与流程 S1~S8 的对应关系。
- 完成摘要草案 `abstract.md`，覆盖技术领域、技术问题、技术方案要点和用途。
- 明确 3 个实施例（无证据、多证据、资源受限迭代）并给出参数示例与数据结构字段。

### 风险与修正动作
- 风险：摘要可能超 300 字，影响提交格式。
- 修正：下一阶段将用脚本做字数强校验并自动告警。
- 风险：权利要求与说明书支撑关系需进一步显式映射。
- 修正：M5 阶段新增 `claim_support_mapper.py` 输出支撑检查报告。

### 文件评审清单
- 完整性：说明书主体章节完整，满足中国发明专利常用结构。
- 术语一致性：关键术语在“术语定义”与“步骤”处已闭环。
- 可实现性：实施例中给出参数、数据结构、停止条件。
- 合规性：明确加入数据合规与安全过滤实现。

### 本次新增/更新文件
- `patent_cn/04_spec/spec_draft.md`
- `patent_cn/04_spec/abstract.md`

---

## 2026-02-09 15:06:11 +08:00 | 阶段：M4 完成

### 本次完成
- 编写并运行 `build_figures.py`，已生成 6 张 300dpi 附图。
- 生成附图清单 `drawings_list.md`，明确摘要附图选择与标记映射规则。
- 修复图中文字字体兼容问题：图内标注改为英文/编号，避免跨环境缺字。

### 风险与修正动作
- 风险：中文字体在不同环境缺失会导致图内标签不可见。
- 修正：统一采用英文+模块编号，说明书中保留中文释义并一一映射。
- 风险：图号与说明书标记不一致会导致形式审查问题。
- 修正：清单中固化 101~110 与图1~图6 映射，并纳入后续自动校验。

### 文件评审清单
- 完整性：图1~图6文件齐全，命名满足任务约束。
- 术语一致性：图中模块编号与说明书标记说明一致。
- 可实现性：附图由脚本生成，可重复构建。
- 合规性：图中不含营销性描述，保留技术表达。

### 本次新增/更新文件
- `patent_cn/scripts/build_figures.py`
- `patent_cn/05_drawings/fig1_system_architecture.png`
- `patent_cn/05_drawings/fig2_method_flow.png`
- `patent_cn/05_drawings/fig3_disagreement_graph.png`
- `patent_cn/05_drawings/fig4_decoupling_subquestions.png`
- `patent_cn/05_drawings/fig5_iteration_feedback_loop.png`
- `patent_cn/05_drawings/fig6_data_structure.png`
- `patent_cn/05_drawings/drawings_list.md`

---

## 2026-02-09 23:40:49 +08:00 | 阶段：M5 完成 + 技术方案再评审

### 本次完成
- 完成 `claims_final.md/spec_draft.md/abstract.md` 到 `docx` 的自动导出并生成目标文档。
- 运行并通过检查脚本：摘要字数、权利要求编号连续性、附图引用一致性、术语一致性、权利要求支撑映射。
- 补齐提交辅助文件：`submission_checklist.md`、`placeholder_map.md`、`final_package_manifest.md`、`export_pdf.log`。
- 对你新增的工程技术初步方案执行严谨评审，新增高优先问题清单与修订计划文档。
- 新增工程实施计划 v2，建立“工程模块 -> S1~S8 -> 专利支撑点”映射。

### 风险与修正动作
- 风险：新增工程方案偏实现层，若不绑定专利术语和权利要求，后续存在支撑断层。
- 修正：新增 `technical_scheme_review_2026-02-09.md` 与 `engineering_plan_v2.md`，显式建立双轨映射。
- 风险：当前目录尚未初始化 git，尚未推送到用户远程仓库。
- 修正：下一步执行 git 初始化、提交与推送。

### 文件评审清单
- 完整性：M0~M5 交付文件齐备（含 docx 与检查报告）。
- 术语一致性：说明书、权利要求、算法文档使用统一术语集。
- 可实现性：脚本可重复构建附图、docx与校验报告。
- 合规性：摘要长度与格式校验通过，可授权性风险已显式化。

### 本次新增/更新文件
- `patent_cn/00_admin/technical_scheme_review_2026-02-09.md`
- `patent_cn/02_invention_design/engineering_plan_v2.md`
- `patent_cn/06_packaging/submission_checklist.md`
- `patent_cn/06_packaging/placeholder_map.md`
- `patent_cn/06_packaging/final_package_manifest.md`
- `patent_cn/06_packaging/export_pdf.log`
- `patent_cn/03_claims/claims_final.docx`
- `patent_cn/04_spec/spec_final.docx`
- `patent_cn/04_spec/abstract_final.docx`
- `patent_cn/06_packaging/cnipa_format_check.md`
- `patent_cn/06_packaging/claim_support_map.md`
- `patent_cn/06_packaging/abstract_len_check.md`

---

## 2026-02-09 23:43:35 +08:00 | 阶段：新增技术方案评审闭环

### 本次完成
- 对 `gptdeepsearch2_9.md` 新增技术方案完成分级问题评审并输出整改建议。
- 新增 `current_status_and_next_steps.md`，明确“已完成/未完成/下一步顺序”。
- 将证据源分级与门控策略回填到算法、数据结构、说明书和权利要求。
- 新增权利要求19、20并重新生成 docx，所有检查脚本再次通过。
- 更新 `final_package_manifest.md`，纳入评审与计划文档。

### 风险与修正动作
- 风险：工程方案与专利文本仍可能在“代码实现粒度”上存在偏差。
- 修正：已建立工程模块到S1~S8与权利要求支撑点映射；后续每个代码迭代需同步回填。
- 风险：项目尚未纳入 Git 版本管理，交接与追溯风险仍在。
- 修正：下一步优先执行 git 初始化与远程推送。

### 文件评审清单
- 完整性：评审报告、计划文档、状态文档均已创建。
- 术语一致性：新增条款与既有术语集一致。
- 可实现性：门控规则已参数化并可代码化实现。
- 合规性：避免低可信证据自动裁决，降低错误融合风险。

### 本次新增/更新文件
- `patent_cn/00_admin/technical_scheme_review_2026-02-09.md`
- `patent_cn/00_admin/current_status_and_next_steps.md`
- `patent_cn/02_invention_design/engineering_plan_v2.md`
- `patent_cn/02_invention_design/algorithm_steps.md`
- `patent_cn/02_invention_design/data_structures.md`
- `patent_cn/04_spec/spec_draft.md`
- `patent_cn/03_claims/claims_final.md`
- `patent_cn/03_claims/claims_final.docx`
- `patent_cn/04_spec/spec_final.docx`
- `patent_cn/06_packaging/final_package_manifest.md`

---

## 2026-02-09 23:48:45 +08:00 | 阶段：版本管理与远程交付完成

### 本次完成
- 初始化本地 Git 仓库并建立 `main` 分支。
- 补充 `.gitignore`（忽略本地配置、虚拟环境、数据库文件等）。
- 完成首个提交：`a3ebb2d`。
- 关联远程仓库：`https://github.com/Deepmind666/doubleLLM_logit_comflicts.git`。
- 成功推送 `main` 到远程并设置 upstream 跟踪。

### 风险与修正动作
- 风险：初次提交时因 git 用户身份未配置导致提交失败。
- 修正：已为当前仓库设置本地提交身份后重试成功。
- 风险：本地配置文件可能误入仓库。
- 修正：已通过 `.gitignore` 排除 `.claude/` 与工作区文件。

### 文件评审清单
- 完整性：提交包含专利交付全量文件及脚本。
- 可追溯性：里程碑日志与提交记录一致。
- 安全性：敏感配置未入仓。
- 可协作性：远程分支与本地主分支已建立跟踪关系。

### 本次新增/更新文件
- `.gitignore`
- `patent_cn/00_admin/work_progress.md`

---

## 2026-02-09 23:56:35 +08:00 | 阶段：工程骨架阶段1落地

### 本次完成
- 新建 `dual_model_divergence_project` 工程骨架，包含主流程、模块包、测试目录、README 与 requirements。
- 实现模块：`model_invoker`、`divergence_detector`、`decoupler`、`fusion_generator`、`evidence_retriever`、`knowledge_graph`、`database`。
- 完成 SQLite 建表逻辑与主流程串联，支持 `--mock` 与 `--enable-evidence`。
- 修复环境依赖回退：`python-dotenv` 缺失时自动降级为 no-op，不阻断运行。
- 完成烟雾测试（ASCII样例）：
  - 年份冲突可识别
  - 管线执行成功
  - 数据库写入查询、回答、融合、证据记录

### 风险与修正动作
- 风险：当前环境未安装 `pytest`，无法直接执行自动化测试命令。
- 修正：已执行等价烟雾测试脚本验证关键链路，后续可安装 `pytest` 后补回归测试。
- 风险：中文参数在某些内联执行链路下有编码扰动。
- 修正：mock触发逻辑增加英文关键词分支，确保跨终端稳定演示。

### 文件评审清单
- 完整性：阶段1工程骨架文件完整，结构符合新增方案目录预期。
- 可实现性：主流程已可运行并输出融合答案。
- 可测试性：已提供 `tests/test_basic_flow.py` 与可执行烟雾路径。
- 可扩展性：已预留证据模块与知识图谱模块接口。

### 本次新增/更新文件
- `dual_model_divergence_project/main.py`
- `dual_model_divergence_project/modules/__init__.py`
- `dual_model_divergence_project/modules/database.py`
- `dual_model_divergence_project/modules/model_invoker.py`
- `dual_model_divergence_project/modules/divergence_detector.py`
- `dual_model_divergence_project/modules/decoupler.py`
- `dual_model_divergence_project/modules/fusion_generator.py`
- `dual_model_divergence_project/modules/evidence_retriever.py`
- `dual_model_divergence_project/modules/knowledge_graph.py`
- `dual_model_divergence_project/tests/__init__.py`
- `dual_model_divergence_project/tests/test_basic_flow.py`
- `dual_model_divergence_project/README.md`
- `dual_model_divergence_project/requirements.txt`
