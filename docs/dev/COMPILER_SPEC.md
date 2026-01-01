# FurryOS Compiler Specification

**Role:** The "Ribosome" (Builder Tool)
**Input:** `GENOME.yaml` + `USER_CONFIG.yaml`
**Output:** Bootable Hybrid ISO (Debian 13 Base)

## 1. The Core Logic Loop

The compiler should be a script (Python suggested, named `launcher.py`) that executes the following stages:

### Stage A: The Harvester (Parsing)

1.  Read `GENOME.yaml` to determine the **Phylum** (Debian Release) and **Kingdom** (Desktop/Server).
2.  Parse `pain_points`. Create a "Fix List" queue.
    - _Example:_ If `python_pep668` is present, queue a command to delete the `EXTERNALLY-MANAGED` flag in the chroot.

### Stage B: The Hydrator (Asset Gathering)

1.  Check for local kernel files in `/kernel/` (`vmlinuz`, `initrd.img`, `filesystem.squashfs`).
2.  **Fallback:** If missing, auto-download the Debian Live ISO defined in `build.base_iso.url`, mount it via loopback, and extract the 3 core files.
3.  Download the **AnthroHeart Asset Pack** if `optional: true` is set in the config.

### Stage C: The Alchemist (Compilation)

1.  **Genus Modules:** Iterate through `taxonomy.genus.modules`.
    - **Heartbeat (C++):** Compile `heartbeat.cpp` using `g++ -O3`.
    - **Vault (Bash):** Make executable and move to `/usr/local/bin/`.
2.  **Injection:** Copy these compiled binaries into the extracted `filesystem.squashfs` (unsquash -> copy -> resquash).

### Stage D: The Architect (ISO Mastering)

1.  Generate `grub.cfg` based on `installer.type` (Hybrid).
    - Entry 1: "Live Mode" (boots squashfs with persistence).
    - Entry 2: "Net Installer" (boots kernel only, triggers installer wizard).
2.  **Visuals:** Inject the `#FF6B35` border CSS into the MATE window manager config (`/home/user/.config/gtk-3.0/gtk.css`).
3.  **Mastering:** Use `xorriso` to build the final ISO with Hybrid MBR/EFI support.

## 2. Specific "Pain Point" Implementations

The Compiler must strictly enforce these rules during the build:

- **PEP 668 Fix:** `rm /usr/lib/python3.*/EXTERNALLY-MANAGED` inside the chroot.
- **Path Hygiene:** During asset copy, recursively rename any file with spaces to underscores (`_`). Fail the build if a path ends in a trailing slash.
- **NVIDIA Pain:** If `step2_hardware.proprietary_logic.nvidia` is triggered, inject `non-free-firmware` to `/etc/apt/sources.list`.

## 3. The "Experience Level" Logic

The Installer Wizard (Calamares or Custom) must read the `USER_CONFIG.yaml` at runtime:

- **IF Granny Mode:** Skip all UI pages. Auto-select `/dev/sda` (or largest disk), Auto-LUKS, Install.
- **IF Gamer Mode:** Show GPU driver checklist. Install Steam.
- **IF Ghost Mode:** Run a script to randomize MAC address (`macchanger -r`) before connecting to WiFi.

## 4. Directory Expectation

The Compiler should expect this structure:

```text
/workspace
  ├── GENOME.yaml
  ├── USER_CONFIG.yaml
  ├── modules/ (Source code for Heartbeat, etc.)
  ├── kernel/ (Local cache)
  └── output/ (Final ISO)
```
