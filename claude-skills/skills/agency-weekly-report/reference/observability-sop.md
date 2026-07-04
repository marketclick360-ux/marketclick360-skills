# Observability SOP

## The five layers

| Layer | Cadence | Audience | Content |
|---|---|---|---|
| Heartbeats | Every 15 min | Machines → operator on failure | Agent/gateway liveness, connection health |
| Daily digest | Daily, one email | Operator (all clients) | Tasks done, errors, review-queue items, anomalies ≥40% vs. baseline |
| Weekly client report | Monday | Client | See report-formats.md |
| Monthly value summary | Monthly (Core/Embedded) | Client | See report-formats.md |
| Incident notice | On client-visible failure | Client | Proactive, within 4 business hours |

## Metrics tracked per client

- Tasks completed, by type
- Items escalated to human review
- Response/turnaround times
- Error count and class
- Volume trends vs. baseline

Value metrics = usage metrics × the client's own unit economics from intake
(lead value, customer value, close rate). Always cite the client's number as
the source.

## Escalation rules

1. Heartbeat failure → alert operator immediately (client, agent, last-success
   time, probable cause).
2. Authorized auto-restart, once.
3. Still failing after 30 min unacknowledged → secondary-channel alert.
4. Client-visible error → operator notifies client proactively within 4
   business hours (fix + prevention included).
5. Daily digest missing → treat as system-down. The digest is the dead-man
   switch.
6. Outbound agent behaving anomalously → auto-pause its sends, queue for
   review, alert operator.

## Baselines

Shadow week (install Phase 5) records each client's normal volumes. Anomaly
detection compares against the trailing average; ±40% triggers a digest flag.
