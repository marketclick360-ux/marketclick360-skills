# Vault Note Rules (AI-first)

Adapted from the `obsidian-second-brain` AI-first vault rule
(`marketclick360-ux/obsidian-second-brain` → `references/ai-first-rules.md`).
Premise: **notes are written for a future Claude session with zero context**,
not for human review. A note that needs the conversation that created it is a
broken note.

## The seven rules

1. **Self-contained context** — every note makes sense alone.
2. **"For future Claude" preamble** — first section after frontmatter.
3. **Rich, consistent frontmatter** — schemas below.
4. **Recency markers** — every external fact carries its date and source.
5. **Sources preserved verbatim** — quotes and URLs exactly as received.
6. **Cross-links mandatory** — every person/client/decision mentioned gets a
   `[[wikilink]]`; create a stub if the target doesn't exist.
7. **Confidence levels** — `stated` (client said it) · `high` (multiple
   sources) · `medium` (single source, plausible) · `speculation` (inference).

## Universal frontmatter

```yaml
---
date: YYYY-MM-DD          # created
updated: YYYY-MM-DD       # last meaningful update
type: <note-type>
client: <client-slug>     # omit only for agency/ notes
tags: [<type>, ...]
ai-first: true
---
```

## Preamble format

```markdown
## For future Claude
This note is a [type] about [topic] for client [client], saved on [date].
It [main purpose]. [Optional staleness/confidence/scope caveat.]
```

## Per-type schemas (add to universals)

**`client-facts`** (`facts.md`) — current state on top, history preserved:

```yaml
type: client-facts
status: active            # prospect | active | paused | churned
tier: core                # starter | core | embedded  ($2.5k/$5k/$8k)
industry: ""
main-contact: "[[<client>/people#Name]]"
```

Facts that change over time use a **bi-temporal timeline** — never overwrite,
always append the new state:

```yaml
timeline:
  - fact: "Tier: starter ($2.5k/mo)"
    from: 2026-03-01        # when it became true
    until: 2026-07-01
    learned: 2026-03-01     # when the vault learned it
    source: "[[decisions/2026-03-01 - signed starter]]"
  - fact: "Tier: core ($5k/mo)"
    from: 2026-07-01
    until: present
    learned: 2026-06-24
    source: "[[decisions/2026-06-24 - upgrade agreed]]"
```

Top-level fields always hold the CURRENT state; `timeline:` holds provenance.
Different facts at different times are history, not a contradiction.

**`decision`** (one file per decision, `decisions/YYYY-MM-DD - title.md`):

```yaml
type: decision
decided-by: ""            # ALWAYS record who — operator, client, or agent
confidence: stated
sources: [...]
```

Body: context → options considered → decision → consequences → who approved.

**`meeting`** (`meetings/YYYY-MM-DD - topic.md`): attendees (wikilinked),
verbatim commitments made *by us* and *by them* (each dated), decisions
(cross-filed per Propagation), next actions → client backlog.

**`person`** (inside the client's `people.md` or `people/`):
role, relationship strength, `last-interaction: YYYY-MM-DD`, communication
preferences, verbatim quotes that reveal priorities.

## Recency markers

Every claim from outside the conversation gets an inline date + source:

```markdown
- Acme's lead volume is ~400/mo (as of 2026-06, June metrics email)
```

Undated claims are treated as unreliable by future sessions.

## Sentinel markers — AI-refreshed, human-annotated notes

For notes a command regenerates (status summaries, architecture notes,
metric rollups) while the operator hand-annotates:

```markdown
<!-- @generated:start -->
...machine content — safe to overwrite on the next refresh...
<!-- @generated:end -->

<!-- @user:start -->
...operator notes — NEVER overwritten...
<!-- @user:end -->
```

Refresh rule: replace only inside `@generated` blocks; everything else is
human-owned. First run with no markers → wrap your output in `@generated`.

## Anti-fabrication (governs reading)

- **No false absence:** never say a fact/note doesn't exist without an
  exhaustive search — the most common observed failure, worse than fabrication.
- **Enumerate, don't sample:** when listing matching notes, list all of them.
- **Mark unknowns `TBD`:** an empty `## Decisions` section is correct when no
  decision was made. Never fill gaps with plausible inventions — a fabricated
  client fact ends up in a client-facing report.

## Contradiction handling

When a new fact conflicts with a stored one: newer + more authoritative wins
(client's own statement > our inference; signed doc > meeting recollection).
Rewrite the stale note and add a `## History` line:
`Previously stated X (source, date). Updated to Y (source, date).`
Genuinely ambiguous → file `decisions/Conflict - <topic>.md` with both sides,
`status: open`, and surface it to the operator.

## Write checklist (every note, before you're done)

- [ ] Frontmatter complete, `ai-first: true`
- [ ] "For future Claude" preamble
- [ ] Every claim dated and sourced; confidence marked where not `stated`
- [ ] Wikilinks for every entity mentioned
- [ ] No secrets (key *locations* ok, values never)
- [ ] `index.md` updated; entry written to `Logs/YYYY-MM-DD.md`
- [ ] Propagation done (see vault-structure.md)
