# Calibration Interview

Run this once at first use, or whenever the user says "recalibrate" / their
circumstances change. The goal: enough context that weekly processing fits
*this* person, not a generic productivity template.

## How to run it

Ask in rounds of 3–4 questions (checkbox Q&A via `AskUserQuestion` where
supported). Stop as soon as you can fill the profile template — usually two
rounds. Don't interrogate.

### Round 1 — rhythm and energy

1. When in the day is your energy highest, and when does it reliably crash?
   (morning person / night owl / post-lunch dip / varies)
2. What does a typical week's fixed structure look like — recurring
   commitments, work blocks, family time, meetings that never move?
3. How many *deep-focus* hours can you realistically get in a good week?
4. Any standing constraints — health, caregiving, travel cadence, injury —
   that planning should always account for?

### Round 2 — categories and workflow

1. What buckets does your life naturally fall into? (e.g. Business, Clients,
   Family, Health, Ministry, Learning, Home) — these become the categories.
2. Where does your *real* schedule live — paper planner, Google Calendar,
   another app? (The skill only outputs lists; the user transfers them there.)
3. How do you want emotional content handled — acknowledged briefly, or
   silently filtered?
4. What does an overloaded week feel like, and what's the first thing you'd
   want dropped when one shows up?

### Optional round 3 — only if answers were vague

Probe whatever is still unclear: deadline sensitivity, how far ahead they
plan, whether appointments should get special treatment.

## Profile template

Draft this, show it for approval, then save to `~/brain-dump/profile.md`:

```markdown
# Brain Dump Profile
*Last calibrated: {date}*

## Energy pattern
- Peak: {when}
- Low: {when}
- Realistic deep-focus hours/week: {n}

## Fixed weekly structure
- {recurring commitment, day/time}
- ...

## Standing constraints
- {health / caregiving / travel / other — or "none"}

## Categories
1. {Category} — {one-line scope}
2. ...

## Preferences
- Primary planner: {paper / app} — skill outputs lists only, never schedules
- Emotional content: {acknowledge briefly / filter silently}
- First thing to drop in an overloaded week: {answer}

## Grounding
The assistant extracts, categorizes, filters, and tracks. Big decisions,
creative ideas, and final scheduling stay with me.
```

Create the directory first if needed: `mkdir -p ~/brain-dump/weeks`.
