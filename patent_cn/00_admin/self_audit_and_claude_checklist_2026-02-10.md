# 自查漏洞与专利潜力评估（2026-02-10）

## 1. 本轮自查范围
- 代码范围：`dual_model_divergence_project/` 全部核心模块、测试与实验脚本。
- 回归命令：`python run_test_cases.py`
- 回归结果：全通过（basic/stage2/stage3 + benchmark + realworld benchmark）。

## 2. 自查结论（执行摘要）
- 当前系统已具备可演示的“分歧检测 -> 结构化解耦 -> 证据裁决 -> 融合输出”闭环。
- 主要风险已从“稳定性风险”转为“能力边界风险”：
  - 能处理 3 类冲突，但证据裁决当前仅支持 `numeric_difference` 自动裁决。
  - 专利描述中的 provenance 细粒度追溯、迭代收敛、预算调度仍未实现。
- 结论：可继续推进专利申请材料，但若目标是“高强度实审抗辩”，建议进入下一轮补强（见第5节）。

## 3. 漏洞/风险清单（按优先级）

### P1（高优先）
1. 证据裁决类型覆盖不足  
   - 位置：`dual_model_divergence_project/modules/evidence_retriever.py:130`  
   - 现状：仅 `numeric_difference` 走证据门控，`omission/contradiction` 固定 `unknown`。  
   - 风险：分歧类型扩展后，裁决能力与检测能力不对齐。  
   - 建议：扩展 `fetch_evidence()` 至多类型策略接口（至少为 contradiction 提供可选外部证据映射）。

2. 主题归一化过于激进  
   - 位置：`dual_model_divergence_project/modules/evidence_retriever.py:10`  
   - 现状：`replace("技术", "")` 会移除任意位置“技术”。  
   - 风险：主题误匹配（同名碰撞、误裁决）。  
   - 建议：改为仅删除后缀“技术”或做词边界约束。

3. 否定词规则易误报  
   - 位置：`dual_model_divergence_project/modules/divergence_detector.py:11-25`  
   - 现状：`"不"、"无"、"未"` 作为独立模式，语境区分弱。  
   - 风险：矛盾冲突误检（false positive）。  
   - 建议：增加上下文模式（例如“不是/并非/不可/cannot/not”优先），单字否定降权或二次验证。

### P2（中优先）
4. provenance 追溯粒度不足  
   - 位置：`dual_model_divergence_project/modules/fusion_generator.py`、`dual_model_divergence_project/modules/database.py`  
   - 现状：输出未包含段落级/证据ID级追溯链。  
   - 风险：专利“可审计性”卖点不够硬。  
   - 建议：新增 provenance 字段并持久化（unit_id -> source_model -> sentence_index -> evidence_id）。

5. DB 事务异常回滚未显式化  
   - 位置：`dual_model_divergence_project/modules/database.py:17-21`  
   - 现状：依赖连接关闭隐式回滚。  
   - 风险：异常场景审计可解释性较弱。  
   - 建议：`except: conn.rollback(); raise`。

6. API 用量未入库  
   - 位置：`dual_model_divergence_project/modules/model_invoker.py:106-111`  
   - 现状：`usage_info` 仅写入 `mode=`。  
   - 风险：无法进行成本审计与性能优化。  
   - 建议：抽取 token usage（若SDK返回）并写入 JSON 文本。

7. Anthropic `max_tokens` 硬编码  
   - 位置：`dual_model_divergence_project/modules/model_invoker.py:45`  
   - 风险：复杂输入可能截断。  
   - 建议：改环境变量配置 `ANTHROPIC_MAX_TOKENS`。

8. 图谱冲突可能与文本冲突重复  
   - 位置：`dual_model_divergence_project/main.py:53-67`  
   - 风险：冲突项重复，影响后续裁决统计。  
   - 建议：基于 `subject/type/claim` 做去重索引。

### P3（建议）
9. `PRAGMA table_info({table})` 使用字符串拼接  
   - 位置：`dual_model_divergence_project/modules/database.py:25`  
   - 风险：当前低（内部常量调用），但规范性不足。  
   - 建议：白名单校验 table 名称。

10. 图谱抽取规则覆盖窄  
   - 位置：`dual_model_divergence_project/modules/knowledge_graph.py:17-21`  
   - 建议：扩展谓词模式并加入否定关系抽取。

## 4. 专利发表潜力自评

### 4.1 量化评分（内部评估）
- 技术新颖表达度：8.0/10  
- 工程可实现性：7.8/10  
- 代码-权利要求对齐度：6.8/10  
- 可验证性与实验证据：7.5/10  
- 综合潜力：7.5/10（中高）

### 4.2 优势
1. 已形成可运行闭环并有自动化回归与双benchmark支撑。
2. 证据门控（L1/L2/L3）规则明确，工程可解释性强。
3. 分歧检测已从精确匹配升级为加权模糊匹配，技术叙述更可信。

### 4.3 主要短板（影响实审说服力）
1. 多类型冲突检测与多类型证据裁决尚未闭环。
2. provenance 细粒度链路未完全落地。
3. 迭代收敛与预算调度仍停留在文档层描述，代码实现不足。

### 4.4 发布策略建议
1. 若近期提交：建议在说明书中明确“当前实施例覆盖范围”，避免超范围承诺。  
2. 若追求更高授权稳健性：建议先补齐第5节三项高优先补强后再提交。

## 5. 下一轮建议（收到 Claude 新评审后执行）
1. 做“问题逐条对照矩阵”：逐条判定 `同意/部分同意/不同意`。  
2. 每条问题必须有：代码证据路径、复现实验命令、修复计划或反证理由。  
3. 形成最终处置表并回写 `work_progress.md`。

---

# Claude 4.6 严格代码审核清单（可直接执行）

## A. 基线与可复现
- [ ] A01 `git log --oneline -n 10` 与文档阶段描述一致
- [ ] A02 `git status --short` 仅出现预期未提交文件
- [ ] A03 `python run_test_cases.py` 全通过
- [ ] A04 benchmark 报告时间戳与当前执行匹配  
  文件：`dual_model_divergence_project/experiments/benchmark_report.md`
- [ ] A05 realworld 报告时间戳与当前执行匹配  
  文件：`dual_model_divergence_project/experiments/realworld_benchmark_report.md`

## B. 主流程安全与稳定
- [ ] B01 空问题拦截有效：`main.py:24-25`
- [ ] B02 超长问题拦截有效：`main.py:26-27`
- [ ] B03 默认 DB 路径不依赖 cwd：`main.py:117`
- [ ] B04 `--allow-mock-fallback` 未开启时 API 失败会抛错
- [ ] B05 `--enable-graph` 关闭时不影响默认路径

## C. 分歧检测算法
- [ ] C01 共识匹配为加权模糊匹配而非集合精确匹配
- [ ] C02 `match_score` 计算符合 `0.7/0.2/0.1`
- [ ] C03 一对一匹配无重复占用
- [ ] C04 `numeric_difference` 识别有效
- [ ] C05 `omission` 识别有效
- [ ] C06 `contradiction` 识别有效
- [ ] C07 `year_conflict_generic` 包含 `subject/model_a_claim/model_b_claim`
- [ ] C08 否定词检测误报率是否可接受（抽样评测）

## D. 解耦与融合
- [ ] D01 冲突单元生成 `subquestion`
- [ ] D02 冲突单元生成 `evidence_snippets`
- [ ] D03 单元具备 `topic_tag`
- [ ] D04 融合输出四区完整：共识/补充/裁决/待验证
- [ ] D05 `unknown` 冲突必须进入待验证区
- [ ] D06 空结构回退保留双模型原文

## E. 证据裁决
- [ ] E01 L1 自动裁决行为正确
- [ ] E02 双独立 L2 自动裁决行为正确
- [ ] E03 L3 不自动裁决
- [ ] E04 `int/str` 年份混用不影响裁决
- [ ] E05 多类型冲突进入 evidence 模块时行为符合预期（当前应为 unknown）
- [ ] E06 subject 归一化不会产生明显误匹配（抽样）

## F. 调用与缓存
- [ ] F01 缓存隔离：mock 不污染 live
- [ ] F02 fallback_mock 不当作 live cache 命中
- [ ] F03 API 重试机制可触发
- [ ] F04 timeout 参数有效
- [ ] F05 `usage_info` 字段内容是否满足审计需求（当前可能不足）

## G. 数据层
- [ ] G01 表结构与迁移幂等
- [ ] G02 evidence 新字段存在：`source_tier/auto_applied/confidence`
- [ ] G03 异常事务回滚策略是否明确
- [ ] G04 WAL + busy_timeout 配置符合预期
- [ ] G05 SQL 拼接风险是否可接受并有约束

## H. 图谱模块
- [ ] H01 `--enable-graph` 路径执行正确
- [ ] H02 图谱冲突与文本冲突是否重复记录
- [ ] H03 图谱规则覆盖是否满足当前演示目标

## I. 实验有效性
- [ ] I01 benchmark case 设计是否覆盖主路径和失败路径
- [ ] I02 realworld case 与 prior_art 数据映射是否真实可追溯
- [ ] I03 报告指标是否存在乐观偏差（仅小样本全绿）
- [ ] I04 报告中是否有分层误差分析（TP/FP/FN/F1）

## J. 专利对齐审查
- [ ] J01 代码与“分歧检测、解耦、裁决、融合”四步主叙述一致
- [ ] J02 未实现能力是否在文档中明确标注“后续阶段”
- [ ] J03 不夸大已实现能力（尤其 provenance、迭代收敛、预算调度）

## K. 交接与审计
- [ ] K01 `work_progress.md` 有时间戳、风险、评审清单
- [ ] K02 `final_package_manifest.md` 包含最新阶段文件
- [ ] K03 评审处置文档与代码实际一致  
  文件：`patent_cn/00_admin/engineering_review_audit_2026-02-10.md`

---

## 建议 Claude 输出格式
1. Findings（按 P0/P1/P2/P3，必须含：文件路径 + 行号 + 复现命令）
2. Open Questions（不确定假设）
3. Minimal Fix Set（最小可合并修复清单）
