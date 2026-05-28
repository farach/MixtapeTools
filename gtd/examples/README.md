# Example: Effect of Free Tutoring on School Attendance

A worked example showing the GTD system applied to a simple policy evaluation.

## The Study

A state launched a free after-school tutoring program in Spring 2026. Districts could opt in through a grant application. Adoption was staggered: some districts started in January 2026, others not until September 2026. We use the staggered rollout as a natural experiment to estimate the program's effect on daily attendance rates.

## Design

- **Estimator:** Two-way fixed effects (district + week FE), difference-in-differences
- **Treatment group:** Districts that adopted in January 2026
- **Control group:** Districts that adopted later (September 2026) — not-yet-treated
- **Outcome:** Daily attendance rate (percent of enrolled students present)
- **Falsification:** Same design applied to Fall 2025 (no program existed)

## What this example demonstrates

| GTD Feature | Example |
|---|---|
| Parent hypothesis with children | H01 (overall effect) → H01a (urban), H01b (rural) |
| Confirmed hypothesis | H01a passes all courtroom stages |
| Testing hypothesis | H01b still awaiting rural estimation |
| Binding decisions | D01-D04 lock in estimator, treatment date, clustering, sample |
| Insight with numbers | ATT = 2.3pp with full statistical detail |
| Falsification insight | Placebo null confirms design validity |
| INDEX formats | Hierarchical DAG (hypotheses) and table (insights) |

## Pipeline (what the scripts would be)

```
scripts/python/00_clean_attendance.py   → data/clean/attendance_panel.csv
scripts/python/01_clean_demographics.py → data/clean/district_demographics.csv
scripts/python/02_build_panel.py        → data/derived/analysis_panel.csv
scripts/python/03_classify_treated.py   → data/derived/treatment_assignment.csv
scripts/r/04_descriptive_figures.R      → output/figures/enrollment_map.pdf
scripts/r/05_estimate_did.R             → output/figures/urban_event_study.pdf
scripts/r/06_estimate_rural.R           → output/figures/rural_event_study.pdf
scripts/r/07_falsification.R            → output/figures/placebo_event_study.pdf
```
