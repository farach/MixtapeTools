---
name: gtd
description: Warrant-first research GTD system. Manages the capture-clarify-organize-reflect-engage cycle for causal inference research. Scaffolds hypotheses/, insights/, decisions/ directories. Interrogates conjectures, files results, tracks binding decisions, checks pipeline freshness, drives the courtroom checklist.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
argument-hint: '[init | conjecture | insight | decide | pipeline | status | courtroom]'
---

# /gtd — Warrant-First Research GTD

## Philosophy

Research with an AI thinking partner is iterated dialogue between human judgment and agent throughput, where every cycle either strengthens a warrant or kills a claim. The harness is whatever machinery makes that dialogue fast, honest, and recoverable.

**Four elements:**

| Element | Definition | Role of dialogue |
|---|---|---|
| **Frame** | A question worth asking | Interrogated by dialogue |
| **Work** | A way to interrogate it | Supervised by dialogue (agents make this cheap) |
| **Warrant** | A way to know you've earned the answer | Built by dialogue — **this is the product** |
| **Dialogue** | The substrate across all three | Human and agent argue their way to claims that hold |

**The binding constraint has shifted.** Pre-agents, Work was binding (coding, cleaning, drafting). Agents make Work cheap. The binding constraint is now Frame and Warrant — what to ask, and whether you've earned the answer. Design the harness around that reallocation.

---

## Commands

### `/gtd init`

Creates the directory structure in the current project:
```
hypotheses/INDEX.md    — DAG of testable claims
insights/INDEX.md      — Atomic findings with provenance
decisions/INDEX.md     — Binding commitments that constrain the pipeline
dashboard.html         — Visual status (serves from localhost)
scripts/build_dashboard_data.py — Regenerates dashboard_data.json
```

Then asks: "What's the first claim you want to test?"

### `/gtd conjecture`

The **clarify** step. Adversarial interrogation:

1. You state something you believe.
2. I run the **courtroom checklist**:
   - **Estimand:** What parameter are you trying to learn?
   - **Population:** On whom?
   - **Variation:** What source of variation identifies it?
   - **Mechanism:** What's the treatment assignment process?
   - **Falsification:** What specific result would kill this?
   - **Sub-claims:** Can this decompose into independently testable pieces?
3. We agree on the precise statement.
4. I write `hypotheses/HXX_slug.md` and update INDEX.

### `/gtd insight`

File a result:
1. What did we find? (One sentence, exact numbers.)
2. Which hypothesis does it speak to?
3. What **pipeline script** produced it? (Must be pipeline, not ad hoc.)
4. Is the figure fresh? (Script timestamp vs. output timestamp.)

Writes `insights/YYYY-MM-DD_slug.md`, updates the linked hypothesis, regenerates `dashboard_data.json`.

### `/gtd decide`

Commit a binding design choice:
1. What's the decision?
2. Why? (One sentence.)
3. What does it constrain downstream?

Writes to `decisions/INDEX.md`. Updates CLAUDE.md if the decision persists across sessions.

### `/gtd pipeline`

Check freshness:
1. For each output, is the source script newer? → stale.
2. Does every figure trace to a pipeline script? → orphans flagged.
3. When was the pipeline last verified?

Runs `python3 scripts/build_dashboard_data.py` and reports.

### `/gtd status`

Quick orientation: hypothesis DAG, pipeline freshness, next actions.

### `/gtd courtroom`

Walk through the DiD checklist stage by stage:
1. **Show Bite** — the event was real
2. **Event Studies** — dynamic effects, pre-trends = 0
3. **Falsification** — placebo finds nothing
4. **Main Results** — headline ATT
5. **Mechanisms** — why, heterogeneity

For each: present the exhibit, interrogate it, confirm or flag. Populates the manuscript view as we go. After completion, draft the narrative from confirmed material in the chosen voice.

---

## The Courtroom (DiD Checklist)

Every quasi-experimental study presents its case. The courtroom is the general form — not just DiD but any design that requires:

1. A first-order effect to exist (show bite)
2. A credible counterfactual (event study / pre-trends)
3. Falsification of confounders (placebo period)
4. The estimate itself (main results)
5. Understanding of why (mechanisms)

Two cross-cutting standards apply to ALL stages:
- **Beautiful** — figures and tables communicate clearly
- **Verified** — pipeline reproducibility, referee2 audits, number consistency

---

## File Formats

### Hypothesis (`hypotheses/HXX_slug.md`)

```markdown
---
id: H01a
status: conjecture | testing | confirmed | rejected | complicated
parent: H01
date_proposed: 2026-05-19
---

## Claim
[One sentence, testable.]

## Courtroom
- Estimand: [what parameter]
- Population: [on whom]
- Variation: [what identifies it]
- Falsification: [what kills it]

## Evidence
- [links to insights, added as they accumulate]
```

### Insight (`insights/YYYY-MM-DD_slug.md`)

```markdown
---
date: 2026-04-10
updates: H01a
result: confirmed | rejected | complicated
stage: [2, 4]           # optional — courtroom stage(s) this speaks to. Overrides keyword matching.
script: scripts/r/05_estimate_did.R
output: output/figures/event_study.pdf
---

## Finding
[The fact. Numbers. Script path. What it means for the hypothesis.]

## Key Numbers
[Table with point estimate, SE, CI, p-value, N]

## Context
[Specification details, baseline, relative magnitude]
```

### Decision (`decisions/INDEX.md`)

Table format. One row per binding decision:
```
| ID | Decision | Date | Rationale |
|---|---|---|---|
| D01 | Primary estimator is TWFE with district and week FE | 2026-04-01 | Sufficient pre-periods; no staggered-timing bias |
```

---

## Status Transitions

```
conjecture → testing:      First pipeline script assigned to test this hypothesis
testing → confirmed:       Positive evidence + falsification passes (Stages 2-4 confirmed)
testing → rejected:        Evidence contradicts + falsification confirms the negative
testing → complicated:     Evidence mixed OR falsification fails
complicated → confirmed:   Complication resolved (new evidence or new design)
complicated → rejected:    Further investigation confirms failure
```

**Rules:**
- A hypothesis CANNOT move to `confirmed` without passing falsification (Stage 3)
- A hypothesis CAN move directly from `conjecture` to `rejected` (if "kills it" condition met immediately)
- `complicated` is NOT terminal — it requires resolution
- Parent hypothesis status = worst child status (if any child is `complicated`, parent is at most `testing`)

---

## Pipeline Levels

| Level | Name | Contains | Example |
|---|---|---|---|
| 1 | Cleaning | Raw → clean; format standardization | `00_clean_survey.py` |
| 2 | Derived | Clean → derived variables; joins, constructs | `02_build_panel.py` |
| 3 | Classification | Derived → treatment/control assignment | `03_classify_treated.py` |
| 4 | Figures | Descriptive outputs, maps, timelines | `04_descriptive_figures.R` |
| 5 | Estimation | Causal inference; the main results | `05_estimate_did.R` |

**Rules:**
- A level-N script may only read outputs from levels < N
- Numbering within level is sequential (00, 01, 02...)
- Language suffix indicates the tool (.py, .R, .do)
- Every output in `output/figures/` must map to exactly one pipeline script

---

## Freshness

Freshness is computed dynamically by comparing file modification times:
- `output.mtime >= script.mtime` → **FRESH** (output generated after script was last modified)
- `output.mtime < script.mtime` → **STALE** (script changed since output was generated)
- Output does not exist → **MISSING**

Freshness is NEVER stored as a permanent field. It is always computed at runtime by `build_dashboard_data.py`. The `fresh` field in insight frontmatter is a snapshot at filing time — the dashboard recomputes it.

---

## INDEX.md Formats

### `hypotheses/INDEX.md` — Hierarchical DAG

```markdown
# Hypothesis DAG

## H01 — Main Claim
Status: **testing**
One sentence description.

### H01a — Sub-claim
Status: **confirmed** (date)
One sentence description.
```

Two levels: parent hypotheses (##) and children (###). Each entry has bold status inline.

### `insights/INDEX.md` — Table

```markdown
# Insights Log

| Date | Finding | Hypothesis | Status |
|---|---|---|---|
| 2026-04-15 | [Placebo is null](file.md) | H01a | confirmed |
| 2026-04-10 | [Urban ATT = 2.3pp](file.md) | H01a | confirmed |
```

Most recent first. Links to individual insight files.

---

## Courtroom → Dashboard Flow

When `/gtd courtroom` confirms a stage:
1. The relevant insight(s) are filed (if not already)
2. The linked hypothesis status may update
3. `build_dashboard_data.py` regenerates the JSON
4. Dashboard Courtroom tab shows the stage as confirmed (green)
5. Dashboard Manuscript tab allows the confirmed material to appear

When `/gtd courtroom` flags a stage as complicated:
1. An insight is filed with `result: complicated`
2. The linked hypothesis moves to `complicated`
3. Dashboard Courtroom tab shows the stage with a yellow indicator
4. Manuscript tab moves that material to "Unearned"

---

## Hooks

Only add hooks for failures that are **silently wrong** (produce plausible but incorrect output).

**Do hook:** Classification file changes but county file not rebuilt → wrong treatment set → wrong ATT → presented wrong numbers. Silent failure. Hook it.

**Don't hook:** Missing figure → LaTeX won't compile. Visible failure. Don't hook it.

Starter hook (adapt paths to your project):
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "command": "if echo \"$TOOL_INPUT\" | grep -q 'LINCHPIN_FILE_NAME'; then echo '⚠️ PIPELINE DEPENDENCY: Rebuild downstream'; fi"
    }]
  }
}
```

---

## Dashboard

The dashboard (`dashboard.html`) reads from `dashboard_data.json` generated by `scripts/build_dashboard_data.py`. It shows:

- **Status** — pipeline freshness, hypothesis summary, latest finding, next actions
- **Courtroom** — 5-stage checklist with expandable evidence panels
- **Pipeline** — scripts grouped by level with freshness indicators
- **Hypotheses** — claim DAG with color-coded status
- **Decisions** — binding commitments table
- **Figures** — all outputs: pipeline vs. orphaned, fresh vs. stale
- **Manuscript** — only confirmed claims with fresh evidence appear here; unearned claims are listed separately

Serve with: `cd project_root && python3 -m http.server 8080`

---

## GTD Mapping

| GTD Stage | Research Equivalent | Mechanism |
|---|---|---|
| **Capture** | Ideas emerge through dialogue | The chat itself |
| **Clarify** | Courtroom checklist + interrogation | `/gtd conjecture` or `/gtd courtroom` |
| **Organize** | Commit to directory | `hypotheses/` `decisions/` `CLAUDE.md` |
| **Reflect** | Dashboard review | `dashboard.html` |
| **Engage** | Run the pipeline | `scripts/` → `output/` |

---

## Principles

1. **The pipeline is the source of truth.** A figure only counts if it traces to a numbered pipeline script.
2. **Freshness is visible.** You should never wonder whether an output is current.
3. **Decisions bind.** Once committed, they constrain downstream work across sessions.
4. **Hypotheses are falsifiable.** Every one has a "kills it" condition written before the test.
5. **The conversation is the inbox.** It generates ideas. The directory captures them.
6. **Warrant is the product.** Not the coefficient — the structure that earns the right to assert it.
7. **Verification is cheap and constant.** Not a quality gate at the end.
