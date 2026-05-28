# Dashboard Tabs — Field by Field

Each tab in the dashboard serves a specific purpose. No overlap. No redundancy.

---

## Output Group

### Narrative

**What it is:** The current best understanding of what is true. Present-tense. Updates in place.

**What it is NOT:** A log of what we tried. That's the Hypotheses tab. The narrative only shows the current state — if something was confirmed then complicated, it says the complicated thing.

**How it's populated:** Reads from `narrative.md`. If that file is a placeholder, auto-assembles from confirmed hypotheses and insights. Once you author the narrative, the auto-assembly never runs again.

**When to update it:** After every audit (step 5 asks: "Update narrative?"). After courtroom stages are confirmed. Whenever the current truth changes.

**Verification features (automatic):**
- **Drift detection:** If narrative.md references a hypothesis ID (H01a, H04, etc.) whose status is not "confirmed," a red warning banner appears at the top listing the problematic references.
- **Inline status badges:** Hypothesis IDs in the narrative text are annotated with colored badges showing their current status (green/yellow/red). No tab-switch needed to verify whether a claim is currently earned.
- **Expandable reasons:** Click a red (complicated) or yellow (testing) badge to expand a one-line explanation of WHY it has that status, pulled from the hypothesis file's "Kills it" section. Click again to collapse.

**Relationship to other tabs:** Draws from Hypotheses (claims) and Insights (evidence). The Courtroom confirms material that enters the narrative.

---

## Structure Group

### Overview

**What it is:** Operational health at a glance. Hypothesis counts by status, pipeline freshness ratio, latest insight, recent audits.

**What it is NOT:** The argument. That's the Courtroom and Narrative. Overview is pure project management.

**How it's populated:** Computed live from hypothesis files (status counts), pipeline scripts (freshness), insights (latest), and audit records (recent cards).

**The audit cards:** Click to expand. Show topic, conclusion, and whether the narrative was updated.

---

### Courtroom

**What it is:** The five stages of proof that earn the right to assert a causal claim. Evidence-based. Each stage must be confirmed before the material can appear in the Narrative or Manuscript.

**The five stages:**
1. **Show Bite** — The event was real. Maps, volume, timeline.
2. **Event Studies** — Dynamic effects. Pre-treatment coefficients = 0.
3. **Falsification** — Placebo period must find nothing.
4. **Main Results** — Headline ATT.
5. **Mechanisms** — Heterogeneity, channels, why.

**Status colors:** Green (confirmed), yellow (complicated), grey (no evidence yet).

**How evidence maps to stages:** Auto-detected by keywords in insight titles. An insight titled "Placebo is null" maps to Stage 3. An insight titled "ATT = 2.3pp" maps to Stage 4.

**What it is NOT:** The mechanical checklist. The courtroom is "does the evidence hold up?" The checklist is "do we have the artifacts?"

---

### Checklist

**What it is:** Nine mechanical DiD steps. A recipe. Status is determined by file existence — does the expected output exist?

**The nine steps:**
1. Target parameter (defined in decisions)
2. Treatment timing table
3. Treatment rollout plot
4. Outcomes by cohort
5. Covariate balance
6. Propensity scores / overlap
7. Estimate (CS/SynthDiD)
8. Event study
9. Sensitivity (HonestDiD / Oster bounds)

**Status colors:** Green (output exists), yellow (partial), red (missing), grey (no expected output defined).

**What it is NOT:** Quality judgment. A step can be "done" (file exists) while the corresponding courtroom stage is "complicated" (evidence doesn't hold up). The checklist says you did the work. The courtroom says the work earned the claim.

---

### Code

**What it is:** Unified code viewer. Left panel splits into two sections: Pipeline (green header, with freshness dots) and Stale (yellow header, with yellow border). Click any file to view syntax-highlighted source in the right panel.

**Pipeline scripts:** In the DAG. Produce official outputs. Green dot = fresh (output newer than script). Yellow dot = stale (script modified since last run).

**Stale scripts:** Not in the DAG. Cannot appear in the courtroom or checklist. Must be promoted to pipeline via `/gtd audit` to become official.

**What it is NOT:** An editor. View-only. Changes happen in your IDE.

---

### Data

**What it is:** Catalog of source datasets. Each entry shows: descriptive name, description, source, collection period, which scripts consume it, which figures it produces, and a preview of the first few rows.

**How it's populated:** A curated catalog (`DATA_CATALOG` in the server) defines the sources. The server auto-checks file existence, computes sizes, and reads CSV previews live.

**What it is NOT:** A listing of intermediate/derived files. Those are produced by the pipeline. The Data tab shows raw sources only.

---

## Evidence Group

### Hypotheses

**What it is:** The audit trail. Every claim ever filed, including dead ends and rejected ideas. Parent/child DAG structure. Color-coded by status.

**Statuses:**
- `conjecture` — stated but untested
- `testing` — pipeline script assigned
- `confirmed` — evidence positive + falsification passed
- `complicated` — evidence mixed or falsification failed
- `rejected` — evidence contradicts the claim

**What it is NOT:** The current truth. That's the Narrative. Hypotheses show the path taken, including wrong turns. The narrative shows only where we ended up.

---

### Insights

**What it is:** Chronological log of empirical findings. Each has a date, title, linked hypothesis, and result status. The factual record.

**Requirements to file:** Exact numbers. Hypothesis link. Pipeline script provenance. No ad hoc results.

---

### Decisions

**What it is:** Binding design choices. Once committed, they constrain all downstream work across sessions. One row per decision.

**Fields:** ID, Decision (one sentence), Date, Rationale.

**What makes a decision binding:** It cannot be reversed without a new decision that explicitly supersedes it. Scripts must respect it. The courtroom assumes it.

---

### Figures

**What it is:** Gallery of all PNG figures in `output/figures/`. Each figure is a **flippable card** — click to flip and see the source script, file path, modification date, and a link to view the full source code.

**Border colors:**
- Green = fresh (output newer than its source script)
- Yellow = stale (source script modified since figure was generated)
- Grey = orphaned (no source script mapped)

**Why flippable:** For someone who cannot mentally visualize a figure while reading code in another tab, the card flip provides immediate co-presentation — the figure and its provenance in one gesture.

---

### Tables

**What it is:** LaTeX (`.tex`) and CSV table files from `output/tables/`. Click to view syntax-highlighted source.

---

## Reference Group

### Skills

**What it is:** All installed Claude Code skills with their names, argument hints, and one-line descriptions. A reference so you never have to remember what's available.

**Invoke with:** `/skill_name [args]` in Claude Code.
