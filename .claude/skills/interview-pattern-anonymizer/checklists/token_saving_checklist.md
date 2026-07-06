# Token-Saving Checklist

The workflow is designed to run in many small chats. Keep each one cheap.

## Before starting

- [ ] Read `NEXT_ACTION.md` and `PROJECT_STATE.md` first — do not
      reconstruct history from chat or by re-reading old outputs.
- [ ] This chat does ONE stage for ONE unit of work (one transcript in
      Stage 1; one synthesis, composite, or check in later stages).
- [ ] Load only the files the current stage's playbook lists as inputs.

## Stage discipline (what may be read at each stage)

| Stage | May read | Must NOT read |
|---|---|---|
| 1 Extract | ONE interview's prepared chunks | other interviews |
| 2 Synthesize | pattern maps only | raw/prepared transcripts |
| 3 Composite | synthesis map only | pattern maps, transcripts |
| 4 Risk check | composite draft only | everything upstream |
| 5 Validate | validator report | everything upstream |

- [ ] After Stage 1, raw and prepared transcripts are never opened again.

## During the task

- [ ] Long transcripts are chunked (the prepare script handles this; use
      `--chunk-words` to shrink further if needed).
- [ ] Write full results to files; keep chat replies to paths + short
      summaries.
- [ ] Do not paste file contents into chat unless the user asks.

## Before ending

- [ ] `PROJECT_STATE.md` updated, `RUN_LOG.md` appended, `NEXT_ACTION.md`
      rewritten so a fresh chat can continue with zero prior context,
      `MANIFEST.csv` current.
- [ ] Closing summary is 5 lines or fewer: done / files touched / next /
      warnings.
