# 中文快速开始

这个工具包帮助团队检查：一个 AI 原型若要影响真实业务，还缺哪些材料和控制条件。

适用情形包括：

- 演示原型已经能运行，需要判断能否进入受控试点；
- 项目负责人需要把数据、评估、复核、运行和回滚条件写清；
- 风控、合规或审计人员需要据此提出问题并留下记录。

## 15 分钟完成一轮初步评审

1. 用 `templates/fde_discovery_interview_guide.md` 访谈业务方；
2. 用 `templates/ai_prototype_readiness_checklist.md` 逐项检查；
3. 用 `templates/risk_register.md` 记录风险、责任人和证据；
4. 用 `scorecards/ai_prototype_readiness_scorecard.md` 汇总讨论结果；
5. 用 `templates/pilot_review_memo.md` 写明下一步建议和待补事项。

## 档位说明

| 分数 | 评审含义 |
|---:|---|
| 0–25 | 仅供演示，不进入真实业务流程 |
| 26–45 | 可作为受控试点候选，先补齐缺口 |
| 46–60 | 可讨论小范围试运行，须明确监控和回滚 |
| 61–70 | 结构准备较充分，仍须逐项检查否决条件 |

档位只反映申报材料的结构，不是上线批准。

## 一票否决

以下任一情况出现时，应先解决问题，再讨论试点或上线：

- 数据授权不清；
- 敏感、个人或受监管数据进入未批准的外部模型；
- 高风险事项没有人工复核；
- 没有日志、版本或可追溯记录；
- 没有暂停、纠错或回滚责任人；
- 无法评估模型输出质量；
- 成本没有上限、预算责任人或停用条件；
- 演示系统被当作已具备生产条件的系统宣传。

## 使用边界

工具用于结构化讨论和试点前检查，不提供法律意见、合规认证或安全审计。它不核实材料中的事实，也不替代领域负责人作出的判断。

## CLI 用法

本仓库提供轻量 CLI：`ai-ready`。

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

v0.6 要求 `schema_version: "0.6"`。命令 `migrate` 只为已知的无版本 v0.5 输入补上版本号并写入新文件；它不改原文件、评分、证据或复核声明。HTML 报告不含脚本，并会转义输入文本。

CLI 把评审输入结构化，生成可复核的评分以及文本、JSON、Markdown 或静态 HTML 报告。