#!/usr/bin/env python3
"""Build model-ready prompt packets from prepared transcripts.

Reads cleaned chunks from /outputs/prepared_transcripts/, combines them with
the stage templates in /prompts, and writes ready-to-paste markdown packets
to /outputs/prompt_packets/:

  stage1_extract__<interview>.md   one per source interview
  stage2_synthesis.md              one packet with paste slots per interview
  stage3_composite.md              one packet with a synthesis paste slot
  stage4_risk_check.md             one packet with a composite paste slot

Requires Python 3.11+. Standard library only.
"""

from __future__ import annotations

import datetime
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREPARED_DIR = PROJECT_ROOT / "outputs" / "prepared_transcripts"
PACKETS_DIR = PROJECT_ROOT / "outputs" / "prompt_packets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

TEMPLATES = {
    "extract": "01_extract_patterns.md",
    "synthesis": "02_cross_interview_synthesis.md",
    "composite": "03_composite_generation.md",
    "risk": "04_identifiability_risk_check.md",
}

# Optional per-domain framing embedded in every packet when present.
DOMAIN_CONTEXT_FILE = "00_domain_context.md"

MIN_INTERVIEWS = 3  # the 3-source recurrence rule cannot work below this

PRIVACY_BANNER = """\
> **PRIVATE WORKING MATERIAL.** The source text below is confidential input
> for pattern analysis only. It must NEVER be quoted, closely paraphrased,
> or reproduced in any final output. Treat every `[FLAG:...]` span as an
> identifying detail that must be generalized or excluded. When in doubt,
> generalize or exclude.
"""


def load_template(key: str) -> str:
    path = PROMPTS_DIR / TEMPLATES[key]
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing prompt template: {path}\n"
            "The /prompts folder must contain all four stage templates."
        )
    return path.read_text(encoding="utf-8").strip()


def group_chunks() -> dict[str, list[Path]]:
    """Group prepared chunk files by interview (strip the _partNN suffix)."""
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(PREPARED_DIR.glob("*.md")):
        interview = re.sub(r"_part\d+$", "", path.stem)
        groups[interview].append(path)
    return dict(groups)


def load_domain_context() -> str:
    """Return the optional domain-context block, or an empty string."""
    path = PROMPTS_DIR / DOMAIN_CONTEXT_FILE
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip() + "\n\n---\n"


def packet_header(title: str) -> str:
    today = datetime.date.today().isoformat()
    return (f"<!-- Prompt packet generated {today} — paste this whole file "
            f"into Claude -->\n\n# {title}\n\n{PRIVACY_BANNER}\n---\n"
            + load_domain_context())


def build_stage1(groups: dict[str, list[Path]], template: str) -> list[Path]:
    written = []
    for interview, chunks in groups.items():
        parts = [packet_header(f"Stage 1 — Pattern Extraction: interview "
                               f"`{interview}`"), template, "\n---\n",
                 "## SOURCE MATERIAL (private — analyze, never quote)\n"]
        for chunk in chunks:
            parts.append(f"### {chunk.name}\n")
            parts.append(chunk.read_text(encoding="utf-8").strip())
            parts.append("")
        out = PACKETS_DIR / f"stage1_extract__{interview}.md"
        out.write_text("\n".join(parts) + "\n", encoding="utf-8")
        written.append(out)
    return written


def build_stage2(groups: dict[str, list[Path]], template: str) -> Path:
    interviews = sorted(groups)
    parts = [packet_header("Stage 2 — Cross-Interview Synthesis"), template,
             "\n---\n"]
    if len(interviews) < MIN_INTERVIEWS:
        parts.append(
            f"> ⚠️ **WARNING: only {len(interviews)} interview(s) available.** "
            f"The minimum-recurrence rule requires a trait to appear in at "
            f"least {MIN_INTERVIEWS} separate interviews, so NO composite "
            f"trait can be justified from this set. Add more interviews "
            f"before proceeding past this stage.\n"
        )
    parts.append(f"## Interviews in this set ({len(interviews)})\n")
    parts.extend(f"- `{i}`" for i in interviews)
    parts.append("\n## STAGE 1 PATTERN MAPS (paste each below)\n")
    for i in interviews:
        parts.append(f"### Pattern map — interview `{i}`\n")
        parts.append("<PASTE THE STAGE 1 OUTPUT FOR THIS INTERVIEW HERE>\n")
    out = PACKETS_DIR / "stage2_synthesis.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return out


def build_stage3(template: str) -> Path:
    parts = [packet_header("Stage 3 — Composite Generation"), template,
             "\n---\n",
             "## STAGE 2 SYNTHESIS MAP (paste below)\n",
             "<PASTE THE STAGE 2 CROSS-INTERVIEW SYNTHESIS OUTPUT HERE>\n"]
    out = PACKETS_DIR / "stage3_composite.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return out


def build_stage4(template: str) -> Path:
    parts = [packet_header("Stage 4 — Identifiability Risk Check"), template,
             "\n---\n",
             "## COMPOSITE DRAFT UNDER REVIEW (paste below)\n",
             "<PASTE THE STAGE 3 COMPOSITE PROFILE HERE>\n"]
    out = PACKETS_DIR / "stage4_risk_check.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return out


def main() -> int:
    if not PREPARED_DIR.is_dir() or not any(PREPARED_DIR.glob("*.md")):
        print(f"ERROR: no prepared transcripts found in {PREPARED_DIR}.\n"
              "Run 'python src/prepare_transcripts.py' first.")
        return 1

    try:
        templates = {k: load_template(k) for k in TEMPLATES}
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    PACKETS_DIR.mkdir(parents=True, exist_ok=True)
    groups = group_chunks()

    print("=" * 68)
    print("BUILD PROMPT PACKETS")
    print("=" * 68)
    if (PROMPTS_DIR / DOMAIN_CONTEXT_FILE).is_file():
        print(f"Domain context: prompts/{DOMAIN_CONTEXT_FILE} embedded in "
              "every packet")
    else:
        print("Domain context: none (add prompts/00_domain_context.md to "
              "frame a specific interview set)")

    stage1 = build_stage1(groups, templates["extract"])
    stage2 = build_stage2(groups, templates["synthesis"])
    stage3 = build_stage3(templates["composite"])
    stage4 = build_stage4(templates["risk"])

    print(f"\nInterviews found: {len(groups)} "
          f"({sum(len(v) for v in groups.values())} prepared chunk(s))")
    for p in stage1:
        print(f"  • {p.relative_to(PROJECT_ROOT)}")
    for p in (stage2, stage3, stage4):
        print(f"  • {p.relative_to(PROJECT_ROOT)}")

    if len(groups) < MIN_INTERVIEWS:
        print(f"\n⚠️  WARNING: only {len(groups)} interview(s). The 3-source "
              "recurrence rule means no composite trait can be justified yet. "
              "Add more transcripts before generating composites.")

    print("\nNext: paste each stage1_extract__*.md packet into Claude, save "
          "the outputs to outputs/pattern_maps/, then work through stages "
          "2–4. Finish with: python src/validate_outputs.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
