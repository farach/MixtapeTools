---
date: 2026-04-15
title: Placebo ATT is null — falsification passes
updates: H01a
result: confirmed
script: scripts/r/07_falsification.R
output: output/figures/placebo_event_study.pdf
---

## Finding

Placebo ATT = 0.1 percentage points (SE = 0.7, 95% CI [-1.3, 1.5], p = 0.87). Applying the same TWFE specification to Fall 2025 (before the tutoring program existed) yields a precisely estimated null. The design does not produce false positives.

## Key Numbers

| Metric | Value |
|---|---|
| Placebo ATT | 0.1 pp |
| Standard Error | 0.7 |
| 95% CI | [-1.3, 1.5] |
| p-value | 0.87 |
| Specification | Same as main (district + week FE, district clusters) |
| Placebo period | Sep–Dec 2025 |
| N (district-weeks) | 791 |

## Context

- Uses identical specification to the main result (D01, D03 decisions)
- Treatment date is artificially set to the same calendar week in 2025
- Same districts classified as "treated" and "control"
- Pre-trends in the placebo period are also flat

## Implication

This is the critical falsification test. The null result confirms that the main ATT (2.3pp) is not an artifact of the research design. H01a can now move to `confirmed` status.
