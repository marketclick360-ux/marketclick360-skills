---
name: agency-onboarding
description: Runs the MarketClick360 client install pipeline (intake → scope → provision → agents-build-agents → shadow week → go-live). Use when onboarding a new agency client, sending intake, drafting the access checklist or any phase's client email, or checking a phase's entry/done criteria.
argument-hint: [client-name] [phase]
---

# Agency Client Onboarding

Run one phase of the install pipeline for a client. Every phase: agents draft,
the operator approves. Nothing client-facing sends without operator sign-off.

## Steps

1. Identify the client and the current phase. Check the phase's **entry
   criteria** in [reference/pipeline-sop.md](reference/pipeline-sop.md) before
   doing anything — if entry criteria aren't met, report what's missing and stop.
2. Execute the phase tasks per the SOP. Use the exact client email wording from
   [reference/comms-templates.md](reference/comms-templates.md), filling
   placeholders from the client's vault.
3. For intake work (questions, red-flag scan, access checklist, AI-employee job
   description), use [reference/intake-system.md](reference/intake-system.md).
4. Verify **done criteria** and tick the internal checklist before declaring
   the phase complete. Deposit any new reusable artifact back into this repo.

## Approval gates (never skip)

- GATE 1: agent specs approved before build
- GATE 2: tool permissions approved before any live connection
- GATE 3: shadow-week fixes approved before applying
- GATE 4: operator personally flips production on

## Output

Phase marked done with its checklist complete, client comms drafted (queued for
operator approval, not sent), and the client vault updated with what happened.

## Client vault

Client context (facts, tone, tools, decisions, backlog) lives in the private
`marketclick360-ux/agency-vault` repo, operated per the `agency-client-vault`
skill. Read the client's `_CLIENT.md` card first — and `tone.md` before
drafting anything client-facing. Write decisions, commitments, and requests
back per that skill's Two-Output and propagation rules. Client data never
enters this public skills repo.
