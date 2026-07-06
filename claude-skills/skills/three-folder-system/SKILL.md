---
name: three-folder-system
description: Dan Harrison's three-folder file organization system — Atlas (thinking), Projects (building), End Products (finished). Use when the user wants to organize files or a messy workspace, set up Atlas/Projects/End Products folders, sort a cluttered directory or drive, triage downloads, or asks "where should this file go".
argument-hint: [setup | cleanup | maintain] [directory]
allowed-tools: Bash(python *) Bash(ls *) Bash(mkdir *) Bash(find *)
---

# Three-Folder System

Every file is exactly one of three things. That's the whole system:

| Folder | Question it answers | What lives there |
|---|---|---|
| **01 Atlas** (thinking) | "Is it just an idea or raw material?" | Notes, brainstorms, clippings, idea dumps, rough strategic drafts |
| **02 Projects** (building) | "Am I working on it right now?" | Anything actively in progress |
| **03 End Products** (heart) | "Is it finished?" | Final, polished, exported, delivered |

If a file doesn't fit cleanly, that's not a filing problem — it means the plan
for that item isn't clear yet. Say so; the friction is the feature (it lets
the user "debug" their workflow).

## Pick the mode

| User intent | Mode |
|---|---|
| "Set this up" / folders don't exist yet | **Setup** |
| "Sort this mess" / existing clutter | **Cleanup** |
| "Keep it clean" / periodic triage / "where does X go" | **Maintain** |

## Setup

Ask which workspace to restructure (a directory, Drive, Notion — this skill
handles local directories; for cloud tools, output the structure for the user
to create). Then scaffold:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/triage.py init --base "<workspace>"
```

Explain the flow in one breath: new stuff → Atlas; acting on it → Projects;
done → End Products, then archive/delete the temporary project files.

## Cleanup — sort existing clutter

1. Inventory what's there (prints name, type, size, last modified — nothing is
   read or moved):

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/triage.py scan --base "<workspace>"
   ```

2. Propose a sort using [reference/sorting-rules.md](reference/sorting-rules.md)
   — for **every file**: destination + a one-line *why*. Items that don't fit
   go in an explicit **Unclear — needs a decision** list with the question
   that would resolve each ("is the Q3 deck still being edited, or shipped?").
3. Get approval, then apply. The script dry-runs by default; `--yes` moves:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/triage.py apply plan.tsv --base "<workspace>"        # preview
   python ${CLAUDE_SKILL_DIR}/scripts/triage.py apply plan.tsv --base "<workspace>" --yes  # move
   ```

   Never pass `--yes` without the user having seen the plan.

## Maintain

For "where does X go", answer with the three questions above and one-line
reasoning. For recurring tidiness, re-run **Cleanup** on the loose files —
or offer to set up a scheduled triage (a cron/skill invocation that runs
`scan` and proposes sorts periodically); build that only if the user says yes.

## Works with `brain-dump`

The two skills share a philosophy (AI organizes, user decides) and a pipeline:
parked ideas from a brain dump are Atlas material, this week's active tasks
are Projects material, and finished deliverables land in End Products. See
that skill for the weekly capture side.

## Output

Done means: the three folders exist, every file the user approved has moved,
and the **Unclear** list (if any) has been handed back as decisions to make —
not silently filed somewhere plausible.
