# 占位符替换清单（总表）

| 占位符 | 含义 | 主要出现文件 |
|---|---|---|
| 【申请人名称】 | 专利申请主体名称 | `patent_cn/00_admin/applicant_inventor.json`、`patent_cn/04_spec/spec_draft.md` |
| 【申请人地址】 | 申请人通信地址 | `patent_cn/00_admin/applicant_inventor.json` |
| 【邮编】 | 申请人邮编 | `patent_cn/00_admin/applicant_inventor.json` |
| 【国家或地区】 | 申请人所属国家或地区 | `patent_cn/00_admin/applicant_inventor.json` |
| 【统一社会信用代码或身份证明】 | 主体证照号 | `patent_cn/00_admin/applicant_inventor.json` |
| 【发明人1】 | 第一发明人姓名 | `patent_cn/00_admin/applicant_inventor.json`、`patent_cn/04_spec/spec_draft.md` |
| 【发明人2】 | 第二发明人姓名 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系人】 | 对接联系人 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系电话】 | 联系电话 | `patent_cn/00_admin/applicant_inventor.json` |
| 【联系邮箱】 | 联系邮箱 | `patent_cn/00_admin/applicant_inventor.json` |
| 【实施例参数】 | 可替换的实验参数集合 | `patent_cn/02_invention_design/*.md`、`patent_cn/04_spec/spec_draft.md` |
| 【相似度阈值】 | 语义对齐阈值 | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md` |
| 【NLI阈值】 | 分歧分类置信度阈值 | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md` |
| 【最大迭代次数】 | S8 收敛迭代上限 | `patent_cn/02_invention_design/algorithm_steps.md`、`patent_cn/04_spec/spec_draft.md` |

## 使用规则
- 占位符统一使用中文全角方括号，避免与技术术语冲突。
- 未获取用户信息前，不替换占位符，不阻断文本生成。
- 在最终 docx 包中同步保留“占位符总表 + 文件内定位说明”。

