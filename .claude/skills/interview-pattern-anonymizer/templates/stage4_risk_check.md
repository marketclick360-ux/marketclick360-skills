# Stage 4 Playbook — Identifiability Risk Check

Use ONLY the composite draft. Review it adversarially: assume the role of
someone motivated to trace it to a real person (a viewer who knows the
source interviews, a family member, the interviewee themselves).

## Inputs

- One composite draft from `outputs/composites/`.
- The review rules in `prompts/04_identifiability_risk_check.md` — answer
  its seven questions one by one and use its exact output format (risk
  rating, specific risk flags, safer replacement suggestions, final
  PASS/FAIL recommendation).

## Steps

1. Read the composite draft.
2. Answer all seven questions: single-source traceability, exact or rare
   details, memorable phrasing, rare-trait combinations, trauma
   specificity, insider recognition, real-person implication (including
   presence of the required label).
3. Judge combinations, not just single details. A narrow generalization is
   still identifying. Err on the side of flagging.
4. Rate Low / Medium / High. A Medium with unresolved flags is a FAIL.
5. Save the report to
   `outputs/risk_checks/risk_check__<composite-slug>.md`.
6. Then run the mechanical gate:
   `python src/validate_outputs.py`
   Both this validator and your PASS must agree before the draft is final.
7. In chat, report the rating, the flag count, and PASS/FAIL. On FAIL, set
   `NEXT_ACTION.md` to a Stage 3 revision citing the specific flags.

## Handoff

Update `PROJECT_STATE.md`, append to `RUN_LOG.md`, set `NEXT_ACTION.md`
(revision loop, or "composite final" when both gates pass).
