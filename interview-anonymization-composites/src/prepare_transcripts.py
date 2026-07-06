#!/usr/bin/env python3
"""Prepare raw interview transcripts for anonymized pattern analysis.

Reads .txt and .md files from /transcripts, strips or flags obvious
identifying metadata, splits long transcripts into manageable chunks, and
writes cleaned markdown files to /outputs/prepared_transcripts/.

Original files in /transcripts are never modified or overwritten.

Safety posture: default to caution. Anything that looks like an identifier
is either removed outright (URLs, emails, phones, handles, timestamps) or
wrapped in a visible [FLAG:...] marker so that downstream prompt stages are
forced to generalize or exclude it. False positives in flagging are
acceptable; false negatives are the real risk.

Usage:
    python src/prepare_transcripts.py [--chunk-words N]

Requires Python 3.11+. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS_DIR = PROJECT_ROOT / "transcripts"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "prepared_transcripts"

DEFAULT_CHUNK_WORDS = 1500  # target words per output chunk

# ---------------------------------------------------------------------------
# Removal patterns (replaced entirely — these carry no analytic value)
# ---------------------------------------------------------------------------

RE_URL = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_PHONE = re.compile(
    r"(?<!\d)(?:\+?\d{1,2}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"
)
# Social handles — matched AFTER emails are removed so we don't clip addresses.
RE_HANDLE = re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,30}\b")
# Timestamps: [00:12:34], (12:34), or bare 00:12:34 / 12:34 markers.
RE_TIMESTAMP = re.compile(r"[\[(]?\b\d{1,2}:\d{2}(?::\d{2})?\b[\])]?")

# ---------------------------------------------------------------------------
# Generalization patterns (replaced with a neutral placeholder)
# ---------------------------------------------------------------------------

RE_AGE = re.compile(
    r"\b(?:aged?\s+\d{1,3}|\d{1,3}[\s-]*(?:years?|yrs?)[\s-]*old"
    r"|when\s+(?:I|he|she|they)\s+(?:was|were)\s+\d{1,3})\b",
    re.IGNORECASE,
)
RE_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
RE_DATE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\[YEAR\])?\b"
)

# Capitalized words that are almost always ordinary sentence-position words,
# not names/places. Anything capitalized and NOT in this set gets flagged.
COMMON_CAPITALIZED = {
    "A", "About", "After", "All", "An", "And", "Are", "As", "At", "Back",
    "Because", "Before", "But", "Can", "Could", "Dad", "Did", "Do", "Does",
    "Don", "Even", "Every", "Everybody", "Everyone", "Everything", "God",
    "Had", "Has", "He", "Her", "His", "How", "I", "If", "In", "Interviewer",
    "Is", "It",
    "Just", "Like", "Look", "Man", "Maybe", "Me", "Mom", "Mother", "Father",
    "My", "No", "Nobody", "Not", "Nothing", "Now", "Of", "Oh", "Okay", "On",
    "One", "Or", "Our", "Out", "People", "Right", "She", "So", "Some",
    "Sometimes", "Speaker", "That", "The", "Then", "There", "These", "They",
    "Things", "This", "Those", "To", "Was", "We", "Well", "Were", "What",
    "When", "Where", "Which", "Who", "Why", "Will", "With", "Would", "Yeah",
    "Yes", "You", "Your",
}

# A run of one or more Capitalized words (possibly with initials/apostrophes),
# e.g. "Nashville", "San Diego", "Mary Jo". Flagged unless every word in the
# run is a common capitalized word.
RE_PROPER_RUN = re.compile(
    r"\b(?:[A-Z][a-z]{1,}|[A-Z]\.)(?:['’][A-Za-z]+)?"
    r"(?:\s+(?:[A-Z][a-z]{1,}|[A-Z]\.)(?:['’][A-Za-z]+)?)*\b"
)

# Line-start speaker label, e.g. "MARK:", "Interviewer:", "John Smith:".
RE_SPEAKER_LINE = re.compile(
    r"^\s*(?P<label>[A-Z][A-Za-z.'’-]*(?:\s+[A-Z][A-Za-z.'’-]*){0,2}|[A-Z]{2,15})"
    r"\s*:\s+"
)
INTERVIEWER_LABELS = {"interviewer", "host", "q", "question", "int"}


def scrub_metadata(text: str, stats: Counter) -> str:
    """Remove URLs, emails, phones, handles, timestamps; generalize ages/dates."""
    def count_sub(pattern: re.Pattern, repl: str, key: str, s: str) -> str:
        s, n = pattern.subn(repl, s)
        stats[key] += n
        return s

    text = count_sub(RE_URL, "[URL REMOVED]", "urls", text)
    text = count_sub(RE_EMAIL, "[EMAIL REMOVED]", "emails", text)
    text = count_sub(RE_PHONE, "[PHONE REMOVED]", "phones", text)
    text = count_sub(RE_HANDLE, "[HANDLE REMOVED]", "handles", text)
    text = count_sub(RE_TIMESTAMP, "", "timestamps", text)
    text = count_sub(RE_AGE, "[AGE GENERALIZED]", "ages", text)
    text = count_sub(RE_YEAR, "[YEAR]", "years", text)
    text = count_sub(RE_DATE, "[DATE GENERALIZED]", "dates", text)
    return text


def generalize_speaker_labels(lines: list[str], stats: Counter) -> list[str]:
    """Replace obvious line-start speaker labels with generic ones.

    A label is treated as a speaker label only if the same label starts at
    least two lines (or is a known interviewer word) — this avoids mangling
    one-off prose like "Note: ...".
    """
    counts: Counter[str] = Counter()
    for line in lines:
        m = RE_SPEAKER_LINE.match(line)
        if m:
            counts[m.group("label")] += 1

    out = []
    for line in lines:
        m = RE_SPEAKER_LINE.match(line)
        if m:
            label = m.group("label")
            if counts[label] >= 2 or label.lower() in INTERVIEWER_LABELS:
                generic = (
                    "Interviewer:" if label.lower() in INTERVIEWER_LABELS
                    else "Speaker:"
                )
                line = RE_SPEAKER_LINE.sub(generic + " ", line, count=1)
                stats["speaker_labels"] += 1
        out.append(line)
    return out


def flag_proper_nouns(text: str, stats: Counter, flagged: Counter) -> str:
    """Wrap likely names/places in [FLAG:...] markers.

    We deliberately over-flag: any capitalized run containing a word not in
    the common-words set is marked. Downstream prompts treat every flagged
    span as identifying material that must be generalized or excluded.
    """
    def repl(m: re.Match) -> str:
        run = m.group(0)
        words = run.replace("’", "'").split()
        if all(w.rstrip(".").strip("'") in COMMON_CAPITALIZED for w in words):
            return run
        # Skip placeholders we introduced ourselves (e.g. YEAR inside brackets
        # is handled by never matching inside [...] — see caller).
        stats["flags"] += 1
        flagged[run] += 1
        return f"[FLAG:{run}]"

    # Protect existing [...] placeholders from being re-processed.
    parts = re.split(r"(\[[^\]\n]*\])", text)
    return "".join(p if p.startswith("[") else RE_PROPER_RUN.sub(repl, p)
                   for p in parts)


def split_into_chunks(text: str, chunk_words: int) -> list[str]:
    """Split text into chunks of roughly chunk_words, on paragraph boundaries."""
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[list[str]] = [[]]
    count = 0
    for para in paragraphs:
        n = len(para.split())
        if count and count + n > chunk_words:
            chunks.append([])
            count = 0
        chunks[-1].append(para)
        count += n
    return ["\n\n".join(c) for c in chunks if c]


def chunk_header(source: Path, idx: int, total: int, flagged: Counter) -> str:
    today = datetime.date.today().isoformat()
    lines = [
        f"<!-- Prepared transcript chunk — generated {today} -->",
        "",
        "> **PRIVATE WORKING MATERIAL — never quote, republish, or closely",
        "> paraphrase this text in any final output.**",
        ">",
        f"> Source file: `{source.name}` | Chunk {idx} of {total}",
        ">",
        "> `[FLAG:...]` markers are likely identifying details (names, places,",
        "> organizations). All later stages MUST generalize or exclude them.",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def process_file(path: Path, chunk_words: int) -> tuple[int, Counter, Counter]:
    stats: Counter = Counter()
    flagged: Counter = Counter()

    text = path.read_text(encoding="utf-8", errors="replace")
    # Scrub metadata first so leading timestamps don't hide speaker labels.
    text = scrub_metadata(text, stats)
    lines = generalize_speaker_labels(
        [line.lstrip() for line in text.splitlines()], stats
    )
    text = flag_proper_nouns("\n".join(lines), stats, flagged)
    # Collapse whitespace artifacts left behind by removals.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    chunks = split_into_chunks(text, chunk_words)
    total = len(chunks)
    stem = re.sub(r"[^\w-]+", "_", path.stem).strip("_").lower()

    for i, chunk in enumerate(chunks, start=1):
        suffix = f"_part{i:02d}" if total > 1 else ""
        out_path = OUTPUT_DIR / f"{stem}{suffix}.md"
        out_path.write_text(
            chunk_header(path, i, total, flagged) + chunk + "\n",
            encoding="utf-8",
        )
    return total, stats, flagged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--chunk-words", type=int, default=DEFAULT_CHUNK_WORDS,
        help=f"target words per output chunk (default {DEFAULT_CHUNK_WORDS})",
    )
    args = parser.parse_args()

    if not TRANSCRIPTS_DIR.is_dir():
        print(f"ERROR: transcripts folder not found at {TRANSCRIPTS_DIR}.\n"
              "Create it and place your .txt/.md transcript files inside.")
        return 1

    sources = sorted(
        p for p in TRANSCRIPTS_DIR.iterdir()
        if p.suffix.lower() in {".txt", ".md"} and p.name.lower() != "readme.md"
    )
    if not sources:
        print(f"No .txt or .md transcripts found in {TRANSCRIPTS_DIR}.\n"
              "Add transcript files there (README.md is ignored) and re-run.")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print("PREPARE TRANSCRIPTS  —  originals are read-only, never modified")
    print("=" * 68)

    grand = Counter()
    for path in sources:
        n_chunks, stats, flagged = process_file(path, args.chunk_words)
        grand.update(stats)
        print(f"\n• {path.name}  →  {n_chunks} chunk(s) written")
        print(f"    removed: {stats['urls']} URLs, {stats['emails']} emails, "
              f"{stats['phones']} phones, {stats['handles']} handles, "
              f"{stats['timestamps']} timestamps")
        print(f"    generalized: {stats['ages']} ages, {stats['years']} years, "
              f"{stats['dates']} dates, {stats['speaker_labels']} speaker labels")
        print(f"    flagged for exclusion: {stats['flags']} likely "
              f"names/places ({len(flagged)} distinct)")
        if flagged:
            top = ", ".join(w for w, _ in flagged.most_common(8))
            print(f"    most frequent flags: {top}")

    print("\n" + "-" * 68)
    print(f"Done. {len(sources)} file(s) processed → {OUTPUT_DIR}")
    print("Flags are NOT removed — they are markers. Review the prepared")
    print("files; downstream prompt stages must generalize or exclude every")
    print("[FLAG:...] span. Next: python src/build_prompt_packets.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
