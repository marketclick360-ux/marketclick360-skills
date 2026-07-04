#!/usr/bin/env bash
# Scaffold the agency-vault repo, or add one client folder to it.
#
#   scaffold_vault.sh /path/to/agency-vault              # bootstrap the vault
#   scaffold_vault.sh /path/to/agency-vault "Acme Co"    # add a client
#
# Idempotent: never overwrites an existing file.
set -euo pipefail

VAULT="${1:?usage: scaffold_vault.sh <vault-path> [client name]}"
CLIENT_NAME="${2:-}"
TODAY="$(date +%F)"

write_if_absent() { # $1=path, stdin=content
  if [ -e "$1" ]; then echo "skip (exists): $1"; else
    mkdir -p "$(dirname "$1")"; cat > "$1"; echo "created: $1"; fi
}

# ---------- vault skeleton ----------
if [ -z "$CLIENT_NAME" ]; then
  mkdir -p "$VAULT"/{Logs,agency/decisions,clients,templates}

  write_if_absent "$VAULT/_CLAUDE.md" <<EOF
# Claude Operating Manual - MarketClick360 Agency Vault

> Read this file before doing anything in this vault.
> It overrides the agency-client-vault skill where they differ.

## Vault identity
- **Owner:** MarketClick360 (solo AI agent agency)
- **Purpose:** per-client knowledge that makes every agency agent work
- **Privacy:** PRIVATE repo. Client data never leaves it. No secret values, ever.
- **Last updated:** $TODAY

## Operating rules
1. Load progressively: CRITICAL_FACTS.md -> index.md -> the one client in play.
2. Search before creating. Never claim absence without an exhaustive search.
3. Notes follow the agency-client-vault skill's note-rules.md (AI-first:
   preamble, frontmatter, dated claims, wikilinks, confidence, bi-temporal
   timeline for changing facts).
4. Two-Output rule: client insight in conversation = answer + vault write.
5. Rewrite, don't append (except Logs/ and timeline: arrays). Add a
   ## History line when replacing a fact.
6. Propagate every write (see the skill's propagation table) and update
   index.md + Logs/$TODAY.md.
7. Never delete: archive with _archived_ prefix + status: archived.

## Folder map
| Folder | Purpose |
|---|---|
| agency/ | Agency-level identity, decisions, time log |
| clients/<slug>/ | One folder per client - facts, people, tone, tools, backlog, decisions, meetings, reports |
| Logs/ | Daily operation log (append-only) |
| templates/ | Blank note templates |
EOF

  write_if_absent "$VAULT/CRITICAL_FACTS.md" <<EOF
# Critical facts (keep under ~150 tokens, always current)

- Agency: MarketClick360 - solo AI agent agency, "AI employees" on retainer
- Tiers: starter \$2.5k / core \$5k / embedded \$8k per month
- Operator: marketclick360@gmail.com
- Blueprint: marketclick360 repo -> docs/ai-agency-scaling-plan.md
- Pending work: marketclick360 repo -> docs/ops-board.md
- Weekly report ships every Monday, no exceptions
EOF

  write_if_absent "$VAULT/index.md" <<EOF
# Vault index

Read this before searching. One line per note: \`[[path]] - what it holds\`.

## agency/
- [[agency/SOUL]] - agency identity, voice, standing rules
- [[agency/time-log]] - date/client/minutes/task

## clients/
(none yet)
EOF

  write_if_absent "$VAULT/log.md" <<EOF
# Operation log

Entries live in Logs/YYYY-MM-DD.md - this file is only a pointer.
EOF

  write_if_absent "$VAULT/Logs/$TODAY.md" <<EOF
# $TODAY

**00:00** - bootstrap | vault scaffolded
EOF

  write_if_absent "$VAULT/agency/SOUL.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: agency-identity
tags: [agency, identity]
ai-first: true
---

## For future Claude
This note is the agency's identity card, created $TODAY. It defines voice and
standing rules that apply to every client unless the client's tone.md says
otherwise.

## Voice
Warm, concise, premium-but-plain. No jargon, no hype. Drafts are queued for
operator approval - agents never send.

## Standing rules
- TBD (fill from the blueprint SS3 as they solidify)
EOF

  write_if_absent "$VAULT/agency/time-log.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: time-log
tags: [agency, time-log]
ai-first: true
---

## For future Claude
Append-only operator time log. Feeds repricing and the Day-90 niche decision.

| Date | Client | Minutes | Task |
|---|---|---|---|
EOF
  echo "Vault scaffolded at $VAULT"
  exit 0
fi

# ---------- client folder ----------
SLUG="$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]\+/-/g' -e 's/^-//' -e 's/-$//')"
DIR="$VAULT/clients/$SLUG"
mkdir -p "$DIR"/{decisions,meetings,reports}

write_if_absent "$DIR/_CLIENT.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: client-card
client: $SLUG
tags: [client-card, $SLUG]
ai-first: true
---

## For future Claude
Always-current ~150-token card for $CLIENT_NAME. Read this at L2; open the
rest of the folder only when this client is the subject of the work.

- **Client:** $CLIENT_NAME
- **Status:** TBD (prospect | active | paused | churned)
- **Tier:** TBD (starter | core | embedded)
- **Main contact:** TBD
- **What we run for them:** TBD
- **Current focus:** TBD
- **Landmines:** TBD
EOF

write_if_absent "$DIR/facts.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: client-facts
client: $SLUG
status: TBD
tier: TBD
industry: ""
main-contact: ""
tags: [client-facts, $SLUG]
ai-first: true
timeline: []
---

## For future Claude
Company facts for $CLIENT_NAME. Top matter holds CURRENT state; timeline:
holds every changed fact with from/until/learned/source. Every claim below
needs a date and source.

## Facts
- TBD
EOF

write_if_absent "$DIR/people.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: people
client: $SLUG
tags: [people, $SLUG]
ai-first: true
---

## For future Claude
Contacts at $CLIENT_NAME: role, relationship, last-interaction, preferences,
verbatim quotes that reveal priorities.

## Contacts
- TBD
EOF

write_if_absent "$DIR/tone.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: tone
client: $SLUG
tags: [tone, $SLUG]
ai-first: true
---

## For future Claude
Voice and comms rules for $CLIENT_NAME. Overrides agency/SOUL.md for this
client. Every client-facing draft must pass these.

## Rules
- TBD
EOF

write_if_absent "$DIR/tools.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: tools
client: $SLUG
tags: [tools, $SLUG]
ai-first: true
---

## For future Claude
$CLIENT_NAME's stack and integrations. Record WHERE each credential lives
(e.g. "Vercel env var X", "operator's password manager") - NEVER the value.

## Stack
- TBD
EOF

write_if_absent "$DIR/backlog.md" <<EOF
---
date: $TODAY
updated: $TODAY
type: backlog
client: $SLUG
tags: [backlog, $SLUG]
ai-first: true
---

## For future Claude
Every request $CLIENT_NAME makes gets logged here with a date - the backlog
itself becomes upgrade evidence at renewal time.

| Date | Request | Status | Notes |
|---|---|---|---|
EOF

echo "Client folder created: $DIR"
echo "Next: fill _CLIENT.md and facts.md from the intake record, then add the client to index.md."
