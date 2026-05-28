---
id: H01
title: Free tutoring increases attendance
status: testing
parent: null
children: [H01a, H01b]
date_proposed: 2026-04-01
date_resolved: null
---

## Claim

Districts that adopted the free after-school tutoring program experienced increased daily attendance rates, identified by staggered rollout timing across districts.

## Courtroom

- **Estimand:** ATT of the tutoring program on daily attendance rate (percentage points)
- **Population:** Students in grades 3-8 in districts that adopted in Spring 2026
- **Variation:** Staggered district-level adoption; early adopters (Jan 2026) vs. later adopters (Sep 2026)
- **Mechanism:** Districts opted in through a competitive grant application; selection on observable characteristics (enrollment size, prior attendance, poverty rate)
- **Falsification:** Same design in Fall 2025 (pre-program) should yield null
- **Sub-claims:** Urban districts (H01a) and rural districts (H01b) may respond differently due to transportation barriers and alternative activities

## Kills It

1. Pre-trends are not parallel — attendance was already diverging before program start
2. Placebo estimate (Fall 2025) is statistically significant at the 5% level
3. Effect disappears when controlling for concurrent district-level policies (confounders)

## Evidence

- [2026-04-10: Urban ATT = 2.3pp](../insights/2026-04-10_urban_att.md) → H01a confirmed
- [2026-04-15: Placebo is null](../insights/2026-04-15_rural_pretrends.md) → falsification passes
