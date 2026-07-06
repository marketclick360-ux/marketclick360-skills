#!/usr/bin/env python3
"""Validate composite drafts and risk checks for obvious privacy problems.

Scans .md/.txt files in /outputs/composites/ and /outputs/risk_checks/ and
flags patterns that suggest re-identification risk: direct quotes, exact
ages/years/dates, place-like details, name-like details, URLs, phone numbers,
emails, social handles, real-person implications, and overly specific
biographical combinations.

This is a heuristic tripwire, not a guarantee. A clean report does NOT prove
a composite is safe — it only means no obvious machine-detectable problem was
found. The Stage 4 human/model risk check is still required.

Prints a plain-English report and saves it to /outputs/risk_checks/.

Requires Python 3.11+. Standard library only.
"""

from __future__ import annotations

import datetime
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPOSITES_DIR = PROJECT_ROOT / "outputs" / "composites"
RISK_DIR = PROJECT_ROOT / "outputs" / "risk_checks"
REPORT_PREFIX = "validation_report"  # our own reports are skipped when scanning

US_STATES = (
    "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|"
    "Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|"
    "Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|"
    "Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|"
    "New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|"
    "Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|"
    "Virginia|Washington|West Virginia|Wisconsin|Wyoming"
)


@dataclass
class Check:
    key: str
    severity: str  # HIGH or MEDIUM
    explanation: str
    pattern: re.Pattern


CHECKS = [
    Check("direct_quote", "HIGH",
          "A long quoted passage — final composites must contain no direct "
          "quotes from source interviews.",
          re.compile(r'["“]([^"”\n]{35,})["”]')),
    Check("exact_age", "HIGH",
          "An exact age — ages must be generalized (e.g. 'as a teenager', "
          "'in midlife').",
          re.compile(r"\b\d{1,3}\s*(?:years?|yrs?)[\s-]*old\b|\baged?\s+\d{1,3}\b",
                     re.IGNORECASE)),
    Check("exact_year", "HIGH",
          "An exact calendar year — replace with a generalized era "
          "(e.g. 'in the early years of adulthood').",
          re.compile(r"\b(?:19|20)\d{2}\b")),
    Check("exact_date", "HIGH",
          "A specific calendar date — dates must not appear in composites.",
          re.compile(r"\b(?:January|February|March|April|May|June|July|August|"
                     r"September|October|November|December)\s+\d{1,2}\b")),
    Check("location", "HIGH",
          "A specific place (city/state, address, or named region) — "
          "locations must be generalized (e.g. 'a mid-sized city').",
          re.compile(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?,\s*[A-Z]{2}\b"
                     r"|\b\d+\s+\w+\s+(?:Street|St|Avenue|Ave|Road|Rd|"
                     r"Boulevard|Blvd|Drive|Dr|Lane|Ln)\b"
                     rf"|\b(?:{US_STATES})\b")),
    Check("name_like", "MEDIUM",
          "A name-like phrase (honorific + name, or two capitalized words) — "
          "composites must not contain real names; verify these are not "
          "person or place names.",
          re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Aunt|Uncle|Pastor|Coach)\.?\s+"
                     r"[A-Z][a-z]+\b")),
    Check("url", "HIGH", "A URL — links to source material must not appear.",
          re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)),
    Check("phone", "HIGH", "A phone number.",
          re.compile(r"(?<!\d)(?:\(\d{3}\)|\d{3})[\s.-]\d{3}[\s.-]\d{4}(?!\d)")),
    Check("email", "HIGH", "An email address.",
          re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    Check("handle", "MEDIUM", "A social-media handle.",
          re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,30}\b")),
    Check("real_person_claim", "HIGH",
          "Wording that implies the composite is a real, specific person — "
          "composites must be clearly labeled fictional.",
          re.compile(r"\b(?:this is a real (?:person|story)|a real person named|"
                     r"(?:his|her|their) real name|true story|actually happened|"
                     r"based on one (?:person|interview|individual)|"
                     r"identifies? (?:him|her|them) as)\b", re.IGNORECASE)),
    Check("unresolved_flag", "HIGH",
          "An unresolved [FLAG:...] marker carried over from a prepared "
          "transcript — the flagged detail was never generalized or excluded.",
          re.compile(r"\[FLAG:[^\]]+\]")),
]

# Categories that, in combination, suggest an overly specific biography.
SPECIFICITY_KEYS = {"exact_age", "exact_year", "exact_date", "location",
                    "name_like"}
SPECIFICITY_THRESHOLD = 2  # 2+ distinct specific categories in one file

MISSING_LABEL_MSG = (
    "Missing the required label 'Fictionalized anonymized composite' — "
    "every composite must carry it."
)


def scan_file(path: Path) -> list[tuple[str, str, int, str]]:
    """Return findings as (severity, message, line_number, snippet)."""
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    hit_categories = set()
    for check in CHECKS:
        for i, line in enumerate(lines, start=1):
            # Skip markdown headings for the name-like heuristic: headings
            # like "Composite Profile" are title-case by convention.
            if check.key == "name_like" and line.lstrip().startswith("#"):
                continue
            for m in check.pattern.finditer(line):
                snippet = m.group(0)[:60]
                findings.append((check.severity,
                                 f"{check.explanation}", i, snippet))
                hit_categories.add(check.key)

    if len(hit_categories & SPECIFICITY_KEYS) >= SPECIFICITY_THRESHOLD:
        findings.append((
            "HIGH",
            "Overly specific biographical combination — this file mixes "
            f"{len(hit_categories & SPECIFICITY_KEYS)} categories of exact "
            "detail (ages/years/dates/places/names). Even individually minor "
            "details can identify someone in combination.", 0, ""))

    # Composites must carry the fictional label.
    if (path.parent == COMPOSITES_DIR
            and "fictionalized anonymized composite" not in text.lower()):
        findings.append(("HIGH", MISSING_LABEL_MSG, 0, ""))

    return findings


def main() -> int:
    targets = []
    for folder in (COMPOSITES_DIR, RISK_DIR):
        if folder.is_dir():
            targets.extend(
                p for p in sorted(folder.iterdir())
                if p.suffix.lower() in {".md", ".txt"}
                and not p.name.startswith(REPORT_PREFIX)
            )

    if not targets:
        print("No composite drafts or risk checks found to validate.\n"
              f"Save Stage 3 outputs to {COMPOSITES_DIR}\n"
              f"and Stage 4 outputs to {RISK_DIR}, then re-run.")
        return 1

    report: list[str] = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report.append(f"# Validation report — {now}\n")
    report.append("This is a heuristic scan for obvious privacy problems. "
                  "A clean result does not guarantee safety; the Stage 4 "
                  "risk-check prompt is still required.\n")

    total_high = total_medium = 0
    for path in targets:
        findings = scan_file(path)
        rel = path.relative_to(PROJECT_ROOT)
        report.append(f"\n## {rel}\n")
        if not findings:
            report.append("PASS — no obvious problems detected.\n")
            continue
        highs = [f for f in findings if f[0] == "HIGH"]
        meds = [f for f in findings if f[0] == "MEDIUM"]
        total_high += len(highs)
        total_medium += len(meds)
        verdict = ("NEEDS REVISION" if highs else "REVIEW RECOMMENDED")
        report.append(f"**{verdict}** — {len(highs)} high-risk and "
                      f"{len(meds)} medium-risk finding(s).\n")
        for severity, msg, line_no, snippet in findings:
            where = f"line {line_no}" if line_no else "whole file"
            shown = f" → `{snippet}`" if snippet else ""
            report.append(f"- **{severity}** ({where}): {msg}{shown}")
        report.append("")

    report.append("\n---\n")
    if total_high:
        report.append(f"**Overall: {total_high} high-risk finding(s) — do not "
                      "publish these drafts. Generalize or remove every "
                      "flagged detail, then re-run this validator and the "
                      "Stage 4 risk check.**")
    elif total_medium:
        report.append(f"**Overall: no high-risk findings, but {total_medium} "
                      "medium-risk item(s) need a human look before the "
                      "drafts are considered safe.**")
    else:
        report.append("**Overall: no obvious problems detected. Still run "
                      "the Stage 4 risk-check prompt before treating any "
                      "composite as final.**")

    report_text = "\n".join(report) + "\n"
    print(report_text)

    RISK_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RISK_DIR / f"{REPORT_PREFIX}_{stamp}.md"
    out.write_text(report_text, encoding="utf-8")
    print(f"Report saved to {out.relative_to(PROJECT_ROOT)}")

    return 2 if total_high else 0


if __name__ == "__main__":
    sys.exit(main())
