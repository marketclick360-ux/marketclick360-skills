# IRMAA Planning Levers

Use when the client's income is high but no life-changing event applies, or to plan future years. Remember the **2-year lookback**: income in tax year X sets premiums in year X+2. Model each lever with `scripts/irmaa.py --add <amount>` (or a negative amount) to show the dollar effect.

**Tax advice gate:** Until Janet is an Enrolled Agent (target: by July 2027), present these as *education* and refer specific tax advice to the client's CPA/EA. After enrollment, follow Circular 230 and get §7216 consent before using return data.

## Contents
1. Income timing
2. Retirement-account levers
3. Charitable levers
4. Insurance-product levers (separate appointment)
5. Household and filing-status effects

## 1. Income timing
- **Capital gains:** spread large sales across tax years; harvest losses to offset gains.
- **Home sale:** the gain over the exclusion counts toward MAGI. Time the sale and plan for the jump 2 years later.
- **Deferred comp / bonuses / severance:** spread payouts where the plan allows; a big final year triggers IRMAA 2 years later (and possibly an SSA-44 "work stoppage" case).

## 2. Retirement-account levers
- **Roth conversions:** short-term MAGI increase, then tax-free income later. Best in the "gap years" between retirement and RMDs. Size conversions to **stay at or under a threshold**; use the script's headroom number. Conversions done at 63+ affect IRMAA (lookback).
- **RMDs:** can't be avoided, but planning conversions before RMD age shrinks them.
- **HSA:** stop HSA contributions 6 months before Medicare starts (Part A coverage is retroactive up to 6 months). HSA withdrawals for qualified expenses aren't income.

## 3. Charitable levers
- **QCD (qualified charitable distribution):** age 70½+, IRA money sent directly to charity is **excluded from AGI** and counts toward RMDs. The cleanest MAGI reducer for charitable clients. Verify the annual limit each year.
- Donating appreciated stock (instead of selling it) avoids the gain.

## 4. Insurance-product levers (separate, client-requested appointment)
CMS rule: no life/annuity marketing during MA/PDP sales activity. These need their own appointment with suitability/best-interest documentation.
- **QLAC** inside an IRA: excluded from RMD calculations until payouts start (by 85). Verify the current dollar limit.
- **Life insurance cash value:** policy loans and withdrawals up to basis generally aren't taxable. Watch for lapse risk.
- **Non-qualified annuities:** withdrawals of gains **raise** MAGI. Review timing before adding more.
- **Survivor IRMAA:** after a spouse dies, the survivor files single (after the year of death), so the same income often lands in a higher tier. Life insurance can cover the gap; "death of spouse" also qualifies for SSA-44.

## 5. Household and filing-status effects
- **Joint filers both on Medicare pay IRMAA twice**: always run `--both-on-medicare`.
- **Married filing separately** (living together) has very harsh brackets. Rarely worth it for IRMAA purposes.
- **Tax-exempt interest counts** toward IRMAA MAGI, so municipal bonds don't avoid IRMAA.
