# 占位符替换定位（提交包）

| 占位符 | 建议替换内容 | 主要位置 |
|---|---|---|
| 【申请人名称】 | 企业/个人全称 | `patent_cn/00_admin/applicant_inventor.json` |
| 【申请人地址】 | 通信地址 | `patent_cn/00_admin/applicant_inventor.json` |
| 【发明人1】 | 第一发明人姓名 | `patent_cn/00_admin/applicant_inventor.json` |
| 【发明人2】 | 第二发明人姓名 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系人】 | 对接联系人 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系电话】 | 电话 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系邮箱】 | 邮箱 | `patent_cn/00_admin/applicant_inventor.json` |
| 【相似度阈值】 | 对齐匹配阈值（如0.78） | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md` |
| 【NLI阈值】 | 分歧分类置信度阈值（如0.82） | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md` |
| 【最大迭代次数】 | 迭代上限（如3） | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md`、`patent_cn/03_claims/claims_final.md` |
| 【实施例参数】 | 性能参数/统计值 | `patent_cn/02_invention_design/problem_solution_effect.md` |

## 替换建议

1. 先替换 `00_admin` 中主体信息，再替换技术阈值参数。  
2. 若未确定阈值，可先保留占位符，提交前统一替换。  
3. 替换后重新执行脚本检查，确保格式与编号未被破坏。

