# marketclick360-skills

Shared Claude Code **Agent Skills** for all your projects, organized with
**progressive disclosure** and **multi-file structures** so they stay cheap to
load and easy to maintain.

## The idea in one picture

```
Startup        →  Claude reads ONLY each skill's name + description  (~60 tokens each)
On invocation  →  The matched skill's SKILL.md body loads            (~1–2k tokens)
On demand      →  reference/*.md and scripts/* load only when needed (cost only if read)
```

That's progressive disclosure: a skill can be huge on disk but nearly free in
context until the moment Claude actually needs a specific piece of it.

## What's in here

```
marketclick360-skills/
├── .claude-plugin/
│   └── plugin.json            # Makes this an installable plugin
├── skills/
│   ├── skill-template/        # Copy this to start a new skill
│   │   ├── SKILL.md           # Navigation hub (keep it short)
│   │   ├── reference/
│   │   │   └── DETAILS.md     # Loaded on demand
│   │   └── scripts/
│   │       └── example.py     # Executed, not loaded into context
│   ├── release-prep/          # A fully worked multi-file example
│   │   ├── SKILL.md
│   │   ├── reference/
│   │   │   ├── checklist.md
│   │   │   └── versioning.md
│   │   └── scripts/
│   │       └── changelog.py
│   ├── agency-onboarding/     # Client install pipeline SOP + comms + intake system
│   ├── agency-agent-prompts/  # System prompts for the internal agent bench
│   ├── agency-scope-proposal/ # Tiers, proposals, repricing playbook
│   ├── agency-weekly-report/  # Client reports + observability SOP
│   ├── agency-content-engine/ # Delivery-to-content workflow + anonymization
│   └── agency-niche-scorecard/# Day-90 niche decision scoring
└── README.md
```

The six `agency-*` skills implement the
[MarketClick360 operating blueprint](https://github.com/marketclick360-ux/marketclick360/blob/main/docs/ai-agency-scaling-plan.md)
— every reusable template, agent prompt, and SOP from the blueprint lives here
as a loadable skill.

## How to organize a *complex* skill (the rules that matter)

1. **SKILL.md is a table of contents, not an encyclopedia.** Keep it under
   ~500 lines. Put the "what to do" up top; link out to the heavy detail.
2. **Reference files stay one level deep.** `SKILL.md → reference/foo.md` is
   read in full. Deeper chains (`foo.md → bar.md`) get only partially read.
3. **Split by topic so irrelevant detail stays on disk.** e.g. a billing skill
   with `reference/invoices.md`, `reference/refunds.md`, `reference/taxes.md` —
   Claude opens only the one the task needs.
4. **Put a Table of Contents at the top of any reference file > ~100 lines** so
   Claude sees the full scope even on a partial read.
5. **Scripts run; they don't load.** Anything deterministic (validation,
   formatting, scanning) goes in `scripts/`. Only the script's *output* enters
   context, not its source.
6. **Write the `description` in the third person and pack it with triggers** —
   it's what makes Claude auto-pick the skill. e.g. "Prepares a release: bumps
   version, writes changelog, tags. Use when asked to cut a release, ship, or
   publish."

## Using these across all your repos (3 tiers)

| Tier | Where | Use it for |
| --- | --- | --- |
| **Shared (this repo)** | Install as a plugin in every project | Skills you want everywhere: release-prep, security-audit, review helpers |
| **Personal** | `~/.claude/skills/` on your machine | Your own quick utilities, available in any local session |
| **Project** | `.claude/skills/` committed in a single repo | Things only that project needs: its deploy command, its DB migration steps |

### Install this plugin in a project

From inside a project where you run Claude Code:

```
/plugin marketplace add marketclick360-ux/marketclick360-skills
/plugin install marketclick360-skills
```

Skills then appear namespaced, e.g. `/marketclick360-skills:release-prep`.
Update everywhere by pushing here and re-running `/plugin install`.

> Note: Skills run in the Claude Code **CLI** (local, container, or web session
> with the repo checked out). For a project to pick up *project* skills in a
> web/cloud session, commit them to that repo's `.claude/skills/`.

## Add a new skill

1. Copy `skills/skill-template/` to `skills/your-skill-name/`.
2. Edit the frontmatter `name` (lowercase-hyphenated) and `description`.
3. Keep `SKILL.md` short; move detail into `reference/` and logic into
   `scripts/`.
4. Commit and push. Re-install the plugin in your projects to pick it up.
