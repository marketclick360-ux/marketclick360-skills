#!/usr/bin/env python3
"""Scaffold the brain-dump week file and print its path.

Usage:
    python new_week.py           # this ISO week
    python new_week.py --next    # next ISO week (for carry-over)

Creates ~/brain-dump/weeks/<YYYY>-W<ww>.md with the standard skeleton if it
doesn't exist, then prints the absolute path (and whether it was created).
Only the printed output enters Claude's context.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

TEMPLATE = """# Week {iso} ({start} – {end})

## Raw Dump

<!-- Paste the unfiltered stream here, verbatim. Never edited. -->

## Organized

<!-- Built by the brain-dump skill per processing-rules.md -->
"""


def main() -> None:
    day = date.today()
    if "--next" in sys.argv[1:]:
        day += timedelta(weeks=1)
    year, week, _ = day.isocalendar()
    iso = f"{year}-W{week:02d}"
    monday = date.fromisocalendar(year, week, 1)
    sunday = date.fromisocalendar(year, week, 7)

    weeks_dir = Path.home() / "brain-dump" / "weeks"
    weeks_dir.mkdir(parents=True, exist_ok=True)
    path = weeks_dir / f"{iso}.md"

    if path.exists():
        print(f"exists: {path}")
    else:
        path.write_text(
            TEMPLATE.format(iso=iso, start=monday.isoformat(), end=sunday.isoformat()),
            encoding="utf-8",
        )
        print(f"created: {path}")

    profile = Path.home() / "brain-dump" / "profile.md"
    if not profile.exists():
        print("warning: no profile.md — run Setup (calibration) first")


if __name__ == "__main__":
    main()
