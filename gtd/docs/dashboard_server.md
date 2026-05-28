# The Live Dashboard Server

## Architecture

A single Python file (`dashboard_server.py`, ~700 lines) that replaces both the build step and the file server. Uses only the standard library (`http.server`). No pip installs required.

```
GET /                    → Full dashboard HTML (rendered server-side)
GET /api/code?path=X    → Raw file content for the code viewer (AJAX)
GET /output/figures/*   → Static file serving (images)
GET /scripts/*          → Static file serving (source code)
```

## Why A Server Instead of Static HTML

The dashboard must never be stale. A static HTML file with a JSON build step introduces a failure mode: you edit a hypothesis, forget to rebuild, and the dashboard lies to you.

The server reads the filesystem on every page load. Edit a file, refresh the browser, see the change. No intermediate step. No cache. The server IS the build step.

## What Gets Scanned On Every Request

| Function | Reads | Produces |
|---|---|---|
| `scan_hypotheses()` | `hypotheses/H*.md` | Frontmatter + claims + evidence |
| `scan_insights()` | `insights/2*.md` | Findings log |
| `scan_decisions()` | `decisions/INDEX.md` | Binding decisions table |
| `scan_pipeline()` | Script files + output files (mtime) | Freshness status |
| `scan_figures()` | `output/figures/*.png` | Gallery with provenance |
| `scan_code_files()` | `scripts/**/*.py`, `*.R` | File listing |
| `scan_data()` | `DATA_CATALOG` + filesystem | Source dataset status |
| `scan_stale_code()` | Scripts not in `PIPELINE_SCRIPTS` | Unregistered code list |
| `scan_audits()` | `audits/2*.md` | Recent audit cards |

## Color Semantics (Consistent Across All Tabs)

| Color | Meaning |
|---|---|
| Green | confirmed / fresh / done / exists |
| Yellow | testing / stale / partial / complicated |
| Red | rejected / missing |
| Grey | pending / todo / orphaned |

## The Frozen Skeleton

These are hardcoded in the server and define the structure of the project:

- **`PIPELINE_SCRIPTS`** — The DAG. Which scripts exist, their levels, expected outputs.
- **`FIGURE_SCRIPT_MAP`** — Which figure comes from which script.
- **`COURTROOM_STAGES`** — The 5 proof stages with their keywords for insight mapping.
- **`CHECKLIST_STEPS`** — The 9 mechanical steps with expected output files.
- **`DATA_CATALOG`** — Source datasets with descriptions and provenance.

To add a script to the pipeline, edit `PIPELINE_SCRIPTS`. To map a new figure, edit `FIGURE_SCRIPT_MAP`. These are intentionally manual — promoting something to the pipeline is a deliberate act.

## Running It

```bash
cd your_project
python3 dashboard_server.py
# Open http://localhost:8080/
```

Or double-click `open_dashboard.command` which kills any existing server, starts fresh, and opens the browser.

## Design Constraints

- Single file. No external dependencies. No templates to lose.
- Python 3.9+ (system Python on macOS).
- Dark theme. Inter font for prose, SF Mono for code.
- 200px sidebar nav. Sticky. Scrollable.
- All HTML rendered server-side (no client-side framework). Only the Code viewer uses AJAX.
- Figures served as static files from the project directory.
