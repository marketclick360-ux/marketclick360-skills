# Intake System

The live form is the `client-intake-form` repo. This file holds the question
bank, red-flag table, access checklist format, and the AI-employee job
description template.

## Contents
- [Form sections & questions](#form-sections--questions)
- [Red flags](#red-flags)
- [Access checklist format](#access-checklist-format)
- [AI Employee Job Description template](#ai-employee-job-description-template)

## Form sections & questions

**A. Business snapshot** — What do you sell, to whom? Team size/roles? Single
point of contact? What does a good month look like, in numbers?

**B. Pain deep-dive (the funnel)** — Brain-dump every repetitive weekly task
(unfiltered) → what falls through the cracks when busy → for each top pain
(max 3): describe it; frequency + duration; who handles it; walk through the
LAST time it happened; cost when done wrong/late ($ if possible); **why hasn't
it been fixed yet?**; which parts need human judgment vs. procedure. Then:
the revenue bottleneck question, the magic-wand question, the weekly-dread
question.

**C. Tool stack** — Email, CRM, calendar, messaging, docs, where leads arrive,
anything self-built/unusual, and **who can actually grant access**.

**D. Success metrics** — The 90-day proof number; lead value; customer value;
how it's measured today. (These become the weekly report's units and the
repricing evidence.)

**E. Compliance** — Regulated data (health/financial/minors)? Data that can't
leave their systems? Rules on customer contact? Who approves outbound?

**F. Working style & decision** — Update channel preference; honest response
speed; **who makes the final decision**; prior attempts and why they didn't
stick; budget comfort (anchored at $2.5k+).

## Red flags

| Red flag | Signal | Response |
|---|---|---|
| No measurable outcome | Can't answer any Section D question | Decline or convert to paid discovery |
| Access gatekeeping | "Our IT guy handles that, he's hard to reach" | Access becomes a signed precondition with named owner + date |
| Agency-hopper | 2+ prior vendors "who didn't get it" | Probe why; usually a management problem |
| Scope sprawl | 8+ workflows, all "top priority" | Force-rank; cap v1 at tier limits |
| Regulated-data core | Main workflow touches PHI/claims/financial advice | Decline politely pre-niche (marketing-adjacent is fine) |
| Micromanager | Daily calls, approval on everything | $8k tier or decline |
| Budget mismatch | Flinches at $2.5k anchor | Disqualify; never discount below $2.5k |

## Access checklist format

Per tool from Section C:
`☐ access level (read/send/admin) · ☐ who grants it · ☐ how (invite/API key/OAuth) · ☐ test performed · ☐ date granted · ☐ minimum-necessary confirmed`

## AI Employee Job Description template

> **Role:** {e.g., Lead Response & Follow-up Assistant}
> **Reports to:** {SPOC} (day-to-day), MarketClick360 (management, monitoring, training)
> **Responsibilities:** {3–5 bullets from scoped workflows, in the client's language}
> **Explicitly not responsible for:** {exclusions}
> **Hours:** 24/7, no sick days
> **Supervision:** Continuously monitored; written report every Monday; monthly improvement
> **Escalates to a human when:** {escalation triggers}
