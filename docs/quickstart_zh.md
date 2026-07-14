# 中文快速开始

这个仓库是一套“AI 原型到生产准备度工具箱”。它适合在以下场景使用：

- AI demo 已经能跑，但不知道能不能进入真实业务；
- 项目负责人需要判断是否可以试点；
- 合规/风控/审计团队需要明确数据、模型、权限、日志和人工复核边界；
- FDE / 解决方案 / AI 治理顾问需要快速做客户发现和上线条件评估。

## 15 分钟用法

1. 用 `templates/fde_discovery_interview_guide.md` 访谈业务方；
2. 用 `templates/ai_prototype_readiness_checklist.md` 逐项打分；
3. 用 `templates/risk_register.md` 记录风险、责任人和证据；
4. 用 `scorecards/ai_prototype_readiness_scorecard.md` 给出结论；
5. 用 `templates/pilot_review_memo.md` 写出是否进入试点的建议。

## 评分结论

| 分数 | 建议 |
|---:|---|
| 0–25 | 只能算 demo，不建议进入真实业务 |
| 26–45 | 只能做受控试点 |
| 46–60 | 可考虑小范围生产试运行，但要有监控和回滚 |
| 61–70 | 准备度较高，但仍要检查一票否决项 |

## 一票否决

出现以下任一情况，不建议进入生产：

- 数据授权不清；
- 敏感/个人/受监管数据进入未批准外部模型；
- 高风险事项没有人工复核；
- 没有日志、版本和责任链；
- 无法评估模型输出质量；
- 没有人负责暂停、回滚、纠错和持续维护。

## 这个仓库不是法律意见

它不是合规认证、法律意见或安全审计。它只是一个结构化讨论和试点前检查工具。

## CLI 用法

本仓库现在包含一个轻量 CLI：`ai-ready`。

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
ai-ready score examples/sample_assessment.json
ai-ready report examples/sample_assessment.json --output examples/reports/sample_assessment_report.md
```

它的作用不是替代治理判断，而是把 readiness review 的输入结构化，输出一个可复核的评分和 Markdown 报告。
