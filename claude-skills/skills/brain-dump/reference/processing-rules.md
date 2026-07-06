# Processing Rules

How a raw dump becomes an organized week. Applied in **Dump** mode, always
with `~/brain-dump/profile.md` already read.

## Step 1 — Preserve

Paste the raw dump verbatim into the week file's `## Raw Dump` section. Never
edit, summarize, or "clean up" the original — it's the source of truth and
part of the point (the user re-reads it sometimes).

## Step 2 — Extract

Walk the dump line by line and pull out every:

- **Task** — anything with an implied action ("call the accountant", "fix the
  landing page hero")
- **Appointment** — anything with a date/time attached; these are facts, not
  tasks, and go in their own list
- **Idea** — "what if / someday / maybe" material; park it, don't task-ify it
- **Feeling** — stress, dread, excitement about specific responsibilities

One dump line can yield multiple items. Vague fragments ("dentist??",
"the Miller thing") go to **Needs clarification** — never guess.

## Step 3 — Filter

Feelings are handled per the profile preference:

- *Acknowledge briefly*: one sentence at the top of the organized output
  ("Noted: the client project is weighing on you — its tasks are flagged
  🔥 high-friction"). Then move on.
- *Filter silently*: drop them from the output entirely.

Either way, a feeling attached to a task is *metadata* (mark the task
high-friction), never a task itself.

## Step 4 — Categorize and tag

Sort tasks into the profile's categories. Tag each task:

| Tag | Meaning |
|---|---|
| ⚡ deep | Needs a peak-energy focus block |
| 🔁 light | Doable tired, in fragments, or while waiting |
| 🔥 friction | Emotionally loaded — pair with peak energy or break it down |
| 📅 {date} | Hard deadline (only if one actually exists — don't invent) |

## Step 5 — Reality check

Count the ⚡ deep tasks against the profile's realistic deep-focus hours and
this week's flexibility check ("low energy, travel, appointments?"). If the
list exceeds capacity, say so and propose — don't decide — what to defer,
starting with the profile's "first thing to drop".

## Output format (goes in the week file's `## Organized` section)

```markdown
### Appointments (transfer to your planner)
- {day date time} — {what}

### {Category 1}
- [ ] ⚡ {task} 📅 {date}
- [ ] 🔁 {task}

### {Category 2}
- [ ] 🔥⚡ {task}

### Ideas parked
- {idea}

### Needs clarification
- "{original fragment}" — what did you mean?

### Load check
{1–3 sentences: fits / doesn't fit this week's capacity, and the proposed
deferral if it doesn't.}
```

End by reminding the user to transfer appointments and chosen tasks into
their primary planner — that step is theirs.
