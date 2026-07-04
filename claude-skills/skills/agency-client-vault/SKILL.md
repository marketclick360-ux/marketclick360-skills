---
name: agency-client-vault
description: Operate the private agency-vault repo (marketclick360-ux/agency-vault) — the client knowledge vault holding per-client facts, tone, tools, decisions, meetings, and backlogs. Use when reading or writing client context, saving decisions/commitments from a conversation, onboarding a new client folder, reconciling contradictory client facts, or bootstrapping the vault itself. Use proactively whenever a conversation produces client information worth preserving.
argument-hint: [client-name]
---

# Client Knowledge Vault

The vault is what makes every agency agent work — the Master CSA, weekly
reports, and proposals all read from it. It is written for **future Claude
sessions to retrieve and reason over**, not for human browsing.

⚠️ **Privacy invariant:** the vault lives ONLY in the private
`marketclick360-ux/agency-vault` repo. Client data never enters this (public)
skills repo, the public `obsidian-second-brain` fork, or any other public
surface. Secrets (API keys, passwords) never enter the vault at all — record
*where* a credential lives, never its value.

## Steps

1. **Boot:** read the vault's `_CLAUDE.md` first — it overrides this skill.
   Then load progressively, never everything: `CRITICAL_FACTS.md` (~120
   tokens) → `index.md` to navigate → the one client folder in play. Levels
   are defined in [reference/vault-structure.md](reference/vault-structure.md).
2. **Read before you write:** search the vault before creating any note —
   duplicates are vault rot. Never assert something is *absent* from the vault
   without an exhaustive search (false absence is the #1 failure mode).
3. **Write by the rules:** every note follows
   [reference/note-rules.md](reference/note-rules.md) — frontmatter, "For
   future Claude" preamble, dated claims, wikilinks, confidence levels,
   bi-temporal `timeline:` for facts that change.
4. **Two-Output rule:** any conversation that produces client insight yields
   (a) the answer to the user AND (b) the insight filed into the vault. After
   a client-related session, offer to save.
5. **Rewrite, don't append:** new information updates the existing note (with
   a `## History` line for what changed). Only `Logs/`, `raw/`, and
   `timeline:` arrays are append-only. Two notes must never disagree without
   knowing they disagree — reconcile or file a conflict note.
6. **Propagate:** a decision touches the client's `decisions/` AND `facts.md`
   AND the day's log entry. Propagation table in vault-structure.md.
7. **New client or new vault:** run the scaffold —

   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/scaffold_vault.sh /path/to/agency-vault            # bootstrap vault
   bash ${CLAUDE_SKILL_DIR}/scripts/scaffold_vault.sh /path/to/agency-vault "Acme Co"  # add a client
   ```

   Then fill the generated `_CLIENT.md` facts card from intake/discovery.

## Output

Vault reads: the minimal context loaded, cited by note path. Vault writes:
notes that pass the checklist at the bottom of note-rules.md, `index.md` and
the daily log updated, and a one-line report of what was filed where.
