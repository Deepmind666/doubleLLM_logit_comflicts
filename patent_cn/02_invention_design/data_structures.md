# 数据结构定义（M2）

## 1. 论点单元（Proposition Unit）

```json
{
  "unit_id": "A_003",
  "model_side": "A",
  "topic": "药物剂量上限",
  "type": "constraint",
  "text": "每日剂量不超过20mg",
  "source_para": "OA.p4",
  "confidence": 0.81,
  "evidence_refs": ["doc_12#p3"]
}
```

字段说明：
- `type`: `conclusion|condition|step|constraint|assumption`
- `source_para`: 源输出段落定位，用于 provenance
- `confidence`: 来自模型或后处理估计分值

## 2. 对齐匹配关系 M

```json
{
  "pair_id": "M_014",
  "unit_a": "A_003",
  "unit_b": "B_005",
  "semantic_sim": 0.84,
  "rule_score": 0.76,
  "position_score": 0.66,
  "match_score": 0.79
}
```

## 3. 分歧点 D

```json
{
  "divergence_id": "D_014",
  "pair_id": "M_014",
  "divergence_type": "boundary_conflict",
  "nli_label": "contradiction",
  "nli_conf": 0.88,
  "numeric_delta": 5.0,
  "status": "pending_adjudication"
}
```

类型枚举：
- `contradiction`
- `missing`
- `assumption_conflict`
- `boundary_conflict`
- `numeric_difference`
- `definition_difference`

## 4. 子问题与证据计划

```json
{
  "sub_question_id": "Q_D_014",
  "divergence_id": "D_014",
  "question_text": "针对成人患者，安全剂量上限应为多少？",
  "verifiable": true,
  "retrievable": true,
  "executable": true,
  "retrieval_plan": [
    {"source": "kb_internal", "priority": 1, "expected_gain": 0.72},
    {"source": "web_guideline", "priority": 2, "expected_gain": 0.61}
  ]
}
```

## 5. 裁决记录 J_d

```json
{
  "judgment_id": "J_014",
  "divergence_id": "D_014",
  "decision": "support_B",
  "decision_confidence": 0.83,
  "evidence_ids": ["E_203", "E_204"],
  "evidence_tier_used": "L1",
  "auto_applied": true,
  "explanation": "B侧引用证据更完整且时间更新。",
  "keep_multi_solution": false
}
```

## 6. 融合输出 F（固定模板）

```json
{
  "result_id": "F_20260209_001",
  "consensus_section": ["..."],
  "divergence_section": ["..."],
  "adjudication_section": ["..."],
  "pending_section": ["..."],
  "provenance": [
    {"output_para": "F.p7", "source": ["OA.p4", "OB.p5", "J_014"]}
  ]
}
```

## 7. 审计与合规记录

```json
{
  "audit_id": "AUD_001",
  "privacy_check": "pass",
  "bias_check": "pass",
  "illegal_content_check": "pass",
  "evidence_gate_check": "pass",
  "timestamp": "2026-02-09T15:00:00+08:00"
}
```
