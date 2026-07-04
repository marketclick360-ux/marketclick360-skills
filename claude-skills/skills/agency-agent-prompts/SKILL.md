---
name: agency-agent-prompts
description: System prompts for the MarketClick360 internal agent bench — Master Client Success Agent, intake analysis, workflow mapping, scope builder, spec writer, automation builder, QA, observability, weekly report, repricing, and content repurposing agents. Use when instantiating an internal agency agent, writing a per-client master agent, or checking an agent's approval gates and failure modes.
argument-hint: [agent-name] [client-name]
---

# Agency Agent Prompts

Instantiate an internal agency agent from its canonical prompt. One Master
Client Success Agent exists per client; the rest are a shared bench.

## Steps

1. Pick the agent. Prompts live in:
   - [reference/master-csa.md](reference/master-csa.md) — per-client Master
     Client Success Agent + the client vault structure it depends on.
   - [reference/onboard-bench.md](reference/onboard-bench.md) — Intake
     Analysis, Workflow Mapping, Scope Builder, Agent Spec Writer,
     Automation Builder.
   - [reference/ops-bench.md](reference/ops-bench.md) — QA/Test,
     Observability, Weekly Report, Repricing/Renewal, Content Repurposing.
2. Copy the prompt, fill `{PLACEHOLDERS}`, and note the agent's **approval
   requirements** — they are part of the prompt, not optional.
3. Watch for the listed failure modes when reviewing the agent's output.

## Hard rules baked into every prompt

- Agents draft; the operator approves. No agent sends client-facing content.
- Pricing, renewals, and permission grants are operator-only.
- Missing information is reported as a gap, never invented.
- Every new reusable component gets deposited back into this repo.

## Client vault

Client context (facts, tone, tools, decisions, backlog) lives in the private
`marketclick360-ux/agency-vault` repo, operated per the `agency-client-vault`
skill. Read the client's `_CLIENT.md` card first — and `tone.md` before
drafting anything client-facing. Write decisions, commitments, and requests
back per that skill's Two-Output and propagation rules. Client data never
enters this public skills repo.
