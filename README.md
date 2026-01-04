# FurryOS Gen2 Builder

FurryOS Gen2 Builder is a toolchain for creating a customized Debian Live ISO themed for FurryOS (anthro-focused desktop experience). Drop in your own wallpapers, sounds, docs, and desktop scripts, then build a bootable ISO.

> This repo is the **builder/template**, not the finished ISO. You add assets locally, then build your own image.

---

## Requirements

- Debian or Debian-based system (tested on Bookworm/Trixie)
- 10-20 GB free disk space for build workspace
- Internet access to download the base Debian Live ISO
- Packages: `python3`, `python3-venv`, `python3-yaml`, `squashfs-tools`, `xorriso`, `curl` or `wget`, `xterm` or another `x-terminal-emulator`

Install typical dependencies:

    sudo apt update
    sudo apt install -y python3 python3-venv python3-yaml squashfs-tools xorriso curl xterm

---

## Repository Layout

    FurryOS-Gen2/
    ├── FurryOS_Builder.py           # GUI launcher
    ├── build_furryos.sh             # Main build script (runs all phases)
    ├── prepare_iso_workspace.sh     # ISO extraction helper (called by build script)
    ├── GENOME.yaml                  # Build configuration (paths, identity, assets)
    ├── generate_build_plan.py       # Internal helper (JSON build plan)
    ├── validate_genome.py           # Validates GENOME.yaml
    ├── payload/
    │   └── assets/
    │       ├── desktop/             # Desktop items & installer
    │       ├── wallpapers/          # Background images
    │       ├── splash/              # Boot splash artwork
    │       ├── sounds/              # System/startup sounds
    │       ├── music/               # Optional music content
    │       ├── docs/                # Documentation (PDF/TXT)
    │       └── images/              # Extra images, icons, logos
    ├── LICENSE
    └── README.md

`_generated/` (build workspace and final ISO) is **created at build time** and should not be committed to Git.

---

## Quick Start

### 1. Clone the repo

    git clone https://github.com/YourUsername/FurryOS-Gen2.git
    cd FurryOS-Gen2

### 2. Run the GUI

    python3 FurryOS_Builder.py

### 3. Copy your assets

Using the GUI:

- Open the **Asset Folders** or **Quick Start** tab
- Use the "Open Asset Folders" buttons to open directories
- Copy files into these locations:

  payload/assets/desktop/
  README.txt
  FurryOS-Installer.sh
  FurryOS-Installer.desktop
  install-desktop-scripts.sh
  icons/furryos-installer.png # 128x128 PNG

  payload/assets/wallpapers/
  default.jpg # Main wallpaper (1920x1080+)

  payload/assets/splash/
  splash.png # Boot splash image (1920x1080)

  payload/assets/sounds/
  startup.ogg # Short login sound (OGG format)

  payload/assets/music/
  _.ogg / _.mp3 # Optional music tracks

  payload/assets/docs/
  _.pdf, _.txt # Guides, readmes

  payload/assets/images/
  (logos, extra artwork, etc.)

### 4. Build the ISO

**Easiest method (recommended):**

- In **Quick Start** tab, click **"Build FurryOS ISO"**
- A terminal window opens and runs `build_furryos.sh` with `sudo`
- First run:
  - Downloads the base Debian Live ISO (if not already present)
  - Extracts it into `_generated/work/`
- Every run:
  - Validates `GENOME.yaml`
  - Copies your assets into the live filesystem
  - Installs desktop scripts and defaults
  - Rebuilds the squashfs and creates a new ISO

**Command-line equivalent:**

    cd /path/to/FurryOS-Gen2
    sudo ./build_furryos.sh

### 5. Find the finished ISO

After a successful build:

    _generated/iso/FurryOS-Gen2-amd64.iso
    _generated/iso/FurryOS-Gen2-amd64.iso.sha256
    _generated/specs/FurryOS-Gen2-PROVENANCE.txt

Use this ISO with a VM (GNOME Boxes, VirtualBox, etc.) or write it to USB.

---

## Customization via GENOME.yaml

`GENOME.yaml` defines:

- Distribution identity (name, generation, branding)
- Where assets live under `payload/assets`
- Which wallpaper/splash/sound to use as defaults
- Optional metadata such as author, license, and URLs

You can edit it manually or use the GUI's **"Edit GENOME.yaml"** button, then rebuild.

---

## Desktop Experience in the Live ISO

On first boot of the FurryOS Gen2 ISO, you should see:

- FurryOS wallpaper and theme as defined by your assets
- A **"Install FurryOS Gen2"** desktop icon using your custom icon file
- `README.txt` on the desktop (if provided)
- Optional sounds, docs, and music embedded into the live system

If any of these are missing, verify:

- The files are present under `payload/assets/…`
- Paths in `GENOME.yaml` match those locations
- Phase 6 output during `build_furryos.sh` shows asset copying without errors

---

## What Not to Commit

To keep the repository lightweight:

- Do **not** commit:
  - `_generated/` directory
  - ISO images (`*.iso`, `*.img`)
  - Large music packs and bulk media
- Optionally include **one small example** of wallpaper, splash, and sound; instruct users to replace them with their own content

Example `.gitignore` fragment:

    # Build workspace and outputs
    _generated/
    generated/
    *.iso
    *.img
    *.sha256
    *.log

    # Python cache
    __pycache__/
    *.pyc
    *.pyo

If you want to ship example media, keep them small and clearly labeled as samples.

---

## Build Time

- **First build:** ~15-25 minutes (downloads + extracts Debian ISO)
- **Subsequent builds:** ~10-15 minutes (reuses extracted filesystem)

---

## Troubleshooting

### Build fails with "ISO not found"

- Ensure you have internet access
- The script will auto-download Debian Live ISO if not present
- Or manually place `debian_live.iso` in project root

### Assets don't appear in the ISO

1. Check files exist in `payload/assets/`
2. Watch Phase 6 output during build
3. Verify paths in `GENOME.yaml` match your file locations

### Permission errors

- Make sure you run with `sudo`: `sudo ./build_furryos.sh`
- If you get "ISO already mounted" errors:

  sudo umount \_generated/work/iso-mount
  sudo rm -rf \_generated
  sudo ./build_furryos.sh

---

## License and Attribution

- Code and scripts in this builder: See `LICENSE` file
- FurryOS branding, artwork, and AnthroHeart Universe content remain the property of **Anthro Teacher / Anthro Entertainment LLC**
- Users must provide their own wallpapers, music, and media when building custom ISOs
- Do not redistribute proprietary assets without permission

---

## Credits

**Created by:** Anthro Teacher
**Organization:** Anthro Entertainment LLC
**License:** MIT (code), proprietary (FurryOS branding/assets)

For more information, visit: https://furry-os.org | https://anthroentertainment.com
