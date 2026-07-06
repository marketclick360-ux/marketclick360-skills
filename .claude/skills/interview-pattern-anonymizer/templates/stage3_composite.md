# Stage 3 Playbook — Generate a Fictionalized Anonymized Composite

Use ONLY the synthesis map. Never reopen pattern maps or transcripts here.

## Inputs

- The latest synthesis map in `outputs/synthesis_maps/`.
- The generation rules in `prompts/03_composite_generation.md` — follow its
  five required sections (A. Composite Profile, B. Source-Derived Pattern
  Basis, C. Fictionalized Connective Tissue, D. Details Intentionally
  Excluded, E. Re-identification Risk Notes) exactly.

## Steps

1. Read the synthesis map, including its anonymization guidance.
2. Write a 500–900 word documentary-style composite that begins with the
   required label:
   > **Fictionalized anonymized composite.** This profile does not describe
   > a real person. It is a fictional illustration of patterns that
   > recurred across multiple interviews.
3. Build source-derived elements ONLY from themes that met the 3-interview
   threshold. Everything that makes it read as one life — sequence, scenes,
   persona — is invented connective tissue, listed in Section C.
4. No quotes, no close paraphrases, no exact ages/dates/locations, no real
   or similar names, humane non-voyeuristic tone throughout.
5. Self-check before saving: could any single source interviewee read this
   and reasonably say "that's me"? If yes, generalize and rewrite.
6. Save to `outputs/composites/composite__<slug>__draft01.md` (increment
   the draft number on revisions).
7. In chat, report the file path and word count. Do not paste the full
   profile unless the user asks.

## Handoff

Update `PROJECT_STATE.md`, append to `RUN_LOG.md`, set `NEXT_ACTION.md` to
Stage 4 with the draft's path.
