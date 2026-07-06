# Privacy Checklist

Run through this before starting any stage, and again before saving any
output. Every unchecked box means stop and fix.

## Source handling

- [ ] No video/audio was downloaded; no site was scraped; no transcript or
      caption was fetched from the internet.
- [ ] Only local files from `transcripts/` (or their prepared derivatives)
      are being used.
- [ ] No raw transcript text is pasted back into chat.
- [ ] No transcripts, titles, URLs, or names have been placed inside the
      Skill folder.

## Content of the output being saved

- [ ] No direct quotes of any length.
- [ ] No close paraphrases or distinctive turns of phrase.
- [ ] No real names, aliases, street/stage names, or similar-sounding names.
- [ ] No exact locations (cities, neighborhoods, streets, named facilities —
      jails, rehabs, shelters, motels, hospitals).
- [ ] No exact ages, dates, or years.
- [ ] No rare jobs, rare family structures, or unusual detail combinations.
- [ ] No unique trauma details or recognizable story beats — themes only.
- [ ] No gang/crew names; no specific charges or sentences.
- [ ] No raw YouTube metadata (titles, URLs, episode identifiers).
- [ ] Every `[FLAG:...]` span from prepared transcripts was generalized or
      excluded — none carried forward.

## Composite-specific gates

- [ ] Every source-derived element recurs across **3+ separate interviews**
      (verified against the synthesis map, not memory).
- [ ] The label "Fictionalized anonymized composite" is present and the
      text never implies a real person.
- [ ] Rare-trait combination check done: no fingerprint of individually
      safe details.
- [ ] Tone is humane and documentary — no voyeurism, no
      trauma-as-spectacle.
- [ ] `python src/validate_outputs.py` run and no high-risk findings.
- [ ] Stage 4 risk check is PASS at Low risk.

**Default rule: when in doubt, generalize or exclude.**
