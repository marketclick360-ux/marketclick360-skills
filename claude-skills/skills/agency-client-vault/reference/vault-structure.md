# Vault Structure & Operating Model

The vault is the private repo `marketclick360-ux/agency-vault`. One vault,
one folder per client, plus agency-level knowledge. Adapted from the
`obsidian-second-brain` executive preset + assistant mode.

## Layout

```
agency-vault/
├── _CLAUDE.md               # Operating manual — read FIRST, overrides the skill
├── CRITICAL_FACTS.md        # ~120-token agency facts card (always loaded)
├── index.md                 # Catalog of every note — read before searching
├── log.md                   # Thin pointer to Logs/ (never holds entries)
├── Logs/
│   └── YYYY-MM-DD.md        # Operation log: **HH:MM** - action | summary
├── agency/
│   ├── SOUL.md              # Agency identity, voice, positioning, standing rules
│   ├── decisions/           # Agency-level decisions (pricing, niche, tooling)
│   └── time-log.md          # date / client / minutes / task (feeds repricing + Day-90)
├── clients/
│   └── <client-slug>/       # lowercase-hyphenated, e.g. acme-co/
│       ├── _CLIENT.md       # ~150-token always-current card + folder notes
│       ├── facts.md         # company facts, bi-temporal timeline
│       ├── people.md        # contacts, roles, preferences, quotes
│       ├── tone.md          # voice & comms rules for THIS client
│       ├── tools.md         # stack, integrations, where credentials live (never values)
│       ├── backlog.md       # every request logged — becomes upgrade evidence
│       ├── decisions/       # YYYY-MM-DD - title.md
│       ├── meetings/        # YYYY-MM-DD - topic.md
│       └── reports/         # copies of sent weekly reports / value summaries
└── templates/               # blank versions of the files above
```

## Progressive context loading (never load the whole vault)

| Level | Load | Cost | When |
|---|---|---|---|
| L0 | `_CLAUDE.md` + `CRITICAL_FACTS.md` | ~300 tok | Always, at session start |
| L1 | `index.md` + last ~10 `Logs/` entries | ~1–2k | Navigating / "what's the state?" |
| L2 | `_CLIENT.md` cards of active clients | ~150/client | Cross-client work (Monday reports, tier mapping) |
| L3 | One client's full folder | 5–20k | That client is the subject of the work |

Rule of thumb: L3 for at most the one or two clients in play. `_CLIENT.md`
exists precisely so other clients stay at L2.

## Propagation rules (never write in isolation)

| Event | Also update |
|---|---|
| Decision made | client `decisions/` + `facts.md` (if it changes state) + today's log |
| Client request | `backlog.md` + today's log |
| Meeting held | `meetings/` note + `people.md` last-interaction + backlog + log |
| Commitment made by us | client backlog (with due date) + log |
| Fact changed (tier, contact, stack) | `facts.md` timeline + `_CLIENT.md` card + log |
| Report sent | copy to `reports/` + log |
| Any note created/renamed | `index.md` |

## Auto-save vs ask

Save **without asking**: decisions, commitments, new people, client facts
stated in conversation, completed work worth logging.
**Ask before** saving: anything health/legal/financial-personal about a person,
and before archiving or restructuring existing notes.

## Archive discipline

Never delete. Prefix the filename `_archived_`, set `status: archived`.
Churned client → the whole folder gets a `status: churned` card and stays.
The vault is a permanent record.

## Maintenance cadence (any session can run these)

- **Weekly (before Monday reports):** sweep `Logs/` for the week per client;
  check `backlog.md` items are current; update `_CLIENT.md` cards.
- **Monthly health audit:** contradictions between notes, undated claims,
  stale `last-interaction`, orphan notes missing from `index.md`, notes
  without frontmatter. Fix safe issues; list destructive fixes for approval.

## Bootstrap

New vault or new client → `scripts/scaffold_vault.sh` (see SKILL.md). After
scaffolding a client, fill `_CLIENT.md` and `facts.md` from the intake record
(`client-intake-form` output is agent-ready markdown — ingest it, then file
each section to the right note).
