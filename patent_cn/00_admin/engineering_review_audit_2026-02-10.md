# 工程评审复核与处置记录（2026-02-10）

## 1. 复核范围
- 依据 `.claude.md` 中第三轮评审（问题 #39~#60）进行复核。
- 本轮目标：优先修复算法主链路偏差，提升“评审结论 -> 可执行改动”的闭环质量。

## 2. 复核结论（摘要）
- 已采纳并落地：
  - #39：共识检测由“精确集合匹配”升级为“加权模糊匹配”。
  - #41：新增冲突类型 `omission`、`contradiction`（原有 `numeric_difference` 保留）。
  - #42：`decoupler` 增加子问题生成与依据片段抽取。
  - #51：融合输出新增“待验证区”，与共识/补充/裁决形成四区结构。
  - #45：`db_path` 默认路径改为相对 `main.py` 解析，去除对 `cwd` 的依赖。
  - #40：`requirements.txt` 将 `openai` 下限提升至 `1.68.0`，与 Responses API 对齐。
  - #56（部分）：新增算法回归测试，覆盖模糊匹配/遗漏/矛盾/超长输入。
- 本轮部分处理：
  - #43：接入可选图谱冲突检测开关 `--enable-graph`，默认关闭。
- 本轮暂未处理（后续阶段）：
  - provenance 细粒度追溯结构（#52）
  - 完整迭代收敛控制链路（#11/#12）
  - 预算调度与多资源编排（#14/#17）

## 3. 代码改动清单
- `dual_model_divergence_project/modules/divergence_detector.py`
  - 引入加权匹配：`0.7 semantic + 0.2 rule + 0.1 position`
  - 新增冲突识别：`numeric_difference / omission / contradiction`
  - 输出增强：保留句级匹配与索引信息，支撑后续结构化解耦。
- `dual_model_divergence_project/modules/decoupler.py`
  - 为冲突单元生成子问题（subquestion）
  - 抽取模型A/B依据片段（evidence_snippets）
  - 增加主题标签（topic_tag）
- `dual_model_divergence_project/modules/fusion_generator.py`
  - 输出重构为四区：共识区/补充区/裁决区/待验证区
- `dual_model_divergence_project/main.py`
  - `db_path` 默认值路径修正
  - 新增 `--enable-graph` 开关并可选注入图谱冲突
- `dual_model_divergence_project/requirements.txt`
  - `openai>=1.68.0`
- `dual_model_divergence_project/tests/test_basic_flow.py`
  - 新增测试：模糊共识、遗漏冲突、矛盾冲突、超长输入拦截

## 4. 验证结果
- 命令：`python run_test_cases.py`
- 结果：全部通过
  - `tests.test_basic_flow`：7/7
  - `tests.test_stage2_cases_unittest`：5/5
  - `tests.test_stage3_realworld_benchmark_unittest`：1/1
  - `experiments/run_benchmark.py`：6/6 case 通过
  - `experiments/run_realworld_benchmark.py`：7/7 case 通过

## 5. 后续建议
1. 继续补足 provenance（段落级来源、证据ID级追溯）。
2. 将图谱冲突与文本冲突做去重融合，避免重复冲突项。
3. 引入迭代收敛与预算调度模块，推进对权利要求11/12/14/17的实现对齐。
