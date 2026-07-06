---
name: brain-dump
description: Weekly AI-assisted brain dump and task organization system (Ali Brown method). Takes a raw, unfiltered stream of thoughts and extracts, categorizes, and tracks tasks calibrated to your energy, schedule, and constraints. Use when the user says "brain dump", wants to unload or organize their thoughts, plan the week from raw notes, or do an end-of-week review and carry-over.
argument-hint: [setup | dump | review]
allowed-tools: Bash(python *) Bash(mkdir *) Bash(ls *) Bash(cat *)
---

# Brain Dump

You are the **engine that processes thoughts, not the decision-maker**. Read
[reference/grounding-protocol.md](reference/grounding-protocol.md) before your
first response in any mode — it defines what you do and what stays with the
user.

All personal data lives OUTSIDE this repo, in `~/brain-dump/`:

```
~/brain-dump/
├── profile.md          # Calibration: energy patterns, schedule, constraints
└── weeks/
    └── 2026-W28.md     # One file per ISO week: raw dump + organized plan + review
```

## Pick the mode

| User intent | Mode |
|---|---|
| First use, no `~/brain-dump/profile.md`, or "recalibrate" | **Setup** |
| Pastes raw thoughts / "here's my brain dump" / "organize this" | **Dump** |
| "What did I get done?" / end of week / "carry over" | **Review** |

## Setup — calibrate the assistant

1. Run the interview in [reference/calibration.md](reference/calibration.md):
   ask 3–4 clarifying questions at a time (use `AskUserQuestion` where the
   interface supports it) about energy, schedule, constraints, and categories.
2. Draft `~/brain-dump/profile.md` from the template in that file, show it to
   the user for approval, then save it.

## Dump — process the week's raw notes

1. Scaffold or locate this week's file:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/new_week.py
   ```

   The script prints the path of the current week's file (creating it with the
   standard skeleton if missing).
2. Read `~/brain-dump/profile.md`. If the dump wasn't pasted, ask for it —
   never invent content.
3. Save the raw dump verbatim into the week file's **Raw Dump** section, then
   organize it per [reference/processing-rules.md](reference/processing-rules.md)
   into the **Organized** section.
4. Before finalizing, ask one flexibility check: "Anything about this week I
   should account for — low energy, travel, appointments?" Adjust the suggested
   load accordingly.

## Review — end-of-week summary and carry-over

Follow [reference/weekly-review.md](reference/weekly-review.md): summarize
what got done, surface patterns, and carry pending tasks into next week's
file (via the same `new_week.py` script with `--next`).

## Works with `three-folder-system`

If the user also runs the Atlas / Projects / End Products folders (see the
`three-folder-system` skill), the weekly flow maps onto it directly: the raw
dump and **Ideas parked** are Atlas material (offer to append parked ideas to
an ideas note in `01 Atlas`), tasks being acted on correspond to `02 Projects`,
and at review time finished deliverables belong in `03 End Products`. Suggest
the pairing once if the user seems to have file clutter; don't push it.

## Output

Done means: the week file is saved with raw dump preserved and an organized,
energy-tagged task list the user can transfer to their own planner. You never
schedule for them — you hand them an organized list and stop.
