---
name: agency-scope-proposal
description: Builds tier-fitted scopes, proposals, and repricing cases for the MarketClick360 AI-employee service ($2.5k/$5k/$8k retainers). Use when scoping a new client, drafting a proposal, deciding a tier, handling scope creep, or preparing a renewal or upgrade conversation.
argument-hint: [client-name]
---

# Scope & Proposal Generator

Turn intake answers into a tier-fitted offer, and metrics history into renewal
evidence. The operator always sets final price — nothing here auto-sends.

## Steps

1. **Tier fit:** count scoped workflows → base tier, then apply the +1-tier
   modifiers from [reference/tiers.md](reference/tiers.md). Sanity check:
   estimated monthly value to the client must be ≥3× the retainer — if not,
   narrow scope or recommend declining. Never discount.
2. **Proposal:** follow the structure in [reference/tiers.md](reference/tiers.md)
   — page 1 is the AI Employee Job Description in the client's own intake
   words; exclusions are as explicit as inclusions.
3. **Scope creep:** log every out-of-scope request to the client's backlog and
   reply with the standard swap-or-upgrade template.
4. **Renewals:** check the triggers in [reference/repricing.md](reference/repricing.md)
   and, when one fires, assemble the value-summary one-pager for the operator.

## Output

A draft scope + proposal (or renewal one-pager) queued for operator pricing
and approval, with any tier-fit ambiguity flagged rather than resolved silently.

## Client vault

Client context (facts, tone, tools, decisions, backlog) lives in the private
`marketclick360-ux/agency-vault` repo, operated per the `agency-client-vault`
skill. Read the client's `_CLIENT.md` card first — and `tone.md` before
drafting anything client-facing. Write decisions, commitments, and requests
back per that skill's Two-Output and propagation rules. Client data never
enters this public skills repo.
