---
name: interview-pattern-anonymizer
description: Stage-by-stage workflow for turning manually provided interview transcripts into fictionalized anonymized composite profiles. Use when the user wants to analyze interview transcripts or channel-based transcript sets to extract recurring cross-interview patterns, generate anonymized composites, or run re-identification risk checks. One small stage per chat; project files are the memory.
---

# Interview Pattern Anonymizer

Use this Skill when the user wants to analyze interview transcripts (e.g.
long-form YouTube interview episodes provided as local text files) to extract
recurring patterns and create **fictionalized anonymized composite profiles**.

## Core purpose

Help the user process transcripts without overloading one chat. The project
files are the memory. Each chat completes ONE small task, saves the result to
a file, updates the handoff files, and leaves a clean starting point for the
next chat.

The companion project lives at `interview-anonymization-composites/` in this
repository. Its scripts do the mechanical work:

| Script | Purpose |
|---|---|
| `python src/prepare_transcripts.py` | clean + flag + chunk raw transcripts |
| `python src/build_prompt_packets.py` | build stage prompt packets |
| `python src/validate_outputs.py` | heuristic privacy scan of drafts |

Run all commands from the `interview-anonymization-composites/` directory.

## Non-negotiable rules

1. Analyze **transcripts only** — never raw video or audio.
2. Do NOT download videos, scrape websites, or fetch transcripts/captions
   from the internet. The user places transcript files in `transcripts/`
   manually.
3. Do NOT store transcripts, raw YouTube titles, video URLs, real names, or
   private outputs inside this Skill folder — they belong in the project
   folder, which is git-ignored.
4. Do NOT include raw YouTube metadata (titles, URLs, channel-specific
   episode identifiers) in prompt packets, manifests, or outputs by default.
   Use neutral interview IDs (`interview_01`, `interview_02`, ...).
5. Final outputs must never contain: direct quotes, close paraphrases, real
   names, exact locations, exact dates, exact ages, rare jobs or family
   structures, unique trauma details, distinctive events, or memorable
   phrases.
6. **The 3-source rule:** no detail may appear in a composite unless it
   recurs across at least 3 separate interviews.
7. Every composite must carry the label **"Fictionalized anonymized
   composite"** and must never imply it describes a real person.
8. Do not paste raw transcript text back to the user in chat. Refer to files
   by path.
9. Keep chat outputs compact and structured; write full results to files.
10. When in doubt, generalize or exclude.

## Workflow stages

Run exactly ONE stage per chat unless the user asks otherwise.

- **Stage 0 — Manifest:** create/update `MANIFEST.csv` (see
  `templates/stage0_manifest.md` conventions below; neutral IDs only).
- **Stage 1 — Extract:** one transcript → one pattern map.
  Playbook: `templates/stage1_extract_patterns.md`
- **Stage 2 — Synthesize:** all pattern maps → one synthesis map.
  Playbook: `templates/stage2_synthesis.md`
- **Stage 3 — Composite:** synthesis map → one composite draft.
  Playbook: `templates/stage3_composite.md`
- **Stage 4 — Risk check:** composite draft → risk report.
  Playbook: `templates/stage4_risk_check.md`
- **Stage 5 — Validate:** run `python src/validate_outputs.py` and act on
  findings. Both gates (validator + Stage 4 PASS at Low risk) must pass
  before a composite is final.

Before starting any stage, read `checklists/privacy_checklist.md` and
`checklists/token_saving_checklist.md`.

## Token-saving behavior

- Process one transcript at a time.
- Chunk long transcripts (the prepare script does this).
- After Stage 1, never touch raw transcripts again.
- Stage 2 uses ONLY saved pattern maps. Stage 3 uses ONLY the synthesis map.
  Stage 4 uses ONLY the composite draft.
- Progress lives in durable project files, not chat memory.

## Project memory (handoff files)

These live in the project root (`interview-anonymization-composites/`) and
are git-ignored because they may reference private working material. Create
them on first use if missing:

- **`PROJECT_STATE.md`** — current stage per interview, what exists in each
  outputs folder, open issues. Overwrite to reflect current truth.
- **`RUN_LOG.md`** — append-only log: date, action taken, files touched.
- **`NEXT_ACTION.md`** — the single next task, written so a brand-new chat
  can execute it without any other context.
- **`MANIFEST.csv`** — one row per interview, header:
  `interview_id,source_file,prepared,stage1_done,notes`
  Neutral IDs and local file names only — never titles, URLs, or names.

## Required handoff at the end of EVERY task

1. Update `PROJECT_STATE.md`, append to `RUN_LOG.md`, rewrite
   `NEXT_ACTION.md`, and update `MANIFEST.csv` when relevant.
2. End the chat with a short summary: what was completed, which files were
   created or changed, what the next chat should do, and any privacy
   warnings.
