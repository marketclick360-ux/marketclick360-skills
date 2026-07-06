# Stage 4 — Identifiability Risk Check

## Purpose

Adversarially review a composite profile for re-identification risk. Assume
the role of someone motivated to trace the profile back to a real person: a
viewer who knows the source interviews well, a family member, a neighbor, or
the interviewee themselves. Your job is to find what they would find.

## Questions you MUST answer, one by one

1. **Single-source traceability** — Does any part of this profile feel
   traceable to ONE specific interview rather than a pattern across many?
2. **Exact or rare details** — Are there exact ages, dates, years, places,
   or details rare enough (unusual jobs, rare family structures, distinctive
   events) to narrow the field to a few people?
3. **Memorable phrasing** — Are there phrases that read like quotes or close
   paraphrases — wording distinctive enough that a viewer of the source
   material would recognize it?
4. **Rare-trait combinations** — Are multiple individually-safe traits
   combined into a fingerprint? (Three common traits together can be rarer
   than one uncommon trait.)
5. **Trauma specificity** — Are any trauma or adversity details specific
   enough that the person who lived them would recognize their own story?
6. **Insider recognition** — Could someone familiar with the source
   interviews — or with the person — plausibly say "I know who that is"?
7. **Real-person implication** — Does anything in the profile imply it
   describes a real individual? Is the required "Fictionalized anonymized
   composite" label present and unambiguous?

## Standards for judging

- Err on the side of flagging. A false alarm costs a rewrite; a miss costs
  someone their privacy.
- Judge combinations, not just single details.
- "Generalized" is not enough if the generalization is still narrow
  (e.g. "a city in the mountain West known for tourism" is a location).

## Produce EXACTLY this output

### 1. Risk Rating
One of: **Low / Medium / High**, with a one-paragraph justification.
- **Low** — pattern-level throughout; no plausible path to a person.
- **Medium** — mostly safe, but one or more elements need generalizing.
- **High** — at least one element could plausibly identify a source.

### 2. Specific Risk Flags
A numbered list. For each flag: the passage or element (described, not
quoted at length), which of the seven questions it fails, and why.

### 3. Safer Replacement Suggestions
For every flag, a concrete rewrite suggestion that keeps the pattern but
removes the risk (e.g. "replace the named type of workplace with 'a
physically demanding job'").

### 4. Final Recommendation
**PASS** (publishable as-is), or **FAIL** (must be revised and re-checked).
A Medium rating with unresolved flags is a FAIL. When in doubt, FAIL — the
composite can always be revised and re-reviewed.
