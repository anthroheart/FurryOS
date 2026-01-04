#!/usr/bin/env python3

from pathlib import Path
import yaml
from rich import print
from datetime import datetime

ROOT = Path.cwd()
GENOME = ROOT / "GENOME.yaml"
LOG_DIR = ROOT / "_generated" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / f"validate-genome-{datetime.now().isoformat(timespec='seconds')}.log"

def log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("[bold green]Validating GENOME.yaml[/bold green]")

if not GENOME.exists():
    log("[bold red]ERROR: GENOME.yaml not found in project root[/bold red]")
    raise SystemExit(1)

with open(GENOME, "r", encoding="utf-8") as f:
    genome = yaml.safe_load(f)

required_top_keys = [
    "identity",
    "authority_hierarchy",
    "taxonomy",
    "assets",
    "software",
    "modes",
]

missing = [k for k in required_top_keys if k not in genome]

if missing:
    log(f"[bold red]Missing required sections: {missing}[/bold red]")
    raise SystemExit(1)

log("[bold green]GENOME.yaml structure OK[/bold green]")
log(f"Top-level keys: {list(genome.keys())}")

assets_root = genome.get("assets", {}).get("root")
if assets_root:
    assets_path = ROOT / assets_root
    if assets_path.exists():
        log(f"[green]Assets root exists:[/green] {assets_root}")
    else:
        log(f"[yellow]Assets root defined but not found:[/yellow] {assets_root}")

log("[bold green]Validation complete[/bold green]")
