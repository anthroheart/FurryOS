#!/usr/bin/env python

from pathlib import Path
import yaml
import json
from datetime import datetime
from rich import print

# ------------------------------------------------------------
# Project paths (project root = current working directory)
# ------------------------------------------------------------
ROOT = Path.cwd()
GENOME_FILE = ROOT / "GENOME.yaml"

GENERATED_DIR = ROOT / "_generated"
LOG_DIR = GENERATED_DIR / "logs"
SPEC_DIR = GENERATED_DIR / "specs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
SPEC_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().isoformat(timespec="seconds")
LOG_FILE = LOG_DIR / f"build-plan-{timestamp}.log"
PLAN_FILE = SPEC_DIR / "build-plan.json"


def log(message: str):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


# ------------------------------------------------------------
# Load GENOME.yaml
# ------------------------------------------------------------
log("[bold green]Generating build plan from GENOME.yaml[/bold green]")

if not GENOME_FILE.exists():
    log("[bold red]ERROR: GENOME.yaml not found in project root[/bold red]")
    raise SystemExit(1)

with open(GENOME_FILE, "r", encoding="utf-8") as f:
    genome = yaml.safe_load(f)

log("[green]GENOME.yaml loaded successfully[/green]")


# ------------------------------------------------------------
# Resolve assets
# ------------------------------------------------------------
assets_section = genome.get("assets", {})
assets_root = assets_section.get("root")

resolved_assets = {}

if assets_root:
    assets_root_path = ROOT / assets_root
    resolved_assets["root"] = str(assets_root)

    for key, rel_path in assets_section.items():
        if key == "root":
            continue
        abs_path = assets_root_path / rel_path
        resolved_assets[key] = {
            "relative": rel_path,
            "absolute": str(abs_path),
            "exists": abs_path.exists()
        }

    log(f"[green]Assets root:[/green] {assets_root}")
else:
    log("[yellow]No assets.root defined[/yellow]")


# ------------------------------------------------------------
# Software model
# ------------------------------------------------------------
software = genome.get("software", {})
base_packages = software.get("base", {}).get("packages", [])
optional_bundles = software.get("optional_bundles", {})

log(f"[green]Base packages:[/green] {len(base_packages)}")
log(f"[green]Optional bundles:[/green] {list(optional_bundles.keys())}")


# ------------------------------------------------------------
# Modes and themes
# ------------------------------------------------------------
modes = genome.get("modes", {})
themes = genome.get("themes", {})

log(f"[green]Modes detected:[/green] {list(modes.keys())}")


# ------------------------------------------------------------
# Build section
# ------------------------------------------------------------
build_section = genome.get("build", {})


# ------------------------------------------------------------
# Construct build plan
# ------------------------------------------------------------
build_plan = {
    "meta": {
        "generated_at": timestamp,
        "generator": "generate_build_plan.py",
        "genome_file": "GENOME.yaml",
        "notes": "This is a dry-run plan. No actions were performed."
    },
    "system": {
        "name": genome.get("identity", {}).get("system_name", "Unknown"),
        "generation": genome.get("identity", {}).get("generation", "Unknown"),
        "base_distribution": genome.get("taxonomy", {}).get("phylum", {}).get("base_distribution", "Unknown"),
    },
    "assets": resolved_assets,
    "software": {
        "base_packages": base_packages,
        "optional_bundles": optional_bundles
    },
    "modes": modes,
    "themes": themes,
    "build": build_section
}


# ------------------------------------------------------------
# Write build plan
# ------------------------------------------------------------
with open(PLAN_FILE, "w", encoding="utf-8") as f:
    json.dump(build_plan, f, indent=2)

log("[bold green]Build plan generated successfully[/bold green]")
log(f"[green]Plan written to:[/green] {PLAN_FILE}")
log("[bold green]Build-plan generation complete[/bold green]")
