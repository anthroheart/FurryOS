# FurryOS Gen2 Builder (FurryOS_Gen2_Builder_GUI.py)

FurryOS Gen2 Builder is a toolchain for creating a customized Debian Live ISO themed for FurryOS (anthro-focused desktop experience). Drop in your own wallpapers, sounds, docs, and desktop scripts, then build a bootable ISO.

It uses GENOME.yaml as the config file for compiling/building your own custom OS.

> This repo is the **builder/template**, not the finished ISO. You add assets locally, then build your own image.

## FurryOS Gen2. Payload Assets (1.1GB):

https://furry-os.org/assets/FurryOS_Gen2.1_Assets_Payload.zip
https://furry-os.org/assets/FurryOS_Gen2.1_Assets_Payload.zip.sha256

3187d5e2e529f02e8c4ce1152c2c450c8601788f23665ef49fd8bcd1f0668534  FurryOS_Gen2.1_Assets_Payload.zip

## FurryOS Gen2 ISO (4.7GB):

https://furry-os.org/assets/furryos-gen2.1-amd64.iso
https://furry-os.org/assets/furryos-gen2.1-amd64.iso.sha256

b1e4b5301d14ca6b66209a6c7668bc4551a45d803661149429b8e5f2444efae6  furryos-gen2.1-amd64.iso

Debian 13/MATE Live ISO (4.0GB)

## TODO:

Plymouth hiccupped when building with temporary unable to connect to debian servers. So no custom splash image set, though the file is there in splash.png
No startup sound plays (or may playing through my microphone) even though sounds/startup/startup.ogg and haven't tested if sounds/shutdown/shutdown.ogg works.
Check icons on Desktop and fix their links to work.

GENOME.yaml is 760 Lines long, so I couldn't handle everything. Think of it as a guide or model to grow from.

## GitHub:

https://github.com/anthroheart/FurryOS

---

## Requirements

- Debian or Debian-based system (tested on Bookworm/Trixie)
- 10-20 GB free disk space for build workspace
- Internet access to download the base Debian Live ISO
- Packages: `python3`, `python3-venv`, `python3-yaml`, `squashfs-tools`, `xorriso`, `curl` or `wget`, `xterm` or another `x-terminal-emulator`

Install typical dependencies:

    sudo apt update
    sudo apt install -y python3 python3-venv python3-yaml squashfs-tools xorriso curl xterm

**Organization:** Anthro Entertainment LLC
**License:** MIT (code), proprietary (FurryOS branding/assets)

For more information, visit: https://furry-os.org | https://anthroentertainment.com
