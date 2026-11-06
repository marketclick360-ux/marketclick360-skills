---
name: irmaa-check
description: Runs a Medicare IRMAA check for a client. Computes the IRMAA tier and Part B/Part D surcharges from MAGI and filing status, shows how close they are to the next bracket cliff, screens for SSA-44 life-changing events (retirement, work reduction, death of spouse, etc.) and estimates the savings, models "what-if" income (Roth conversions, capital gains), and produces a client-ready summary plus compliance reminders. Use when asked to "run an IRMAA check", "is this client paying IRMAA", "IRMAA appeal", "SSA-44", "IRMAA letter", "will this Roth conversion trigger IRMAA", or during a Medicare review for a high-income or recently retired client.
argument-hint: [MAGI] [single|joint|mfs]
---

# IRMAA Check

A fast, repeatable IRMAA review: **tier → cost → SSA-44 screen → planning headroom → client summary.**
The math comes from `scripts/irmaa.py` (official CMS figures in `reference/brackets.json`). Never do the bracket math by hand.

## Steps

1. **Collect inputs** (ask only for what's missing, all in one message):
   - Filing status: `single` (also head of household / qualifying widow(er)), `joint`, or `mfs` (married filing separately, lived with spouse)
   - MAGI from the return **2 years before the premium year** (2026 premiums use the 2024 return). IRMAA MAGI = AGI (1040 line 11) + tax-exempt interest (line 2a). If they give AGI and tax-exempt interest, pass both.
   - For joint filers: are **both** spouses on Medicare?
   - Did they get an IRMAA letter from SSA? Have they retired or had another life event in the last 2 years? (See step 3.)
   - Any big income planned this year or next (Roth conversion, home or stock sale, bonus)?

2. **Run the calculator** (from this skill's directory):
   ```bash
   python3 scripts/irmaa.py --magi <MAGI> --status <single|joint|mfs> [--both-on-medicare]
   # or: --agi <AGI> --tax-exempt <amount>
   ```
   If the requested premium year isn't in `brackets.json`, the script says so. Tell the user the new figures usually come out in mid-November, and offer to add them from the CMS Part B fact sheet. **Never invent bracket numbers.**

3. **SSA-44 screen:** read [reference/ssa44-events.md](reference/ssa44-events.md) and ask the 8 screening questions. If an event applies, estimate current-year MAGI and rerun with `--new-magi <estimate>` to show the savings. If the problem is wrong or outdated data instead, it's a reconsideration (SSA-561), not an SSA-44.

4. **Planning headroom:** if there's a cliff warning, no event applies, or the client plans big income, read [reference/planning-levers.md](reference/planning-levers.md) and model scenarios with `--add <amount>` (for example, a Roth conversion). Point out the 2-year lookback.

5. **Write the client summary** in this format (plain language, no jargon):
   ```
   IRMAA CHECK: [Client first name] | Premium year [YYYY] | Based on [YYYY-2] tax return
   - Your income used by Social Security: $___ ([filing status])
   - Your IRMAA level: [none / tier X]: you pay $___/month extra ($___/year for your household)
   - Room before the next jump: $___ (crossing it costs $___/year more)
   - Appeal opportunity: [Yes: life event "___", estimated savings $___/year / No]
   - Next steps: [1-3 concrete actions, e.g. gather retirement letter, file SSA-44, talk to your CPA about Roth conversion size]
   Figures are estimates from CMS's [YYYY] tables. Social Security makes the final decision.
   ```

6. **Log it** (suggest to the user): add to the CRM: segment tag, IRMAA tier, SSA-44 filed (Y/N, date), estimated savings, follow-up date.

## Compliance gates (check every time)
- **Before EA enrollment (target July 2027):** IRMAA education and free SSA-44 help only. Don't charge for tax advice or call yourself an EA. Refer specific tax advice to the client's CPA or EA.
- **Tax return data (IRC §7216):** using return information to recommend *any* product (Medigap, MA, life, annuity) requires the client's prior written consent in the IRS-required format.
- **CMS:** no life or annuity products during an MA/PDP appointment or event. Product levers in planning-levers.md need a separate, client-requested appointment with suitability documentation.
- **SSA fees:** help with SSA-44 for free during the Medicare review; the client signs and files. Don't charge for SSA representation unless SSA fee authorization is confirmed.
- **Annual update:** each November add the new year to `reference/brackets.json` from the CMS fact sheet (only official figures), and update `verified_on`.
