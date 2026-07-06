# Interview Anonymization & Composite Workflow

A reusable, fully local workflow for turning manually provided interview
transcripts into **fictionalized, anonymized composite profiles** built from
recurring cross-interview patterns — while minimizing re-identification risk
at every step.

Designed for Soft White Underbelly-style interview analysis, but generic
enough for any interview transcript set.

## What this project does

- Ingests local `.txt`/`.md` transcript files you place in `/transcripts`.
- Strips or flags obvious identifying metadata (URLs, timestamps, speaker
  labels, emails, phones, handles, exact ages/years/dates, likely
  names/places).
- Builds model-ready prompt packets for a four-stage Claude workflow:
  pattern extraction → cross-interview synthesis → composite generation →
  identifiability risk check.
- Validates finished drafts with a heuristic privacy scanner.

## What this project does NOT do

- It does **not** download YouTube videos, scrape websites, fetch
  transcripts, or call any external API. Everything runs locally on files
  you add by hand.
- It does **not** produce disguised summaries of real people. Composites are
  fictional illustrations of patterns that recur across **at least 3
  separate interviews**.
- It does **not** guarantee anonymity by itself. The scripts are guardrails;
  the Stage 4 risk check and your own judgment are the final gate.

## Ethical constraints (baked into every stage)

1. **Recurring patterns only** — a trait may appear in a composite only if it
   was found in **3+ separate interviews** (the minimum recurrence rule).
2. **No quotes, no close paraphrases** — source language never survives into
   outputs.
3. **No unique details** — no names, exact locations, exact ages, exact
   dates, rare jobs, rare family structures, unique trauma details,
   distinctive events, or memorable phrases.
4. **No rare-detail fingerprints** — individually safe details must not be
   combined into a profile that is still identifiable.
5. **No real-person implication** — every composite carries the label
   *"Fictionalized anonymized composite"* and never claims to be real.
6. **Default to caution** — when in doubt, generalize or exclude.

## Folder structure

```
interview-anonymization-composites/
├── transcripts/                  # YOUR input .txt/.md files (git-ignored)
│   └── README.md
├── prompts/                      # Stage templates used by the packet builder
│   ├── 00_domain_context.md      # optional per-domain framing (editable)
│   ├── 01_extract_patterns.md
│   ├── 02_cross_interview_synthesis.md
│   ├── 03_composite_generation.md
│   └── 04_identifiability_risk_check.md
├── outputs/                      # All generated/working files (git-ignored)
│   ├── prepared_transcripts/     # cleaned, chunked transcripts
│   ├── prompt_packets/           # ready-to-paste Claude prompts
│   ├── pattern_maps/             # save Stage 1 outputs here
│   ├── synthesis_maps/           # save Stage 2 outputs here
│   ├── composites/               # save Stage 3 outputs here
│   └── risk_checks/              # save Stage 4 outputs + validator reports
├── src/
│   ├── prepare_transcripts.py
│   ├── build_prompt_packets.py
│   └── validate_outputs.py
├── README.md
├── requirements.txt              # empty on purpose — stdlib only
└── .gitignore                    # keeps transcripts & outputs out of git
```

## Requirements

Python **3.11+**. No external packages, no network access, no services.

## How to add transcripts

Copy your transcript files into `/transcripts` as `.txt` or `.md`. One file
per interview. `README.md` in that folder is skipped automatically. Originals
are never modified.

## How to run each script

All commands run from the project root (`interview-anonymization-composites/`).

| Command | What it does |
|---|---|
| `python src/prepare_transcripts.py` | Cleans and chunks transcripts into `outputs/prepared_transcripts/`. Add `--chunk-words 1000` to change chunk size. |
| `python src/build_prompt_packets.py` | Builds Stage 1–4 prompt packets into `outputs/prompt_packets/`. |
| `python src/validate_outputs.py` | Scans `outputs/composites/` and `outputs/risk_checks/` for privacy problems and saves a report. |

## How to use the prompt packets with Claude

Each packet in `outputs/prompt_packets/` is a single markdown file meant to
be pasted whole into a Claude conversation:

- **`stage1_extract__<interview>.md`** — one per interview. Contains the
  extraction instructions plus that interview's prepared chunks. Paste one
  packet per conversation; save each response as a markdown file in
  `outputs/pattern_maps/`.
- **`stage2_synthesis.md`** — contains the synthesis instructions plus a
  paste slot for each Stage 1 pattern map. Fill the slots, paste the whole
  thing, save the response to `outputs/synthesis_maps/`.
- **`stage3_composite.md`** — paste your Stage 2 synthesis map into its slot,
  run it, save the response to `outputs/composites/`.
- **`stage4_risk_check.md`** — paste a composite draft into its slot, run it,
  save the response to `outputs/risk_checks/`.

Every packet reminds the model that source text is private working material
that must never be quoted in final outputs.

### Domain context (optional)

If `prompts/00_domain_context.md` exists, the packet builder embeds it in
every packet so all four stages share the same framing: what the interview
set is about, which theme areas to watch for, and any domain-specific
identifier risks beyond the standard rules. The included version is tuned
for Soft White Underbelly-style interviews (addiction, homelessness, sex
work, incarceration, recovery — where aliases, named facilities, gang
references, and recognizable public story beats are all treated as
identifying). Edit or delete that file when working with a different
transcript set.

## Using the Claude Skill (recommended for repeated use)

This repository ships a companion Skill at
`.claude/skills/interview-pattern-anonymizer/` that turns the workflow into
small, stateless Claude Code chats instead of one long conversation:

- **The Skill is the reusable brain** — stage playbooks, privacy checklist,
  token-saving checklist. It contains no transcripts and no private data.
- **This project folder is the memory** — four git-ignored handoff files
  keep state between chats: `PROJECT_STATE.md` (current truth),
  `RUN_LOG.md` (append-only log), `NEXT_ACTION.md` (the single next task,
  readable with zero context), and `MANIFEST.csv` (one row per interview,
  neutral IDs only — never titles, URLs, or names).
- **Each chat does one stage for one unit of work**: extract one pattern
  map, or synthesize, or draft one composite, or run one risk check. After
  Stage 1, raw transcripts are never opened again; each later stage reads
  only the previous stage's output file.

To use it: open a Claude Code session in this repository and say what you
want (e.g. "process the next transcript" or invoke
`/interview-pattern-anonymizer`). Claude reads `NEXT_ACTION.md`, does that
one task, saves results into `outputs/`, updates the handoff files, and
tells you what the next chat should do. The Python scripts and the
paste-into-Claude prompt packets in `outputs/prompt_packets/` still work
exactly as described below — the Skill simply automates the same stages
inside Claude Code.

## Recommended workflow

**Step 1** — Place local transcript `.txt` or `.md` files in `/transcripts`.

**Step 2** — Run:
```
python src/prepare_transcripts.py
```

**Step 3** — Run:
```
python src/build_prompt_packets.py
```

**Step 4** — Paste each Stage 1 prompt packet into Claude to create
individual pattern maps. Save them to `outputs/pattern_maps/`.

**Step 5** — Paste the Stage 1 outputs into the Stage 2 synthesis prompt
packet and run it. Save the result to `outputs/synthesis_maps/`.

**Step 6** — Use the Stage 3 prompt packet (with the synthesis map pasted in)
to generate the anonymized fictional composite. Save it to
`outputs/composites/`.

**Step 7** — Use the Stage 4 prompt packet to perform a re-identification
risk check on the composite. Save it to `outputs/risk_checks/`.

**Step 8** — Make sure all outputs are saved into the correct `/outputs`
folders (the validator only sees what's there).

**Step 9** — Run:
```
python src/validate_outputs.py
```

If the validator or the Stage 4 check flags anything, revise the composite,
then repeat Steps 7–9 until it passes.

## How to validate outputs

`validate_outputs.py` scans every `.md`/`.txt` file in `outputs/composites/`
and `outputs/risk_checks/` for: long direct quotes, exact ages, exact years,
exact dates, specific locations, name-like phrases, URLs, phone numbers,
emails, social handles, leftover `[FLAG:...]` markers, wording that implies a
real person, a missing "Fictionalized anonymized composite" label, and
overly specific biographical combinations. It prints a plain-English report
and saves a timestamped copy to `outputs/risk_checks/`.

The validator is a tripwire, not a guarantee: **a clean scan does not prove a
composite is safe** — it means no obvious machine-detectable problem was
found. The Stage 4 review is still required.

## How to interpret risk ratings

Stage 4 rates each composite **Low / Medium / High**:

- **Low** — pattern-level throughout; no plausible path from the profile to
  any one person. Publishable after a final human read.
- **Medium** — mostly safe, but specific elements need further
  generalization. Treat as **not publishable** until every flag is resolved
  and the check is re-run.
- **High** — at least one element could plausibly identify a source
  interview or person. Do not publish; rewrite the flagged material from the
  pattern level up.

A Medium rating with unresolved flags is a FAIL. When in doubt, revise and
re-check — composites are cheap to rewrite; privacy failures are not
reversible.

## Limitations

- Regex-based cleaning and validation are heuristics. They over-flag on
  purpose and can still miss identifiers written in unusual ways — human
  review is part of the workflow, not optional.
- The minimum-recurrence rule needs at least 3 interviews; the scripts warn
  when the set is smaller.
- The scripts prepare and check material; the analytical stages (1–4) are
  performed by you pasting packets into Claude, so their quality depends on
  following the packet instructions faithfully.
