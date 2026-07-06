# Stage 1 Playbook — Extract a Pattern Map from ONE Transcript

Process exactly one interview in this chat. Never load more than one.

## Inputs

- One interview's prepared chunks from `outputs/prepared_transcripts/`
  (same file stem, `_partNN` suffixes). If none exist yet, run
  `python src/prepare_transcripts.py` first.
- The extraction rules in `prompts/01_extract_patterns.md` — follow that
  template's headings and prohibitions exactly.
- Domain framing in `prompts/00_domain_context.md` if present.

## Steps

1. Pick the next unprocessed interview from `MANIFEST.csv` (or ask the user
   which one if the manifest is empty).
2. Read that interview's prepared chunks only.
3. Produce the ten-section pattern map defined in
   `prompts/01_extract_patterns.md`: broad background patterns,
   family/social context, economic pressures, adversity themes,
   coping/survival strategies, emotional patterns, turning points, systemic
   factors, excluded identifying details (category-level log only), and
   uncertainty notes.
4. Treat every `[FLAG:...]` span in the source as identifying: generalize
   or exclude it. No quotes, no close paraphrases, no exact
   ages/places/dates, no unique incidents.
5. Save the pattern map to
   `outputs/pattern_maps/pattern_map__<interview_id>.md`.
6. Do NOT echo transcript text into chat — report the output file path and
   a 3–5 line summary of theme areas found (themes only, no details).

## Handoff

Mark `stage1_done` in `MANIFEST.csv`, update `PROJECT_STATE.md`, append to
`RUN_LOG.md`, and set `NEXT_ACTION.md` (next interview, or Stage 2 once at
least 3 pattern maps exist).
