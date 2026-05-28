# Interrogation Protocols

How each `/gtd` command works, step by step. No philosophy here — just the procedure.

---

## `/gtd init`

**What it creates:**

```
hypotheses/INDEX.md
insights/INDEX.md
decisions/INDEX.md
dashboard.html
scripts/build_dashboard_data.py
dashboard_data.json
```

**What Claude does after scaffolding:**

1. Creates the directories and files above.
2. Copies `dashboard.html` from the skill template.
3. Copies `build_dashboard_data.py` from the skill template.
4. Asks: "What's the first claim you want to test?"
5. If the user answers, immediately enters the `/gtd conjecture` flow below.

---

## `/gtd conjecture`

**Trigger:** User states a belief. Can be vague ("I think X causes Y") or precise.

**Protocol — 6 questions, asked one at a time:**

| # | Question | What Claude is looking for | Follow-up if vague |
|---|---|---|---|
| 1 | **Estimand:** What parameter are you trying to learn? | A named quantity (ATT, ATE, LATE, elasticity, proportion). Not "the effect of X on Y" — the specific parameter. | "Is this the average effect on the treated, or on everyone? What units?" |
| 2 | **Population:** On whom? | A defined group with inclusion/exclusion criteria. | "What ages? What geography? What time period? Who's excluded?" |
| 3 | **Variation:** What source of variation identifies it? | The quasi-experiment, randomization, or natural variation being exploited. | "What changed, for whom, and when? Why would some units be affected and others not?" |
| 4 | **Mechanism:** What's the treatment assignment process? | How units ended up treated vs. control. The selection story. | "Did they choose? Were they assigned? What determined exposure?" |
| 5 | **Falsification:** What specific result would kill this? | A testable prediction that, if violated, means the design fails. Must be concrete. | "If your design is valid, what should we see in a period with no treatment? What pattern would prove this is spurious?" |
| 6 | **Sub-claims:** Can this decompose into independently testable pieces? | Whether the claim has sub-hypotheses that can be tested separately. | "Are there subgroups where the effect might differ? Is there a mechanism you can test independently of the main result?" |

**After the 6 questions:**

1. Claude proposes the one-sentence testable claim. Format: "[Population] experienced [direction] [outcome] due to [variation], identified by [design]."
2. User approves or revises.
3. Claude assigns the next available ID:
   - Top-level: H01, H02, H03...
   - Children: H01a, H01b, H01c...
4. Claude writes `hypotheses/HXX_slug.md` with frontmatter + Claim + Courtroom + Evidence sections.
5. Claude updates `hypotheses/INDEX.md` (adds entry under parent or as new top-level).
6. Claude reports: "Filed as H01a. Kills it: [the falsification condition]. Next: run [what script would test this]."

**The file that gets written:**

```markdown
---
id: H01a
title: Urban districts respond to tutoring
status: conjecture
parent: H01
children: []
date_proposed: 2026-04-08
date_resolved: null
---

## Claim

Students in urban districts that adopted the free tutoring program experienced a 2-4 percentage point increase in daily attendance, identified by staggered rollout across districts.

## Courtroom

- **Estimand:** ATT of tutoring program on daily attendance rate (percentage points)
- **Population:** Students in grades 3-8 in urban districts (RUCC 1-3) that adopted in Spring 2026
- **Variation:** Staggered district-level adoption; early adopters (Jan 2026) vs. later adopters (Sep 2026)
- **Mechanism:** District opted in based on grant application; selection on observable district characteristics
- **Falsification:** Same design applied to Fall 2025 (pre-program) should yield null. Pre-trends in attendance should be parallel.
- **Sub-claims:** None — this is a sub-claim of H01

## Kills It

1. Pre-trends are not parallel (attendance was already diverging before program start)
2. Falsification period (Fall 2025) shows a "treatment effect" of similar magnitude

## Evidence

[empty until insights are filed]
```

---

## `/gtd insight`

**Trigger:** A result was produced (figure, table, estimate). User wants to record it.

**Protocol — 5 steps:**

**Step 1: "What did we find?"**
- Must include numbers. Not "we found an effect" but "ATT = 2.3pp (SE = 0.8, p = 0.004)."
- If the user gives a vague finding, Claude asks: "What's the exact number? What's the confidence interval or standard error?"

**Step 2: "Which hypothesis does this speak to?"**
- Claude lists all hypotheses with status ≠ rejected for reference.
- User picks one (by ID or description).
- If the result doesn't map to any existing hypothesis, Claude asks: "Should we file a new conjecture first?"

**Step 3: "What script produced it?"**
- Must be a pipeline script (numbered, in `scripts/`).
- Claude checks if the file exists. If not: "That script doesn't exist. Is this from an ad-hoc analysis? Pipeline results only — should we create the script first?"
- Records the script path.

**Step 4: "What's the result?"**
- `confirmed` — The evidence supports the hypothesis as stated.
- `rejected` — The evidence contradicts the hypothesis.
- `complicated` — The evidence is mixed, unexpected, or requires interpretation.
- Claude asks the user to choose and explain in one sentence why.

**Step 5: Claude writes and updates.**

What gets written:
1. `insights/YYYY-MM-DD_slug.md` — the insight file
2. Updates the linked hypothesis's Evidence section (appends a link)
3. Updates the hypothesis status IF appropriate:
   - If result = confirmed AND this is the first confirming evidence → hypothesis moves to `testing` (not yet `confirmed` — needs falsification)
   - If result = rejected → hypothesis moves to `rejected`
   - If result = complicated → hypothesis moves to `complicated`
   - If result = confirmed AND falsification has already passed → hypothesis moves to `confirmed`
4. Updates `insights/INDEX.md` (prepends to table)
5. Runs `build_dashboard_data.py` to regenerate `dashboard_data.json`

**The file that gets written:**

```markdown
---
date: 2026-04-10
title: Urban ATT is 2.3pp
updates: H01a
result: confirmed
script: scripts/r/05_estimate_did.R
output: output/figures/urban_event_study.pdf
---

## Finding

ATT = 2.3 percentage points (SE = 0.8, 95% CI [0.7, 3.9], p = 0.004). Urban districts that adopted the tutoring program saw a statistically significant increase in daily attendance relative to not-yet-treated districts. Effect is stable across event-study leads 1-4.

## Context

- Baseline urban attendance: 91.2%
- Effect magnitude: 2.5% relative increase
- Specification: Two-way fixed effects with district and week FE, clustered at district level
- N = 847 district-weeks (142 districts × ~6 weeks post-treatment)
```

---

## `/gtd decide`

**Trigger:** A design choice needs to be locked in. Something that constrains downstream work.

**Protocol — 4 steps:**

**Step 1: "What's the decision?"**
- Must be one sentence, actionable, unambiguous.
- Bad: "We should probably use DiD." Good: "Primary estimator is TWFE with district and week fixed effects."

**Step 2: "Why?"**
- One sentence rationale.
- Must reference either evidence or a practical constraint.

**Step 3: "What does it constrain downstream?"**
- Claude asks what scripts, specifications, or future choices this locks in.
- Example: "This means all estimation scripts must include district FE. It means we cannot use a specification without week FE as a robustness check unless we justify the departure."

**Step 4: Claude writes.**

1. Assigns next DXX ID.
2. Appends one row to `decisions/INDEX.md`.
3. If the decision affects session-persistent knowledge (e.g., variable definitions, sample restrictions), Claude asks: "Should I also update CLAUDE.md with this?"

**The row that gets appended:**

```
| D04 | Primary estimator is TWFE with district and week FE | 2026-04-08 | Sufficient pre-periods for event study; no staggered-timing concern in this design |
```

---

## `/gtd pipeline`

**Trigger:** User asks "is anything stale?" or wants to verify the pipeline.

**Protocol:**

1. Claude runs: `python3 scripts/build_dashboard_data.py`
2. Reports the output in three categories:

**Fresh** (output newer than script):
```
✓ scripts/python/00_clean_survey.py → data/clean/survey_panel.csv [fresh, 2026-04-10 14:30]
```

**Stale** (script newer than output — needs rerun):
```
✗ scripts/r/05_estimate_did.R → output/figures/urban_event_study.pdf [STALE — script modified 2026-04-12, output from 2026-04-10]
```

**Missing** (output doesn't exist):
```
✗ scripts/r/07_falsification.R → output/figures/placebo_event_study.pdf [MISSING]
```

**Orphaned figures** (in output/ but not mapped to any pipeline script):
```
? output/figures/exploratory_scatter.png [ORPHANED — no pipeline script]
```

3. Summary line: "Pipeline: 6/8 fresh, 1 stale, 1 missing. 2 orphaned figures."
4. Recommended action: "Rerun `scripts/r/05_estimate_did.R` to refresh the stale output."

---

## `/gtd status`

**Trigger:** "Where are we?" Quick orientation.

**Protocol — Claude reports 4 things:**

1. **Hypothesis summary:**
   ```
   Hypotheses: 1 confirmed, 2 testing, 1 complicated, 0 rejected (4 total)
   ```

2. **Latest insight:**
   ```
   Latest: 2026-04-15 — Placebo event study is null (H01a falsification passes)
   ```

3. **Pipeline health:**
   ```
   Pipeline: 7/8 fresh, 1 stale (scripts/r/05_estimate_did.R)
   ```

4. **Next actions** (derived from hypothesis statuses):
   ```
   Next actions:
   - H01b (testing): Need to run estimation on rural subsample
   - H01a (confirmed): Ready for courtroom — all evidence in, falsification passed
   ```

---

## `/gtd courtroom`

**Trigger:** The user is ready to walk through the full evidence chain. This is the final interrogation before a hypothesis (or the whole study) can be declared "earned."

**Overview:** Five stages, each interrogated independently. A stage can be:
- **Confirmed** (green) — exhibit presented, interrogated, holds up
- **Complicated** (yellow) — exhibit exists but has problems
- **Missing** (gray) — no exhibit yet

Claude walks through one stage at a time. Does NOT skip ahead.

---

### Stage 1: Show Bite

**What it establishes:** The event/treatment was real, observable, and reached the study population.

**Claude asks:**
1. "What's your exhibit for the event itself? (Timeline, media coverage, policy announcement.)"
2. "Who picked it up? What's the geographic/demographic reach?"
3. "How persistent was exposure? Days, weeks, months?"
4. "Show me the figure or data that documents this."

**Confirmed when:**
- There is a documented timeline with dates
- Geographic/demographic reach is quantified
- A figure or table shows the treatment intensity or coverage
- The exhibit traces to a pipeline script

**Complicated when:**
- The event timing is ambiguous (gradual rollout, no clear start date)
- Coverage data is incomplete
- The figure is from ad-hoc analysis (not in pipeline)

**What Claude does after:**
- Files an insight if not already filed
- Marks Stage 1 status in the courtroom record
- Reports: "Stage 1 (Show Bite): CONFIRMED. The event is documented. Moving to Stage 2."

---

### Stage 2: Event Studies

**What it establishes:** Dynamic treatment effects exist and pre-trends are zero.

**Claude asks:**
1. "Show me the event study plot. What's on each axis?"
2. "Are the pre-treatment coefficients jointly zero? What's the F-test or visual pattern?"
3. "When does the effect begin? Is it immediate or gradual?"
4. "How many pre-periods do you have? Is this sufficient?"

**Confirmed when:**
- Event study figure shows clear zero pre-trends
- Post-treatment coefficients are significant and in the expected direction
- Pre-treatment joint F-test fails to reject the null
- Figure traces to a pipeline script

**Complicated when:**
- One or two pre-period coefficients are marginally significant
- The effect appears before the treatment date
- Insufficient pre-periods (fewer than 3)

---

### Stage 3: Falsification

**What it establishes:** The design doesn't produce false positives in periods without treatment.

**Claude asks:**
1. "What's the placebo period? (Must be a time/place with no treatment.)"
2. "Show me the placebo estimate. What's the ATT?"
3. "Is it statistically zero? Confidence interval includes zero?"
4. "Is the placebo estimated with the same specification as the main result?"

**Confirmed when:**
- Placebo ATT is statistically zero (p > 0.10, CI includes zero)
- Same specification as main results (same FE, same clustering, same sample definition)
- Placebo period is credible (not contaminated by spillovers or anticipation)

**Complicated when:**
- Placebo ATT is marginally significant (p between 0.05 and 0.10)
- Placebo is from a different specification than the main result
- There's a plausible explanation for a non-zero placebo that doesn't invalidate the main result

**Critical rule:** A hypothesis CANNOT move to `confirmed` without passing Stage 3. If falsification fails, the hypothesis is `complicated` at best.

---

### Stage 4: Main Results

**What it establishes:** The headline estimate — the number that answers the research question.

**Claude asks:**
1. "What's the ATT? (Point estimate, SE, CI, p-value.)"
2. "What specification produces this? (Fixed effects, controls, clustering.)"
3. "How robust is it? What happens if you change the specification?"
4. "Is this estimate from a fresh pipeline script?"

**Confirmed when:**
- Point estimate is statistically significant at conventional levels
- Result is robust to reasonable alternative specifications
- The output is fresh (not stale)
- The number is consistent with the event study dynamics from Stage 2

**Complicated when:**
- Sensitive to specification choices
- Significant at 10% but not 5%
- Inconsistent with event study magnitudes

---

### Stage 5: Mechanisms

**What it establishes:** Why the effect exists. Heterogeneity, channels, mediators.

**Claude asks:**
1. "What subgroups did you examine? Any heterogeneity?"
2. "Is there a mediator or channel you can test?"
3. "Does the heterogeneity pattern match the theory?"
4. "Are mechanism results from pipeline scripts?"

**Confirmed when:**
- At least one heterogeneity result is documented
- The pattern is consistent with the proposed mechanism
- Results are from pipeline scripts

**Complicated when:**
- Heterogeneity goes in an unexpected direction
- The mechanism test is inconclusive
- Only ad-hoc exploration, not pipeline

---

### After the courtroom walk-through:

Claude summarizes:
```
Courtroom Status:
  Stage 1 (Show Bite):     ✓ Confirmed
  Stage 2 (Event Studies): ✓ Confirmed
  Stage 3 (Falsification): ✓ Confirmed
  Stage 4 (Main Results):  ✓ Confirmed
  Stage 5 (Mechanisms):    ~ Complicated (heterogeneity unexpected)

Verdict: 4/5 stages confirmed. The main result is EARNED.
Mechanism stage needs resolution before the full narrative is complete.
```

**Dashboard updates:**
- Courtroom tab shows stage-by-stage status (green/yellow/gray)
- Manuscript tab: Stages 1-4 material can be asserted; Stage 5 material is marked "unearned"
- Hypothesis status: If all 5 stages confirmed → `confirmed`. If any stage is complicated → `complicated` with note.

---

## Status Transition Summary

```
conjecture ──→ testing:      First pipeline script is assigned/run
testing ──→ confirmed:       Positive evidence + falsification passes (Stages 2-4 confirmed)
testing ──→ rejected:        Evidence contradicts + falsification confirms the negative
testing ──→ complicated:     Evidence mixed OR falsification fails
complicated ──→ confirmed:   Complication resolved (new evidence or new design)
complicated ──→ rejected:    Further investigation confirms failure
```

**Rules:**
- Cannot reach `confirmed` without passing falsification (Stage 3)
- Can go directly from `conjecture` to `rejected` (if "kills it" condition met immediately)
- `complicated` is NOT terminal — requires resolution
- Parent hypothesis status = worst child status
