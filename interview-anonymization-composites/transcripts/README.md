# /transcripts — source interview files

Place your interview transcript files here as plain **.txt** or **.md**
files. This folder is the ONLY input the workflow reads.

## Rules

- Files must be added **manually** by you. Nothing in this project downloads
  videos, scrapes websites, or fetches transcripts from the internet.
- One file per interview. If an interview spans several files, give them the
  same prefix (e.g. `interview_05_a.txt`, `interview_05_b.txt`) — but a
  single file per interview keeps the grouping cleanest.
- This `README.md` is skipped automatically.
- The preparation script **never modifies files in this folder** — cleaned
  copies are written to `outputs/prepared_transcripts/`.

## Privacy

Everything in this folder is private working material. The project
`.gitignore` excludes all transcript files (and all generated outputs) from
version control so raw interview content is never committed. Keep it that
way.

## Next step

```
python src/prepare_transcripts.py
```
