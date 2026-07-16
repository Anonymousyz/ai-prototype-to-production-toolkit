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
- 没有日志、版本或可追溯记录；
- 没有暂停、纠错或回滚责任人；
- 无法评估模型输出质量；
- 成本没有上限、预算责任人或停用条件；
- 仍是演示系统，却被宣传为已具备生产条件。

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
ai-ready report examples/sample_assessment.json --format html --output examples/reports/sample_assessment_report.html
ai-ready migrate legacy-v05.json --output assessment-v06.json
```

v0.6 要求 `schema_version: "0.6"`。`migrate` 只把已知的无版本 v0.5 输入复制到新文件并补上版本号，不改原文件、评分、证据或复核声明；HTML 报告无脚本并转义输入文本。

它的作用不是替代治理判断，而是把 readiness review 的输入结构化，输出一个可复核的评分和文本/JSON/Markdown/静态 HTML 报告。
