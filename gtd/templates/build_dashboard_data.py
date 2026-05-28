#!/usr/bin/env python3
"""
build_dashboard_data.py — Generic template for the GTD research dashboard.

Scans project directories and generates dashboard_data.json:
  - hypotheses/*.md (frontmatter: id, status, title, parent, children)
  - insights/*.md (frontmatter: date, title, updates, result, script, output)
  - decisions/INDEX.md (table rows)
  - output/figures/* (existence + timestamps)
  - scripts/**/* (timestamps for freshness checking)

Customize PIPELINE_SCRIPTS below for your project.

Run: python3 scripts/build_dashboard_data.py
"""

import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
OUT = ROOT / "dashboard_data.json"

# ============================================================================
# CUSTOMIZE THIS FOR YOUR PROJECT
# ============================================================================
# Each entry: script path, list of output paths, pipeline level, display name
PIPELINE_SCRIPTS = [
    # {"script": "scripts/00_clean.py", "outputs": ["data/clean/output.csv"], "level": 1, "name": "Cleaning"},
    # {"script": "scripts/01_estimate.R", "outputs": ["output/figures/main.pdf"], "level": 2, "name": "Estimation"},
]

# Map figure filenames (without extension) to their source pipeline script
FIGURE_SCRIPT_MAP = {
    # "main_result": "scripts/01_estimate.R",
    # "event_study": "scripts/02_event_study.R",
}
# ============================================================================


def parse_frontmatter(filepath):
    """Parse YAML-like frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            elif val.lower() == "null":
                val = None
            elif val.lower() in ("true", "false"):
                val = val.lower() == "true"
            fm[key.strip()] = val
    return fm, parts[2].strip()


def get_mtime(path):
    if path.exists():
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return None


def scan_hypotheses():
    hyp_dir = ROOT / "hypotheses"
    if not hyp_dir.exists():
        return []
    results = []
    for f in sorted(hyp_dir.glob("H*.md")):
        fm, body = parse_frontmatter(f)
        if not fm.get("id"):
            continue
        claim = ""
        kills_it = ""
        for section in body.split("##"):
            s = section.strip()
            if s.startswith("Claim"):
                claim = s.replace("Claim", "").strip().split("\n")[0]
            elif s.startswith("Kills it"):
                kills_it = s.replace("Kills it", "").strip().split("\n")[0]
        results.append({
            "id": fm.get("id"), "title": fm.get("title", ""),
            "status": fm.get("status", "conjecture"), "parent": fm.get("parent"),
            "children": fm.get("children", []), "claim": claim,
            "kills_it": kills_it, "file": str(f.relative_to(ROOT)),
        })
    return results


def scan_insights():
    ins_dir = ROOT / "insights"
    if not ins_dir.exists():
        return []
    results = []
    for f in sorted(ins_dir.glob("2*.md")):
        fm, body = parse_frontmatter(f)
        if not fm.get("date"):
            continue
        finding = ""
        for section in body.split("##"):
            if section.strip().startswith("Finding"):
                finding = section.strip().replace("Finding", "").strip().split("\n")[0]
        results.append({
            "date": fm.get("date"), "title": fm.get("title", ""),
            "updates": fm.get("updates", ""), "result": fm.get("result", ""),
            "script": fm.get("script", ""), "figure": fm.get("figure", ""),
            "finding": finding, "file": str(f.relative_to(ROOT)),
        })
    return sorted(results, key=lambda x: x["date"], reverse=True)


def scan_decisions():
    idx = ROOT / "decisions" / "INDEX.md"
    if not idx.exists():
        return []
    results = []
    for line in idx.read_text().split("\n"):
        if line.startswith("|") and "---" not in line and "ID" not in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 4:
                results.append({"id": cols[0], "decision": cols[1], "date": cols[2], "rationale": cols[3]})
    return results


def scan_pipeline():
    results = []
    for entry in PIPELINE_SCRIPTS:
        script_path = ROOT / entry["script"]
        script_mtime = get_mtime(script_path)
        outputs = []
        all_fresh = True
        for out in entry["outputs"]:
            out_path = ROOT / out
            out_mtime = get_mtime(out_path)
            fresh = True
            if script_path.exists() and out_path.exists():
                fresh = out_path.stat().st_mtime >= script_path.stat().st_mtime
            elif not out_path.exists():
                fresh = False
            if not fresh:
                all_fresh = False
            outputs.append({"path": out, "exists": out_path.exists(), "mtime": out_mtime, "fresh": fresh})
        results.append({
            "script": entry["script"], "name": entry["name"], "level": entry["level"],
            "exists": script_path.exists(), "script_mtime": script_mtime,
            "outputs": outputs, "all_fresh": all_fresh,
        })
    return results


def scan_figures():
    fig_dir = ROOT / "output" / "figures"
    if not fig_dir.exists():
        return []
    results = []
    for f in sorted(fig_dir.glob("*.png")):
        stem = f.stem
        script = FIGURE_SCRIPT_MAP.get(stem)
        script_path = ROOT / script if script else None
        fresh = None
        if script_path and script_path.exists():
            fresh = f.stat().st_mtime >= script_path.stat().st_mtime
        results.append({
            "name": stem, "path": str(f.relative_to(ROOT)), "mtime": get_mtime(f),
            "script": script, "fresh": fresh, "orphaned": script is None,
        })
    return results


if __name__ == "__main__":
    print("Scanning project...")
    hypotheses = scan_hypotheses()
    insights = scan_insights()
    decisions = scan_decisions()
    pipeline = scan_pipeline()
    figures = scan_figures()

    status_counts = {}
    for h in hypotheses:
        s = h["status"]
        status_counts[s] = status_counts.get(s, 0) + 1

    data = {
        "summary": {
            "hypothesis_counts": status_counts,
            "total_hypotheses": len(hypotheses),
            "total_insights": len(insights),
            "pipeline_stale": sum(1 for p in pipeline if not p["all_fresh"]),
            "pipeline_total": len(pipeline),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "hypotheses": hypotheses,
        "insights": insights,
        "decisions": decisions,
        "pipeline": pipeline,
        "figures": figures,
    }

    OUT.write_text(json.dumps(data, indent=2, default=str))
    print(f"  Hypotheses: {len(hypotheses)}")
    print(f"  Insights: {len(insights)}")
    print(f"  Decisions: {len(decisions)}")
    print(f"  Pipeline: {len(pipeline)} scripts")
    print(f"  Figures: {len(figures)}")
    print(f"\nWritten: {OUT}")
