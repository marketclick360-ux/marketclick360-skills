# Weekly Review

Run at end of week (or whenever the user asks "what did I get done" /
"carry over"). Requires this week's file; if it doesn't exist, say so and
offer to start with a dump instead.

## Step 1 — Ask for actuals

The week file's checkboxes are usually stale (the user works from their own
planner). Show the organized task list and ask which items got done, partially
done, or dropped. Update the checkboxes from their answer — never assume.

## Step 2 — Summarize

Write a `## Review` section at the bottom of the week file:

```markdown
## Review — {date}

### Done
- {task} {category}

### Carried to next week
- {task} — {why it slipped, one phrase, no judgment}

### Dropped on purpose
- {task}

### Patterns
{1–3 observations max, only if genuinely there. e.g. "Both 🔥 tasks slipped
again — consider breaking them smaller." Skip this section rather than
manufacture insight.}
```

Tone check: a light week is data, not failure. No productivity guilt.

## Step 3 — Carry over

1. Scaffold next week's file:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/new_week.py --next
   ```

2. Copy carried tasks into its `## Organized` section under their categories,
   keeping their tags. A task carried **three weeks running** gets flagged:
   ask whether to break it down, delegate it, or delete it — the user decides.
3. Parked ideas do NOT carry automatically — they live in the week they were
   born. Mention any idea the user seemed excited about and ask if it should
   become a task.

## Step 4 — Close

One-line send-off summarizing the week ("6 done, 2 carried, load was
realistic"), then stop. Next week's planning happens at next week's dump.
