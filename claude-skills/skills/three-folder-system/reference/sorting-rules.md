# Sorting Rules

How to categorize files into Atlas / Projects / End Products during Cleanup,
and the reusable prompt for when the user wants to run the sort in another AI
tool.

## The decision test (apply in order)

For each file, ask the three questions — first "yes" wins:

1. **Is it finished?** Completed, exported, delivered, published, signed →
   **03 End Products**. Signals: `final`, `v-final`, `signed`, `delivered`,
   export formats of working docs (a PDF exported from a living .docx),
   dated deliverables in the past.
2. **Am I working on it right now?** Actively edited, part of a live task →
   **02 Projects**. Signals: recent modified date, `draft`/`wip`/`v2` names
   tied to a known current commitment, files referenced by this week's tasks.
3. **Is it an idea, note, or raw material?** → **01 Atlas**. Signals:
   `notes`, `ideas`, `braindump`, clippings, screenshots of inspiration,
   research PDFs, rough strategic drafts with no active project attached.

## Tie-breakers and edge cases

- **Old "in-progress" files** (working names, but untouched for months): the
  project is dormant. Don't guess — put it in **Unclear** and ask: "still
  live, or should its useful parts go to Atlas and the rest to 04 Archive?"
- **Distracting or on-hold projects**: park in **04 Archive** with a
  revisit rule — e.g. "sits in Atlas one month; if untouched, archive."
  Archived ≠ deleted; it's out of sight so it stops competing for attention.
- **Templates and reusable assets** (logos, boilerplate, blank forms): they're
  finished things you reuse → End Products.
- **Reference material you act FROM but never edit** (contracts received,
  specs, brand guidelines): finished, just not by you → End Products.
- **Duplicates / near-versions**: sort the newest; list older versions as
  deletion candidates — but only the user deletes.
- **Anything ambiguous**: Unclear list, with the one question that resolves
  it. A file that won't sort is an unclear plan made visible — that's the
  system working, not failing.

## Project completion ritual

When a project finishes: the deliverable moves to **End Products**, and the
temporary working files move to **04 Archive** or get deleted (user's call).
Atlas source notes stay in Atlas; they may seed the next project.

## Reusable cleanup prompt

When the user wants to run the sort somewhere else (Gemini, ChatGPT, a Drive
they won't connect), hand them this:

> I am setting up an "Atlas, Projects, End Products" three-folder system:
> 01 Atlas = raw notes, ideas, clippings, rough drafts (thinking);
> 02 Projects = files I am actively working on right now (building);
> 03 End Products = final, polished, delivered files (finished);
> 04 Archive = inactive or distracting projects, parked out of sight.
> Based on this list of files, sort each into one of the categories and
> explain why in one line each. If a file doesn't clearly fit, put it in a
> separate "Unclear" list with the question I'd need to answer to place it.
> Here is the list: {paste file list}

## Periodic automation

If the user wants the folders to stay clean automatically, offer to set up a
recurring triage: a scheduled run (cron trigger or calendar reminder) that
executes `triage.py scan` on the loose-files area and proposes a sort. The
proposal is still reviewed by the user — automation gathers and suggests, the
user files. Don't auto-move on a schedule.
