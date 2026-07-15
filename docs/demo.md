# Demonstration cases

All examples are fictional and contain no customer or personal data.

| Case | Intended lesson | Command |
|---|---|---|
| Supplier document assistant | A middling score with no veto still means controlled pilot | `ai-ready score examples/sample_assessment.json` |
| Internal policy search assistant | A stronger score still requires ongoing controls | `ai-ready score examples/internal_policy_search_assistant.json` |
| Customer support action agent | A plausible score cannot override human-review and rollback vetoes | `ai-ready score examples/customer_support_action_agent.json` |

Generate comparable reports:

```bash
ai-ready report examples/sample_assessment.json --output supplier-report.md
ai-ready report examples/internal_policy_search_assistant.json --output policy-search-report.md
ai-ready report examples/customer_support_action_agent.json --output support-agent-report.md
```

The examples demonstrate decision logic; they are not claims of sector compliance or real deployment results.
