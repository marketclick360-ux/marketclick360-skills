#!/usr/bin/env python3
"""IRMAA calculator: tier, surcharge, cliff distance, and SSA-44 savings estimate.

Examples:
  irmaa.py --magi 152000 --status single
  irmaa.py --agi 230000 --tax-exempt 6000 --status joint --both-on-medicare
  irmaa.py --magi 260000 --status joint --new-magi 120000      # SSA-44 estimate
  irmaa.py --magi 104000 --status single --add 15000           # "what if" (e.g. Roth conversion)
  irmaa.py --magi 152000 --status single --json

Premium year Y uses MAGI from tax year Y-2. IRMAA MAGI = AGI + tax-exempt interest.
Data lives in ../reference/brackets.json (only official CMS years).
"""
import argparse
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "reference" / "brackets.json"
CLIFF_WARN = 10000  # flag when within this many dollars of the next threshold


def load_year(year):
    data = json.loads(DATA.read_text())
    key = str(year)
    if key not in data:
        years = sorted(k for k in data if not k.startswith("_"))
        sys.exit(
            f"No official IRMAA table for premium year {year}. Available: {', '.join(years)}.\n"
            "CMS usually publishes next year's figures in mid-November. Add them to "
            "reference/brackets.json from the CMS Part B fact sheet, then rerun."
        )
    return data[key]


def in_tier(magi, tier):
    if tier["upper"] is None:
        return True
    return magi <= tier["upper"] if tier["upper_inclusive"] else magi < tier["upper"]


def find_tier(magi, tiers):
    for i, t in enumerate(tiers):
        if in_tier(magi, t):
            return i
    return len(tiers) - 1


def lower_bound_to_drop(i, tiers):
    """Highest MAGI that lands in tier i-1 (the tier below)."""
    prev = tiers[i - 1]
    return prev["upper"] if prev["upper_inclusive"] else prev["upper"] - 1


def evaluate(magi, status, year_data, people):
    tiers = year_data["tiers"][status]
    std = year_data["part_b_standard"]
    i = find_tier(magi, tiers)
    t = tiers[i]
    monthly = t["b_adj"] + t["d_adj"]
    res = {
        "magi": magi,
        "tier": i,  # 0 = no IRMAA
        "part_b_total_monthly": round(std + t["b_adj"], 2),
        "part_b_surcharge_monthly": t["b_adj"],
        "part_d_surcharge_monthly": t["d_adj"],
        "surcharge_monthly_per_person": round(monthly, 2),
        "surcharge_annual_per_person": round(monthly * 12, 2),
        "surcharge_annual_household": round(monthly * 12 * people, 2),
        "people_on_medicare": people,
    }
    if i > 0:
        target = lower_bound_to_drop(i, tiers)
        prev = tiers[i - 1]
        save = (monthly - (prev["b_adj"] + prev["d_adj"])) * 12 * people
        res["reduce_magi_by_to_drop_a_tier"] = magi - target
        res["annual_savings_if_drop_a_tier"] = round(save, 2)
    if t["upper"] is not None:
        nxt = tiers[i + 1]
        headroom = (t["upper"] - magi) if t["upper_inclusive"] else (t["upper"] - 1 - magi)
        res["headroom_before_next_tier"] = headroom
        res["next_tier_extra_annual_household"] = round(
            ((nxt["b_adj"] + nxt["d_adj"]) - monthly) * 12 * people, 2
        )
        res["cliff_warning"] = headroom <= CLIFF_WARN
    return res


def money(x):
    return f"${x:,.2f}"


def print_report(r, label, year, year_data, status):
    names = {"single": "Single / HOH / QW", "joint": "Married filing jointly", "mfs": "Married filing separately (lived with spouse)"}
    print(f"== {label} ==")
    print(f"Premium year {year} (uses {year_data['magi_tax_year']} tax return MAGI) | {names[status]}")
    print(f"MAGI: {money(r['magi'])}")
    if r["tier"] == 0:
        print("IRMAA: none (standard premium)")
    else:
        print(f"IRMAA tier: {r['tier']} of {len(year_data['tiers'][status]) - 1}")
    print(f"Part B total: {money(r['part_b_total_monthly'])}/mo  (surcharge {money(r['part_b_surcharge_monthly'])})")
    print(f"Part D surcharge: {money(r['part_d_surcharge_monthly'])}/mo (added to plan premium)")
    print(f"IRMAA cost: {money(r['surcharge_annual_per_person'])}/yr per person, "
          f"{money(r['surcharge_annual_household'])}/yr household ({r['people_on_medicare']} on Medicare)")
    if "reduce_magi_by_to_drop_a_tier" in r:
        print(f"To drop one tier: reduce MAGI by {money(r['reduce_magi_by_to_drop_a_tier'])} "
              f"-> saves {money(r['annual_savings_if_drop_a_tier'])}/yr")
    if "headroom_before_next_tier" in r:
        warn = "  ** CLIFF WARNING **" if r["cliff_warning"] else ""
        print(f"Headroom before next tier: {money(r['headroom_before_next_tier'])} "
              f"(crossing costs {money(r['next_tier_extra_annual_household'])}/yr more){warn}")
    print()


def main():
    p = argparse.ArgumentParser(description="IRMAA tier and savings calculator")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--magi", type=float, help="IRMAA MAGI (AGI + tax-exempt interest)")
    g.add_argument("--agi", type=float, help="AGI (Form 1040 line 11); combine with --tax-exempt")
    p.add_argument("--tax-exempt", type=float, default=0.0, help="Tax-exempt interest (Form 1040 line 2a)")
    p.add_argument("--status", required=True, choices=["single", "joint", "mfs"])
    p.add_argument("--year", type=int, default=2026, help="Premium year (default 2026)")
    p.add_argument("--both-on-medicare", action="store_true", help="Joint filers: count 2 people")
    p.add_argument("--new-magi", type=float, help="Estimated MAGI after a life-changing event (SSA-44)")
    p.add_argument("--add", type=float, help="What-if: add this income (e.g. Roth conversion, gain)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    yd = load_year(a.year)
    magi = a.magi if a.magi is not None else a.agi + a.tax_exempt
    people = 2 if (a.status == "joint" and a.both_on_medicare) else 1

    out = {"year": a.year, "status": a.status, "data_status": yd["status"],
           "source": yd["source"], "current": evaluate(magi, a.status, yd, people)}
    if a.new_magi is not None:
        out["after_ssa44"] = evaluate(a.new_magi, a.status, yd, people)
        out["ssa44_annual_savings_estimate"] = round(
            out["current"]["surcharge_annual_household"] - out["after_ssa44"]["surcharge_annual_household"], 2)
    if a.add is not None:
        out["what_if"] = evaluate(magi + a.add, a.status, yd, people)
        out["what_if_extra_annual_cost"] = round(
            out["what_if"]["surcharge_annual_household"] - out["current"]["surcharge_annual_household"], 2)

    if a.json:
        print(json.dumps(out, indent=2))
        return

    print_report(out["current"], "Current", a.year, yd, a.status)
    if "after_ssa44" in out:
        print_report(out["after_ssa44"], "After SSA-44 (estimated new MAGI)", a.year, yd, a.status)
        print(f">> Estimated SSA-44 savings: {money(out['ssa44_annual_savings_estimate'])}/yr\n")
    if "what_if" in out:
        print_report(out["what_if"], f"What-if: +{money(a.add)} income", a.year, yd, a.status)
        print(f">> Extra IRMAA cost of that income: {money(out['what_if_extra_annual_cost'])}/yr\n")
    print(f"Source: CMS {a.year} fact sheet ({yd['source']}). Estimates only; SSA makes the final determination.")


if __name__ == "__main__":
    main()
