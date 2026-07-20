# AI Prototype-to-Production Toolkit(AI 原型→生产就绪度工具包)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
![GitHub release](https://img.shields.io/github/v/release/Anonymousyz/ai-prototype-to-production-toolkit)
[![validate](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit/actions/workflows/validate.yml)

[English README](README.md) · [10 分钟中文上手](docs/quickstart_zh.md)

一个本地优先的工具包,用来回答一个具体的运营问题:

> AI 原型在演示里跑通了。在允许它影响真实业务流程之前,还需要哪些**证据、控制手段和决策权责**?

评审对象不是抽象的模型,而是一个有用户、有输入来源、有决策点、有受影响方、有运行负责人、有失败路径的 **AI 业务流程**。模型跑分只是其中一项输入;数据授权、评估证据、人工复核设计、审计日志、成本、事故归属和回滚同样决定这个流程能不能上。

> [!IMPORTANT]
> 评分是作者自行设计的决策支持启发式,**未经外部校准**。它不认证安全、合规、公平,也不构成上线批准。CLI 只校验申报的结构;它不核实证据真伪、评审人身份或真实运行表现。使用前请读[方法边界](docs/method_status.md)。

## 核心命题

> **演示证明可能性,生产要求问责。**

```text
生产就绪的 AI = 业务流程 + 证据 + 治理 + 问责
```

## 60 秒试用

```bash
python -m pip install "https://github.com/Anonymousyz/ai-prototype-to-production-toolkit/releases/download/v0.6.0/ai_ready-0.6.0-py3-none-any.whl"
ai-ready example --output assessment.json
ai-ready report assessment.json --format html --output report.html
```

打开 `report.html`,查看申报得分、否决状态、各维度缺口和人工复核负责人。本地源码安装则用 `pip install -e .`。

`ai-ready score examples/sample_assessment.json` 的预期输出:

```text
System: Fictional Supplier Document Assistant
Stage: controlled pilot review
Review owner: Fictional cross-functional pilot review committee
Reviewed at: 2026-07-15
Decision: Controlled pilot only
Total: 42/70
Normalized: 42/70 (60.0%)
Veto: no
Top gaps:
- Evaluation set is too small
- Audit log design is incomplete
- Rollback owner is unclear
```

## 评审框架:七个维度

一个原型只有在团队能回答完这七类问题后,才谈得上生产就绪:

```mermaid
flowchart LR
  A[AI 演示] --> B[业务流程映射]
  B --> C[数据边界审查]
  C --> D[评估计划]
  D --> E[人工复核设计]
  E --> F[权限·日志·可审计]
  F --> G[运维·成本·回滚]
  G --> H[试点决策]
  H --> I[小规模生产试验或返工]
```

| 评审层 | 团队必须回答 | 对应产物 |
|---|---|---|
| 业务流程与价值 | 哪个决策或任务被改变?价值和损害如何观测? | 流程图、调研指南、试点备忘录 |
| 数据与授权 | 系统可以读取、留存、外发什么?禁止什么? | 数据边界申报、AI 系统卡 |
| 输出质量与评估 | 什么算合格输出、失败、回归、不可接受的风险? | 评估计划、测试用例、缺口清单 |
| 人工复核与责任链 | 谁能批准、推翻改判、升级上报、暂停、叫停?出错谁负责? | 复核设计、否决记录、决策负责人 |
| 运行 | 权限、日志、成本、事故、监控、回滚归谁? | 风险登记册、运行手册输入 |

## 分数如何变成决策标签

CLI 把七个固定满分的维度加总,然后按顺序应用两条规则:**任何一条否决为真,总分再高也拦下**;没有否决时,总分才映射到讨论档位。

```mermaid
flowchart TB
    subgraph dims["七个维度,固定满分,共 70 分"]
        direction LR
        D1["业务流程与价值 10"]
        D2["数据授权与边界 12"]
        D3["输出质量与评估 12"]
        D4["人工复核与责任链 10"]
        D5["权限·日志·可审计 10"]
        D6["集成·运维·成本 10"]
        D7["组织采纳与改进 6"]
    end
    dims --> V{"8 条否决任一为真?<br/><i>未经授权使用数据 · 敏感数据入未批准模型 ·<br/>高风险决策无人工复核 · 无日志 ·<br/>无回滚负责人 · 输出质量不可评估 ·<br/>成本失控 · 演示冒充生产</i>"}
    V -- "是" --> STOP["不得推进:存在否决项<br/>(无论总分多少;退出码 1)"]
    V -- "否" --> T{"总分(归一化到 70)"}
    T -- "≤ 25" --> R1["仅限演示"]
    T -- "> 25, ≤ 45" --> R2["仅限受控试点"]
    T -- "> 45, ≤ 60" --> R3["小规模生产试验,<br/>须带监控"]
    T -- "> 60" --> R4["生产就绪度较强,<br/>控制项仍须核查"]
```

档位是给评审会议用的讨论标签,不是批准;档位边界有回归测试锁定。

## 快速开始

### 方式 A:工作坊(不写代码)

1. 复制[就绪度检查清单](templates/ai_prototype_readiness_checklist.md),团队各角色对照打分([计分卡](scorecards/ai_prototype_readiness_scorecard.md));
2. 填写[风险登记册](templates/risk_register.md)与 [AI 系统卡](templates/ai_system_card.md);
3. 用[试点评审备忘录](templates/pilot_review_memo.md)形成书面决定。

### 方式 B:CLI

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
ai-ready score examples/sample_assessment.json
ai-ready report examples/sample_assessment.json --format html --output report.html
ai-ready migrate legacy-v05.json --output assessment-v06.json
```

命令、退出码、v0.5 迁移与输入契约见 [`docs/cli.md`](docs/cli.md);输入文件接受带或不带 BOM 的 UTF-8。

## 四个虚构案例

| 案例 | 演示的行为 |
|---|---|
| [供应商文档助手](examples/sample_assessment.json) | 42/70,受控试点档 |
| [内部制度检索助手](examples/internal_policy_search_assistant.json) | 52/70,小规模生产试验档(四例中就绪度最高) |
| [客服自动操作代理](examples/customer_support_action_agent.json) | 触发两条否决,无论总分多少均判"不得推进",退出码 1 |
| [工业安全规程助手](examples/synthetic_industrial_safety_procedure_assistant.json) | 受监管流程语境,44/70 |

案例全部虚构,不含任何客户、雇主或真实运营数据。

## 仓库地图(节选)

| 用途 | 位置 |
|---|---|
| 方法立场与论文式阐述 | [`MANIFESTO.md`](MANIFESTO.md)、[`docs/production_ready_ai_thesis.md`](docs/production_ready_ai_thesis.md) |
| 检查清单与计分卡 | [`templates/`](templates/)、[`scorecards/`](scorecards/) |
| CLI 源码与 JSON Schema | [`src/ai_ready`](src/ai_ready)、[`schemas/readiness_assessment.schema.json`](schemas/readiness_assessment.schema.json) |
| NIST AI RMF / OWASP LLM Top 10 对照 | [`docs/nist_ai_rmf_crosswalk.md`](docs/nist_ai_rmf_crosswalk.md)、[`docs/owasp_llm_top10_mapping.md`](docs/owasp_llm_top10_mapping.md) |
| 评估结果→就绪证据的受控接入 | [`integrations/promptfoo/`](integrations/promptfoo/) |
| 就绪评估→决策包的交接 | [`docs/readiness_to_decision_handoff.md`](docs/readiness_to_decision_handoff.md) |
| 方法边界与校准路线 | [`docs/method_status.md`](docs/method_status.md)、[`docs/roadmap.md`](docs/roadmap.md) |
| 持续集成 | [`.github/workflows/validate.yml`](.github/workflows/validate.yml)(Python 3.9/3.11/3.12,每次 push 运行) |

配套仓库:先用 [Awesome AI Production Readiness](https://github.com/Anonymousyz/awesome-ai-production-readiness) 找工具补缺口,评估要变成负责人可拍板的决策包时用 [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit)。

## 边界

本工具包**不是**法律意见、安全审计、医疗或金融建议,不能替代专业合规审查,也不保证任何 AI 系统安全或可上线。70 分制固定但未校准;每个维度都要求列出证据引用,评审人姓名与日期为必填,八条否决必须逐条申报。这些是结构性检查:未解决的否决不能用高分抵消,CLI 也不核实证据与评审人身份。

## 许可证

MIT,见 [`LICENSE`](LICENSE)。
