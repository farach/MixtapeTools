# Warrant-First Research GTD

> **⚠️ Harness work in progress.** This system is under active development. The dashboard server template and GTD protocol are being refined through real use on the AI agents / minimum wage R&R project. Treat as stable enough to copy and adapt, not stable enough to treat as finished.

---

A system for conducting empirical research with an AI thinking partner. It makes research dialogue **recoverable**, claims **falsifiable**, and the current state of knowledge **always visible**.

---

## The Problem It Solves

Research with AI is iterated dialogue. But dialogue is ephemeral — sessions end, context compresses, the human forgets, and the AI has amnesia. Without external structure, every session starts cold and repeats old mistakes.

This system externalizes the research state into a directory that both human and AI can consult. The dashboard is the shared workspace between two amnesiacs. It is always current, always visual, always structured. Nothing exists until it is filed. Nothing is asserted until it is earned through the courtroom.

---

## Who This Is For

A researcher who:
- Works with an AI thinking partner across many sessions
- Needs to constantly verify progress visually (cannot hold the project state in memory)
- Conducts quasi-experimental causal inference (DiD, SynthDiD, event studies)
- Cares about the difference between "the code runs" and "the code is correct"
- Needs fixed structure that does not sprawl or creep

---

## Philosophy

Four elements define the research process:

| Element | What it is | Where it lives |
|---|---|---|
| **Frame** | A question worth asking | `hypotheses/` |
| **Work** | A way to interrogate it | `scripts/` (the pipeline) |
| **Warrant** | A way to know you've earned the answer | Courtroom + Narrative |
| **Dialogue** | The substrate connecting all three | The conversation (captured into `insights/`, `decisions/`) |

**The binding constraint has shifted.** Pre-agents, Work was binding (coding, cleaning, drafting). Agents make Work cheap. The binding constraint is now Frame and Warrant — what to ask, and whether you've earned the answer.

**Warrant is the product.** Not the coefficient — the structure that earns the right to assert it.

---

## The Dashboard

A live Python server (`dashboard_server.py`) that reads the filesystem on every page load. No build step. No stale JSON. Always current.

### Navigation (4 groups, 12 tabs)

```
Output ──────────
  Narrative        The current best understanding. Present-tense. Updates in place.
  Overview         Hypothesis counts, pipeline health, recent audits.

Structure ───────
  Courtroom        5 stages of proof. Evidence assigned to stages.
  Checklist        9 mechanical DiD steps. File-existence check.
  Code             Pipeline scripts (green) + Stale code (yellow). Click to view.
  Data             Source datasets with descriptions, provenance, previews.

Evidence ────────
  Hypotheses       DAG of claims. Every path taken, including dead ends.
  Insights         Chronological log of findings with numbers.
  Decisions        Binding design choices that constrain the pipeline.
  Figures          Flippable cards — click to see source script on the back.
  Tables           LaTeX and CSV table sources.

Reference ───────
  Skills           All installed Claude Code skills with descriptions.
```

### What Is Frozen (never changes without a code edit)

- The 5 courtroom stages (Show Bite → Mechanisms)
- The 9 checklist steps (Target Parameter → Sensitivity)
- The pipeline DAG (which scripts exist, their levels, expected outputs)
- The figure-to-script mapping
- The data catalog (source names, descriptions, provenance)
- The tab structure and navigation groups
- The color semantics (green=confirmed, yellow=testing, red=complicated)

### What Is Live (computed fresh on every request)

- Hypothesis statuses (read from `hypotheses/H*.md` frontmatter)
- Insight log (read from `insights/2*.md`)
- Decisions table (read from `decisions/INDEX.md`)
- Pipeline freshness (file mtime comparison)
- Figure freshness and orphan detection
- Code file listing
- Narrative text (read from `narrative.md`)
- Audit history (read from `audits/`)

---

## The Filing Discipline

**Findings don't exist until filed.** A result produced in conversation has no ontological status until it passes through `/gtd insight` and lands in `insights/`. Filing requires:

1. Exact numbers (not "we found an effect")
2. Which hypothesis it speaks to
3. Which pipeline script produced it (ad hoc doesn't count)
4. Whether the figure is fresh

This is not bureaucracy — it is the mechanism that ensures the narrative only contains earned claims.

---

## Code Tiers

| Tier | Meaning | Dashboard appearance |
|---|---|---|
| **Pipeline** | Accepted. In the DAG. Produces official outputs. | Green dot in Code tab |
| **Stale** | Under consideration. Not yet in the DAG. Cannot appear in courtroom. | Yellow border in Code tab |
| **Deprecated** | Witnessed and archived. Superseded by pipeline scripts. | Moved to `deprecated/` folder |

Promotion from stale to pipeline happens through `/gtd audit`. Demotion to deprecated happens when a pipeline script replaces it.

---

## The Courtroom vs. The Checklist

Both live under "Structure" but serve different purposes:

**The Courtroom** (5 stages) is the **quality test** — does the evidence hold up under interrogation?
1. Show Bite — the event was real
2. Event Studies — dynamic effects, pre-trends = 0
3. Falsification — placebo period must find nothing
4. Main Results — headline ATT
5. Mechanisms — why, heterogeneity

**The Checklist** (9 steps) is the **existence test** — do we have the mechanical artifacts?
1. Target parameter
2. Treatment timing table
3. Treatment rollout plot
4. Outcomes by cohort
5. Covariate balance
6. Propensity scores / overlap
7. Estimate (CS/SynthDiD)
8. Event study
9. Sensitivity (HonestDiD / Oster bounds)

A checklist step can be "done" (file exists) while the courtroom stage it maps to is "complicated" (the evidence doesn't hold up). The checklist says "you did the work." The courtroom says "the work earned the claim."

---

## The Narrative

**Narrative** = What we currently believe is true. Always present-tense. When evidence updates, the narrative updates in place — you never see the edit history, only the current state. It is the emerging story, honest and rooted in confirmed material. If a hypothesis was confirmed then complicated, the narrative says the complicated thing, not the history.

**Overview** = Operational health. Counts, freshness, what's next. Pure project management.

---

## The Audit Protocol

`/gtd audit [topic]` — systematic interrogation of any part of the project. One question at a time.

Five steps, asked sequentially:

1. **What is it?** Forces alignment. Claude states what we're looking at. User confirms.
2. **Is it correct?** Does it do what we think? Fresh? Matches binding decisions?
3. **Does it belong?** Pipeline vs. stale? Courtroom vs. hypothesis log?
4. **What's next?** Promote, archive, rerun, file, update status. Execute immediately.
5. **Update narrative?** Given what we resolved, should the story change?

Audit records are saved to `audits/YYYY-MM-DD_slug.md` and appear in the Overview tab.

---

## Production and Verification Are Continuous

This is not a system where you build something and then verify it at the end. Production and verification happen simultaneously, constantly. Every figure produced is immediately checked for freshness. Every insight filed is immediately mapped to a courtroom stage. Every hypothesis has a "kills it" condition written before the test runs.

The dashboard enforces this by making staleness, orphans, and misfilings visible the instant they occur. You never wonder whether something is current. You never wonder whether a claim is earned. The structure makes invisible problems visible — and visible problems get fixed.

---

## Skills

The full skill set that complements this system:

| Skill | When to use |
|---|---|
| `/gtd` | Manage the research: conjecture, insight, decide, audit, status |
| `/referee2` | Independent audit — the producer cannot grade its own work |
| `/blindspot` | Peripheral vision — what are you not seeing? |
| `/voice` | Narrative composition in Weitzman, Pollak, or Blend |
| `/beautiful_deck` | Presentation from confirmed material |
| `/tikz` | Visual collision check for generated figures |
| `/bibcheck` | Bibliography audit before submission |
| `/split-pdf` | Deep reading of academic papers |

---

## Installation

### User-level (works in all projects):
```bash
cp -r gtd/ ~/.claude/skills/gtd/
```

### Project-level (one project only):
```bash
cp -r gtd/ your_project/.claude/skills/gtd/
```

### Scaffold in a new project:
```
/gtd init
```

---

## Principles

1. **The pipeline is the source of truth.** A figure only counts if it traces to a numbered pipeline script.
2. **Freshness is visible.** You never wonder whether an output is current.
3. **Decisions bind.** Once committed, they constrain downstream work across sessions.
4. **Hypotheses are falsifiable.** Every one has a "kills it" condition written before the test.
5. **The conversation is the inbox.** It generates ideas. The directory captures them.
6. **Warrant is the product.** Not the coefficient — the structure that earns the right to assert it.
7. **Verification is cheap and constant.** Not a quality gate at the end.
8. **Filing is the ontological gate.** Unfiled results do not exist.
9. **The dashboard is the shared workspace.** Between a human who cannot hold the project in memory and an AI that forgets between sessions.
