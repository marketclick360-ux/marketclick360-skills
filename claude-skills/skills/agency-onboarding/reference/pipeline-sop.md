# Install Pipeline SOP

`intake → scope → provision → agents-build-agents → shadow week → go-live`

Target operator time per install: ≤7 hours total, spread over ~3 weeks.

## Contents
- [Phase 1 — Intake](#phase-1--intake)
- [Phase 2 — Scope](#phase-2--scope)
- [Phase 3 — Provision](#phase-3--provision)
- [Phase 4 — Agents-build-agents](#phase-4--agents-build-agents)
- [Phase 5 — Shadow week](#phase-5--shadow-week)
- [Phase 6 — Go-live](#phase-6--go-live)

## Phase 1 — Intake
- **Objective:** Capture everything needed to design the AI employee, in one pass.
- **Entry:** Qualified lead; discovery call done or booked.
- **Tasks:** Send intake link (operator, 2 min) → client completes form → agent produces profile + gaps + red flags + access checklist → operator reviews red-flag report (10 min).
- **Deliverables:** Structured intake profile; red-flag report; access checklist.
- **Done:** No unresolved gaps on scoped-workflow questions; red flags cleared or deal declined.
- **Checklist:** ☐ Discovery transcript in vault ☐ Intake complete ☐ Profile generated ☐ Gaps chased ☐ Red flags cleared ☐ Client vault created.

## Phase 2 — Scope
- **Objective:** Workflow maps → tier-fitted scope → signed proposal.
- **Entry:** Phase 1 done.
- **Tasks:** Agent maps + ranks workflows → operator selects workflows + tier (20 min) → agent drafts scope + proposal → operator edits/prices/sends (20 min) → client signs.
- **Deliverables:** Workflow maps (deposited to library); scope doc; signed proposal.
- **Done:** Signed proposal AND first payment received.
- **Checklist:** ☐ Maps in library ☐ Tier fits the rules ☐ Exclusions explicit ☐ Signed ☐ Paid ☐ Kickoff booked.

## Phase 3 — Provision
- **Objective:** Client environment: vault, tool connections, permissions.
- **Entry:** Signed + paid; kickoff done.
- **Tasks:** Kickoff call (operator, 30 min) → access checklist sent (agent drafts) → client grants access → connections configured → **GATE 2:** operator verifies each connection + approves permission grants (15 min).
- **Deliverables:** Populated vault; working authenticated connections; permissions log.
- **Done:** Every scoped tool passes a test call; permissions logged at minimum-necessary.
- **Checklist:** ☐ Vault populated ☐ Connections green ☐ Minimum permissions verified ☐ SPOC confirmed ☐ Timeline sent.

## Phase 4 — Agents-build-agents
- **Objective:** Design and assemble the client's production agents from the skills library.
- **Entry:** Provisioning done.
- **Tasks:** Agent drafts specs → **GATE 1:** operator reviews/approves specs (30 min) → builder assembles from library → QA runs test suite → operator reviews failures + fixes (30–60 min).
- **Deliverables:** Approved specs (→ library); built agents; build log with reuse %; QA report.
- **Done:** All test cases pass including adversarial cases; every outbound path has a human-review queue.
- **Checklist:** ☐ Specs approved ☐ Reuse logged ☐ New components deposited ☐ QA green ☐ Review queues on.

## Phase 5 — Shadow week
- **Objective:** Run on real inputs with ZERO client-visible output; find and fix top failure modes.
- **Entry:** QA green.
- **Tasks:** Agents run in shadow (outputs → operator only) → daily output diff vs. expected → operator reviews daily (15–20 min/day) → **GATE 3:** operator approves fixes → metrics baselined.
- **Deliverables:** Shadow-week report; fix log; metric baselines.
- **Done:** Two consecutive clean shadow days; top 3 failure clusters fixed; baselines recorded.
- **Checklist:** ☐ 5+ shadow days ☐ Daily diffs reviewed ☐ Top failures fixed ☐ 2 clean days ☐ Baselines stored ☐ Go-live email drafted.

## Phase 6 — Go-live
- **Objective:** Production on, watchdogs on, reporting scheduled.
- **Entry:** Shadow-week done criteria met.
- **Tasks:** **GATE 4:** operator flips production (10 min) → heartbeats/alerts/digest activated → first weekly report scheduled → go-live email approved + sent → 48-hour heightened watch.
- **Deliverables:** Live AI employee; active observability; go-live email; report schedule.
- **Done:** 48 clean production hours; heartbeats green; first weekly report delivered on time.
- **Checklist:** ☐ Production on ☐ Heartbeats green ☐ Client in daily digest ☐ Report scheduled ☐ 48-hr watch passed ☐ Install retro done (what to templatize).
