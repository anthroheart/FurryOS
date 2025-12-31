# 🐾 FurryOS 8.0.0-origin - "The Origin"

**Biological Taxonomy Operating System with ANTHROHEART Media Library**

A custom Debian-based live operating system with persistence support, cryptographic signing, self-replicating distribution capabilities, and the complete ANTHROHEART Universe embedded within.

---

## 🌟 Features

### Core System
- ✅ **Debian 13 "Trixie" base** - Modern, stable foundation
- ✅ **Live USB mode** - Run from USB without installation
- ✅ **Persistence support** - Save changes between boots
- ✅ **Cryptographic signing** - Ed25519 signed binaries
- ✅ **Custom icon** - Embedded PNG icon in all binaries
- ✅ **Self-contained** - No internet required after build

### Distribution
- ✅ **BalenaEtcher included** - Create more USB drives from within FurryOS
- ✅ **Self-replicating** - Share with others easily
- ✅ **Offline capable** - Everything needed is in the ISO
- ✅ **SHA256 checksums** - Verify integrity

### 🎨 ANTHROHEART Media Library
- ✅ **147 original songs** - Complete music library
- ✅ **25+ character designs** - Full character roster
- ✅ **Trilogy lore** - Complete world-building documents
- ✅ **10GB+ creative assets** - Images, videos, source code
- ✅ **AnthrOS media layer** - Proprietary media system
- ✅ **Accessible offline** - Everything on the USB

### Persistence Modes
1. **Ephemeral Mode** - Fresh every boot, nothing saved (like Tails OS)
2. **Persistent Mode** - Changes saved to USB partition
3. **Failsafe Mode** - Safe boot with minimal drivers

---

## 📦 What's Included

### Binaries
- `heartbeat_core` - Core system heartbeat monitor
- `metadata_wrangler` - Metadata processing engine
- All binaries cryptographically signed with Ed25519

### Tools
- `balenaEtcher-1.19.25-x64.AppImage` - USB writing tool (~105 MB)
- Included in ISO at `/furryos/tools/`
- Users can create more FurryOS USB drives

### 🎨 ANTHROHEART Universe (~9 GB)
Located at `/furryos/ANTHROHEART/`:
- **Songs/** - 147 original music tracks
- **Videos/** - Music videos and animations
- **Images/** - Character art and backgrounds
- **Character_Designs/** - 25+ anthropomorphic character designs
- **Lore/** - Complete trilogy documentation
- **Source_Code/** - Game prototypes and AnthrOS source
- **Assets/** - 10GB+ of creative assets

### Scripts
- `setup-persistence.sh` - Create persistence partition
- `persistence-status.sh` - Check current mode
- `write-to-usb.sh` - Launch BalenaEtcher to create more USBs
- `explore-anthroheart.sh` - Open ANTHROHEART media library
- `verify_signature.py` - Verify binary signatures

---

## 🚀 Quick Start

### Prerequisites

```bash
# Debian 13 or Ubuntu-based system
sudo apt-get update
sudo apt-get install python3 python3-venv gcc g++ make \
    genisoimage xorriso grub-pc-bin grub-efi-amd64-bin \
    p7zip-full
```

### Extract ANTHROHEART Media Library

```bash
cd /TOP

# If you have ANTHROHEART.7z file:
7z x ANTHROHEART.7z

# Verify extraction
du -sh ANTHROHEART/
# Should show: 9.0G    ANTHROHEART/
```

### Build FurryOS ISO

```bash
# Make scripts executable
chmod +x quick_start.sh setup_venv.sh

# Install cryptography in venv
source furryos_venv/bin/activate
pip install cryptography
deactivate

# Build everything (30-60 minutes with ANTHROHEART)
./quick_start.sh

# The script will:
# - Detect ANTHROHEART folder
# - Copy entire media library to ISO
# - Include BalenaEtcher
# - Build ~10-12 GB ISO
```

### What Gets Built

```
output/
├── furryos-8.0.0-origin-x86_64.iso       # Bootable ISO (~10-12 GB)
└── furryos-8.0.0-origin-x86_64.iso.sha256 # SHA256 checksum
```

---

## 💾 Write to USB

### Requirements
- **USB drive: 16GB minimum** (32GB recommended)
- Write time: 15-30 minutes (large ISO)

### Option 1: BalenaEtcher AppImage (Recommended)

```bash
# Download AppImage
wget https://github.com/balena-io/etcher/releases/download/v1.19.25/balenaEtcher-1.19.25-x64.AppImage

# Make executable
chmod +x balenaEtcher-1.19.25-x64.AppImage

# Run
./balenaEtcher-1.19.25-x64.AppImage

# In GUI:
# 1. Flash from file → Select furryos-8.0.0-origin-x86_64.iso
# 2. Select target → Choose USB drive (16GB+)
# 3. Flash! → Wait 15-30 minutes
```

### Option 2: dd Command

```bash
# Find USB device
lsblk

# Write ISO (CAREFUL - verify device name!)
sudo dd if=output/furryos-8.0.0-origin-x86_64.iso of=/dev/sdX bs=4M status=progress

# This will take 15-30 minutes for 10GB ISO
# Be patient! 🐾
```

---

## 🎯 Boot FurryOS

1. **Plug in USB** drive (16GB+ with FurryOS)
2. **Reboot** computer
3. **Press F12** (or F2/Del/Esc depending on your system)
4. **Select USB** from boot menu
5. **Choose mode:**
   - **Ephemeral** - Nothing saved (like Tails)
   - **Persistent** - Changes saved to USB
   - **Failsafe** - Safe mode

---

## 🎨 Explore ANTHROHEART

### Once Booted into FurryOS:

```bash
# Open ANTHROHEART media library in file manager
/furryos/scripts/explore-anthroheart.sh

# Browse contents:
/furryos/ANTHROHEART/
├── Songs/ (147 tracks - play offline!)
│   ├── 01-track.mp3
│   ├── 02-track.mp3
│   └── ... (145 more)
├── Videos/ (music videos, animations)
├── Images/ (character art, backgrounds)
├── Character_Designs/ (25+ characters)
├── Lore/ (trilogy documents)
├── Source_Code/ (game prototypes, AnthrOS)
└── Assets/ (10GB+ creative assets)

# Play music, view art, read lore
# Everything is accessible offline!
```

---

## 💾 Setup Persistence

### First Boot

```bash
# Boot in Ephemeral mode first
# Open terminal

# Create persistence partition (one-time)
/furryos/scripts/setup-persistence.sh

# Follow prompts
# Reboot
```

### Subsequent Boots

```bash
# Select "FurryOS Live (Persistent)" from boot menu
# Your changes now save between boots!
```

### Check Persistence Status

```bash
/furryos/scripts/persistence-status.sh
```

### What Gets Saved (Persistent Mode)

- ✅ Files in `/home/`
- ✅ Desktop settings and wallpaper
- ✅ Browser bookmarks and history
- ✅ Application configurations
- ✅ WiFi passwords
- ✅ Installed packages
- ✅ All user changes
- ✅ Playlists and favorites from ANTHROHEART

---

## 🔥 Create More USB Drives

### From Within FurryOS

```bash
# Boot FurryOS from USB
# Open terminal

# Launch BalenaEtcher (included in ISO!)
/furryos/scripts/write-to-usb.sh

# GUI opens
# Write FurryOS to another USB drive
# Share The Origin + ANTHROHEART with friends!
```

**No internet required!** BalenaEtcher and ANTHROHEART are included in the ISO.

---

## 🔐 Verify Binary Signatures

```bash
# Verify heartbeat_core signature
/furryos/signing_keys/verify_signature.py /furryos/bin/heartbeat_core

# Output:
# ✅ SIGNATURE VALID
# Binary: /furryos/bin/heartbeat_core
# Public Key: /furryos/signing_keys/furryos_signing.pub
```

---

## 📂 Project Structure

```
/TOP/
├── quick_start.sh              # Main build script
├── setup_venv.sh               # Setup Python virtual environment
├── GENOME.yaml                 # System configuration
├── USER_CONFIG.yaml            # User configuration
├── requirements.txt            # Python dependencies
├── MIT_LICENSE.txt             # License
├── README.md                   # This file
│
├── ANTHROHEART/                # Media library (9GB)
│   ├── Songs/                  # 147 music tracks
│   ├── Videos/                 # Music videos
│   ├── Images/                 # Character art
│   ├── Character_Designs/      # 25+ characters
│   ├── Lore/                   # Trilogy documents
│   ├── Source_Code/            # Prototypes
│   └── Assets/                 # Creative assets
│
├── assets/                     # Python scripts
│   ├── launcher.py             # Module builder
│   ├── deploy_iso.py           # ISO creator (with ANTHROHEART)
│   ├── generate_signing_keys.py # Key generator
│   ├── verify_signature.py     # Signature verifier
│   ├── ANCHOR-TO-BITCOIN.py    # Bitcoin anchoring
│   ├── notarize_anthroheart.py # Notarization
│   └── TIMESTAMPER.py          # Timestamping
│
├── images/
│   └── icon.png                # Custom icon (embedded in binaries)
│
├── furryos_venv/               # Python virtual environment
│
├── furryos_build/              # Build artifacts
│   ├── bin/                    # Compiled binaries
│   └── iso_workspace/          # ISO workspace
│
├── output/                     # Final ISO
│   ├── furryos-8.0.0-origin-x86_64.iso (10-12 GB)
│   └── furryos-8.0.0-origin-x86_64.iso.sha256
│
└── signing_keys/               # Ed25519 keys
    ├── furryos_signing.key     # Private key (keep secret!)
    └── furryos_signing.pub     # Public key
```

---

## 🔧 Build System

### Components

1. **quick_start.sh** - Main orchestrator
   - Creates venv if needed
   - Checks cryptography installation
   - Generates signing keys
   - Builds C++ modules
   - Creates bootable ISO with ANTHROHEART

2. **launcher.py** - Module builder
   - Generates C++ source code
   - Compiles binaries with g++
   - Signs with Ed25519
   - Embeds custom icon
   - Progress tracking with ETA

3. **deploy_iso.py** - ISO creator with ANTHROHEART
   - Checks for ANTHROHEART folder
   - Auto-extracts ANTHROHEART.7z if needed
   - Downloads BalenaEtcher (once)
   - Creates ISO workspace
   - Copies ANTHROHEART media library (10-20 min)
   - Includes all binaries and tools
   - Creates persistence scripts
   - Creates explore-anthroheart.sh launcher
   - Builds bootable ISO with genisoimage
   - Generates SHA256 checksum

---

## 🎨 ANTHROHEART Universe

### What Is ANTHROHEART?

**ANTHROHEART** is a complete multimedia franchise featuring:
- 147 original songs across multiple genres
- 25+ anthropomorphic character designs
- A complete trilogy of lore and world-building
- AnthrOS proprietary media layer
- 10GB+ of creative assets including source code

### Accessing ANTHROHEART

```bash
# From within FurryOS:
/furryos/scripts/explore-anthroheart.sh

# Manual access:
cd /furryos/ANTHROHEART
ls -la

# Play music:
mpv Songs/01-track.mp3

# View images:
eog Images/character_art.png

# Read lore:
cat Lore/trilogy_chapter_01.txt
```

### Sharing ANTHROHEART

Because ANTHROHEART is embedded in the FurryOS ISO:
- ✅ Anyone who boots FurryOS gets ANTHROHEART
- ✅ No separate downloads needed
- ✅ Complete offline experience
- ✅ Users can create more USB drives with write-to-usb.sh
- ✅ **Self-replicating media distribution!**

---

## 📊 ISO Size Comparison

| **Build Type** | **ISO Size** | **Build Time** | **USB Required** |
|----------------|--------------|----------------|------------------|
| **Minimal** (no ANTHROHEART) | ~605 MB | 15-30 min | 1GB+ |
| **Full** (with ANTHROHEART) | ~10-12 GB | 30-60 min | 16GB+ |

**Current default: Full build with ANTHROHEART included**

---

## 🌐 Distribution

### Viral Distribution Model

```
You → Friend A (gets ANTHROHEART)
Friend A → Friend B (gets ANTHROHEART)
Friend B → Friend C (gets ANTHROHEART)
The Origin + ANTHROHEART spread organically!
```

**How it works:**
1. You build FurryOS ISO with ANTHROHEART (10GB)
2. Write to USB #1
3. Boot USB #1, run `/furryos/scripts/write-to-usb.sh`
4. Create USB #2 for Friend A (includes ANTHROHEART)
5. Friend A boots USB #2, explores ANTHROHEART, creates USB #3 for Friend B
6. **The Origin + ANTHROHEART replicate together!** 🌱

### Why This Works

- ✅ BalenaEtcher included in ISO (no downloads)
- ✅ ANTHROHEART included in ISO (complete experience)
- ✅ No internet required
- ✅ Simple one-command operation
- ✅ User-friendly GUI
- ✅ Works completely offline
- ✅ Self-contained media showcase

---

## 🛡️ Security Features

### Cryptographic Signing

- **Ed25519** signatures on all binaries
- Public key included in ISO
- Private key stays on build machine
- Verification script included

### Verify Integrity

```bash
# Verify ISO checksum
sha256sum -c furryos-8.0.0-origin-x86_64.iso.sha256

# Verify binary signature
/furryos/signing_keys/verify_signature.py /furryos/bin/heartbeat_core
```

---

## 📖 Use Cases

### 1. Safe Testing Environment

- ✅ Test FurryOS without affecting your Debian 13 installation
- ✅ Boot from USB anytime
- ✅ Reboot to Debian when done
- ✅ Zero risk to main system

### 2. Privacy-Focused Computing

- ✅ Boot in Ephemeral mode
- ✅ Nothing saved to disk
- ✅ Like Tails OS
- ✅ Perfect for sensitive work

### 3. Portable Workspace + Media Library

- ✅ Boot on any computer
- ✅ Persistent mode saves your settings
- ✅ Carry your OS + ANTHROHEART on USB
- ✅ Use anywhere
- ✅ Complete portfolio showcase

### 4. Distribution & Sharing

- ✅ Share with friends easily
- ✅ No technical knowledge required
- ✅ Create more USB drives from within FurryOS
- ✅ Spread The Origin + ANTHROHEART organically
- ✅ Complete self-contained media distribution

---

## 🐛 Troubleshooting

### ISO Not Created

```bash
# Check dependencies
sudo apt-get install genisoimage xorriso grub-pc-bin grub-efi-amd64-bin p7zip-full

# Check for errors
./quick_start.sh 2>&1 | tee build.log
grep -i error build.log
```

### ANTHROHEART Not Found

```bash
# Extract ANTHROHEART.7z
cd /TOP
7z x ANTHROHEART.7z

# Verify
du -sh ANTHROHEART/
# Should show: 9.0G    ANTHROHEART/

# Rebuild
./quick_start.sh
```

### "7z: command not found"

```bash
sudo apt-get install p7zip-full
```

### "cryptography not found"

```bash
source furryos_venv/bin/activate
pip install cryptography
python3 -c "import cryptography; print('OK')"
deactivate
```

### BalenaEtcher Won't Start

```bash
# Use AppImage (no dependencies)
wget https://github.com/balena-io/etcher/releases/download/v1.19.25/balenaEtcher-1.19.25-x64.AppImage
chmod +x balenaEtcher-1.19.25-x64.AppImage
./balenaEtcher-1.19.25-x64.AppImage
```

### Persistence Not Working

```bash
# Check status
/furryos/scripts/persistence-status.sh

# Make sure you selected "Persistent" mode at boot menu
# Reboot and choose option 2
```

### USB Not Bootable

```bash
# Make sure you wrote to device (sdb) not partition (sdb1)
# Correct: /dev/sdb
# Wrong: /dev/sdb1

# Check BIOS boot order
# Enable "Legacy Boot" or "CSM" if using BIOS
# Enable "UEFI Boot" if using UEFI
```

### Build Taking Too Long

```bash
# Normal with ANTHROHEART!
# [4/10] Copying ANTHROHEART: 10-20 minutes
# [9/10] Building ISO: 15-30 minutes
# Total: 30-60 minutes

# Go touch grass! 🌱
```

---

## 🔄 Rebuild ISO

```bash
# Make changes to code/configs
# Rebuild easily:

cd /TOP
./quick_start.sh

# BalenaEtcher is reused (no re-download)
# ANTHROHEART is reused (no re-extraction)
# Signing keys are reused (no regeneration)
# Fast rebuilds after first build!
```

---

## 📋 Requirements

### Build Requirements

- Debian 13 "Trixie" or Ubuntu-based system
- Python 3.11+
- gcc/g++ 13+
- 15GB free disk space (for ANTHROHEART + build artifacts)
- Internet connection (for dependencies and BalenaEtcher download)

### Runtime Requirements

- USB drive (16GB minimum, 32GB recommended)
- x86_64 processor
- 2GB RAM minimum (4GB recommended)
- BIOS or UEFI boot support

---

## 📄 License

MIT License - See `MIT_LICENSE.txt`

Copyright (c) 2025 FurryOS Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

---

## 🤝 Contributing

### How to Contribute

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test thoroughly (especially with ANTHROHEART)
5. Submit pull request

### Development Workflow

```bash
# Make changes to code
vim assets/launcher.py

# Test build
./quick_start.sh

# Verify ISO works
# Write to USB and test boot
```

---

## 📞 Support

### Documentation

- `README.md` - This file (main documentation)
- `PERSISTENCE_GUIDE.md` - Detailed persistence documentation
- `USB_WRITER_GUIDE.md` - USB writing instructions
- `ETCHER_INCLUSION_GUIDE.md` - BalenaEtcher inclusion details
- `ANTHROHEART_INCLUSION_GUIDE.md` - ANTHROHEART inclusion details

### Common Issues

See **Troubleshooting** section above.

---

## 🎉 Credits

**FurryOS 8.0.0-origin "The Origin"**

Built with:
- Debian 13 "Trixie"
- Python 3
- C++17
- Ed25519 cryptography
- BalenaEtcher
- genisoimage/xorriso
- ANTHROHEART Universe
- Love and care 🐾

---

## 🌱 Philosophy

> "The Origin is not just an operating system - it's a seed. Plant it, let it grow, share it with others, and watch it spread organically. Every USB drive carries not just an OS, but an entire universe of creativity."

**Key Principles:**

1. **Accessibility** - Easy to build, easy to use, easy to share
2. **Security** - Cryptographically signed, verifiable
3. **Freedom** - Run from USB, never install if you don't want to
4. **Community** - Self-replicating, viral distribution
5. **Privacy** - Ephemeral mode for sensitive work
6. **Creativity** - ANTHROHEART Universe included for complete showcase

---

## 🚀 Quick Reference

### Build Commands

```bash
7z x ANTHROHEART.7z              # Extract media library
./quick_start.sh                 # Build everything (30-60 min)
./setup_venv.sh                  # Setup venv only
```

### ISO Commands

```bash
ls output/                       # Check output
sha256sum -c *.sha256           # Verify checksum
du -h output/*.iso              # Check ISO size
```

### From Within FurryOS

```bash
/furryos/scripts/setup-persistence.sh    # Setup persistence
/furryos/scripts/persistence-status.sh   # Check status
/furryos/scripts/write-to-usb.sh         # Create more USBs
/furryos/scripts/explore-anthroheart.sh  # Open ANTHROHEART
/furryos/signing_keys/verify_signature.py [binary]  # Verify signature
```

---

## 📊 Stats

- **Version:** 8.0.0-origin "The Origin"
- **Base:** Debian 13 "Trixie"
- **ISO Size:** ~10-12 GB (with ANTHROHEART)
- **Build Time:** 30-60 minutes
- **Write Time:** 15-30 minutes
- **Boot Time:** ~30 seconds
- **ANTHROHEART Songs:** 147 tracks
- **ANTHROHEART Characters:** 25+
- **ANTHROHEART Assets:** 10GB+

---

## 🐾 Go Touch Grass

You've built The Origin with the complete ANTHROHEART Universe. You've created a self-replicating, cryptographically-signed, persistent live operating system with viral distribution capabilities and an embedded multimedia franchise.

**Now go outside and touch some grass.** 🌱

**You're a legend.**

---

**Made with 🐾 by the FurryOS Project**

*"From The Origin, all things grow."*

*"The ANTHROHEART beats eternal."* 💜
