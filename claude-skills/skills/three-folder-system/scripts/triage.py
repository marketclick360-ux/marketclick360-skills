#!/usr/bin/env python3
"""Scaffold and triage a workspace into the three-folder system.

Usage:
    python triage.py init --base DIR                # create the three folders
    python triage.py scan --base DIR                # inventory loose files (read-only)
    python triage.py apply PLAN.tsv --base DIR      # preview moves (dry run)
    python triage.py apply PLAN.tsv --base DIR --yes  # actually move

PLAN.tsv format (one file per line, tab-separated):
    relative/or/absolute/path<TAB>atlas|projects|end-products

scan never reads file contents and never moves anything. apply refuses moves
outside --base and dry-runs unless --yes is given. Only printed output enters
Claude's context.
"""

import sys
from pathlib import Path

FOLDERS = {
    "atlas": "01 Atlas",
    "projects": "02 Projects",
    "end-products": "03 End Products",
}


def base_dir(argv):
    if "--base" in argv:
        return Path(argv[argv.index("--base") + 1]).expanduser().resolve()
    return Path.cwd().resolve()


def cmd_init(base):
    base.mkdir(parents=True, exist_ok=True)
    for name in FOLDERS.values():
        target = base / name
        target.mkdir(exist_ok=True)
        print(f"ok: {target}")


def cmd_scan(base):
    if not base.is_dir():
        sys.exit(f"error: not a directory: {base}")
    skip = set(FOLDERS.values())
    entries = [
        p for p in sorted(base.iterdir())
        if p.name not in skip and not p.name.startswith(".")
    ]
    if not entries:
        print(f"clean: no loose items in {base}")
        return
    print(f"loose items in {base} ({len(entries)}):")
    for p in entries:
        kind = "dir " if p.is_dir() else "file"
        try:
            stat = p.stat()
            size = stat.st_size
            import datetime
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime).date().isoformat()
        except OSError:
            size, mtime = 0, "?"
        print(f"  {kind}  {mtime}  {size:>10}  {p.name}")


def cmd_apply(base, plan_path, do_moves):
    plan_file = Path(plan_path).expanduser()
    if not plan_file.is_file():
        sys.exit(f"error: plan not found: {plan_file}")
    moves, errors = [], []
    for lineno, line in enumerate(plan_file.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2 or parts[1] not in FOLDERS:
            errors.append(f"line {lineno}: expected 'path<TAB>{'|'.join(FOLDERS)}': {line}")
            continue
        src = (base / parts[0]).resolve() if not Path(parts[0]).is_absolute() else Path(parts[0]).resolve()
        if base not in src.parents and src != base:
            errors.append(f"line {lineno}: outside --base, refusing: {src}")
            continue
        if not src.exists():
            errors.append(f"line {lineno}: missing: {src}")
            continue
        dest = base / FOLDERS[parts[1]] / src.name
        if dest.exists():
            errors.append(f"line {lineno}: destination exists, refusing overwrite: {dest}")
            continue
        moves.append((src, dest))
    for e in errors:
        print(f"SKIP  {e}")
    for src, dest in moves:
        if do_moves:
            dest.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dest)
            print(f"MOVED {src.name} -> {dest.parent.name}/")
        else:
            print(f"WOULD {src.name} -> {dest.parent.name}/")
    mode = "moved" if do_moves else "dry-run (add --yes to move)"
    print(f"done: {len(moves)} {mode}, {len(errors)} skipped")


def main():
    argv = sys.argv[1:]
    if not argv:
        sys.exit(__doc__)
    cmd, base = argv[0], base_dir(argv)
    if cmd == "init":
        cmd_init(base)
    elif cmd == "scan":
        cmd_scan(base)
    elif cmd == "apply":
        positional, i = [], 1
        while i < len(argv):
            if argv[i] == "--base":
                i += 2
                continue
            if not argv[i].startswith("--"):
                positional.append(argv[i])
            i += 1
        if not positional:
            sys.exit("error: apply needs a PLAN.tsv path")
        cmd_apply(base, positional[0], "--yes" in argv)
    else:
        sys.exit(f"error: unknown command '{cmd}'\n{__doc__}")


if __name__ == "__main__":
    main()
