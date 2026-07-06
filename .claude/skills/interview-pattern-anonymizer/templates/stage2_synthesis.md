# Stage 2 Playbook — Cross-Interview Synthesis

Use ONLY saved pattern maps. Never reopen raw or prepared transcripts in
this stage — if a pattern map seems thin, the fix is to redo Stage 1 for
that interview in a separate chat, not to peek at the source.

## Inputs

- All pattern maps in `outputs/pattern_maps/`.
- The synthesis rules in `prompts/02_cross_interview_synthesis.md` — follow
  its output format exactly (recurring-themes table, theme clusters,
  excluded-detail log, anonymization guidance).

## Preconditions

- At least 3 pattern maps must exist. With fewer, stop and tell the user
  the 3-source rule cannot be satisfied yet; set `NEXT_ACTION.md` to
  process more interviews.

## Steps

1. Read every pattern map in `outputs/pattern_maps/`.
2. Include a theme ONLY if the same generalized pattern appears
   independently in **3 or more separate interviews**. Count interviews,
   not mentions. Never merge two different rare details into a fake
   "shared" theme.
3. Label recurrence confidence High (5+ interviews or nearly all of a small
   set), Medium (3–4), or Low (3 with interpretive uncertainty).
4. Log excluded patterns at category level with the reason (below
   threshold, too specific, rare-combination risk).
5. Write anonymization guidance for Stage 3, including any set-specific
   risks (e.g. regional skew).
6. Save to `outputs/synthesis_maps/synthesis_map__<date>.md`.
7. In chat, report the file path, the number of themes that met the
   threshold, and the number excluded — no theme details needed beyond
   cluster names.

## Handoff

Update `PROJECT_STATE.md`, append to `RUN_LOG.md`, set `NEXT_ACTION.md` to
Stage 3 with the synthesis map's path.
