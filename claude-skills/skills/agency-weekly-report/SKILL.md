---
name: agency-weekly-report
description: Drafts the Monday client-facing weekly report and runs the observability/retention layer for MarketClick360 clients — heartbeats, daily digest, monthly value summary, incident comms, escalation rules. Use when writing a weekly or monthly client report, setting up monitoring for a client, or handling a production incident.
argument-hint: [client-name]
---

# Weekly Report & Observability

The weekly report is the product the client experiences between deliverables —
it ships every Monday, no exceptions. Observability is what makes it truthful.

## Steps

1. **Weekly report:** draft per the exact structure in
   [reference/report-formats.md](reference/report-formats.md), using only
   metrics that actually exist (omit sections rather than estimate). Leave
   `{OPERATOR_NOTE}` for the operator's personal sentence. Queue for approval —
   never auto-send.
2. **Monthly value summary** (Core/Embedded tiers): same file, monthly format —
   $ impact computed only from the client's own unit economics, sources cited.
3. **Monitoring setup / incidents:** follow
   [reference/observability-sop.md](reference/observability-sop.md) — heartbeat
   cadence, daily digest contents, dead-man switch, escalation order, and the
   proactive incident-notice rule (the client never discovers a failure first).

## Output

A queued report draft (or a monitoring configuration / incident notice) with
every number traceable to the metric store.

## Client vault

Client context (facts, tone, tools, decisions, backlog) lives in the private
`marketclick360-ux/agency-vault` repo, operated per the `agency-client-vault`
skill. Read the client's `_CLIENT.md` card first — and `tone.md` before
drafting anything client-facing. Write decisions, commitments, and requests
back per that skill's Two-Output and propagation rules. Client data never
enters this public skills repo.
