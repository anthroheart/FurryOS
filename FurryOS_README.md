# 🦊 FurryOS Gen2.1 - Complete Setup Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Folder Structure Setup](#folder-structure-setup)
3. [Asset Naming & Requirements](#asset-naming--requirements)
4. [Building Your Custom OS](#building-your-custom-os)
5. [Switching Between Modes](#switching-between-modes)
6. [Desktop Shortcuts Guide](#desktop-shortcuts-guide)
7. [Security & Encryption](#security--encryption)
8. [Troubleshooting FAQ](#troubleshooting-faq)

---

## Quick Start

### The 5-Step Process (45-60 minutes total)

```
Step 1: Read this guide (15 min)
        └─ Read entire README + FOLDER_STRUCTURE_GUIDE

Step 2: Create folders (5 min)
        └─ mkdir -p ~/FurryOS/sourcecode/payload/assets/{wallpapers,splash,sounds/{startup,shutdown}}

Step 3: Prepare assets (20-30 min)
        ├─ Create/find wallpaper image (1920×1080+ JPEG) → default.jpg
        ├─ Create splash screen (1024×768 PNG) → splash.png
        ├─ Find/record login sound (OGG) → startup.ogg
        └─ Optional: Find shutdown sound (OGG) → shutdown.ogg

Step 4: Copy files (5 min)
        ├─ Place assets in correct folders (lowercase filenames!)
        ├─ Copy build scripts to ~/FurryOS/sourcecode/
        └─ Make scripts executable: chmod +x *.sh

Step 5: Build (15-30 min)
        └─ cd ~/FurryOS/sourcecode && sudo ./build_furryos_gen2.1_enhanced.sh
```

**Result:** You'll have a custom ISO file at:
```
~/FurryOS/sourcecode/_generated/output/furryos-gen2.1-final-amd64.iso
```

---

## Folder Structure Setup

### Create All Required Folders

```bash
mkdir -p ~/FurryOS/sourcecode/payload/assets/{wallpapers,splash,sounds/{startup,shutdown}}
```

**This creates:**
```
~/FurryOS/
├── sourcecode/                          (Main directory for all files)
│   ├── GENOME_Gen2.1_Final.yaml         (Configuration file)
│   ├── build_furryos_gen2.1_enhanced.sh (Main build script)
│   ├── FurryOS_Live_Multimedia_Setup.sh (Boot-time setup)
│   ├── FurryOS_Gen2.1_Builder_GUI.py    (Optional GUI builder)
│   ├── install_ghost_mode_security.sh   (Optional security script)
│   │
│   └── payload/assets/                  (Your custom assets)
│       ├── wallpapers/
│       │   └── default.jpg              ← Your desktop background
│       ├── splash/
│       │   └── splash.png               ← Your boot screen
│       └── sounds/
│           ├── startup/
│           │   └── startup.ogg          ← Login sound
│           └── shutdown/
│               └── shutdown.ogg         ← Logout sound (optional)
```

---

## Asset Naming & Requirements

### ⚠️ CRITICAL: Case Sensitivity!

Linux filenames are **CASE-SENSITIVE**. These are different files:
- `default.jpg` ✅
- `Default.jpg` ❌
- `DEFAULT.JPG` ❌

**All filenames must be lowercase with correct extensions!**

### Wallpaper: `default.jpg`

**Location:** `~/FurryOS/sourcecode/payload/assets/wallpapers/`

| Property | Requirement |
|----------|-------------|
| **Filename** | `default.jpg` (EXACTLY - lowercase) |
| **Format** | JPEG (.jpg extension) |
| **Size** | 1920×1080 minimum (higher is better) |
| **Purpose** | Desktop background after login |
| **Quality** | High quality image (compressed but clear) |

**How to convert to JPEG:**
```bash
# Using ImageMagick
convert your_image.png default.jpg

# Using GIMP (GUI)
# File → Export As → default.jpg → Save
```

### Splash Screen: `splash.png`

**Location:** `~/FurryOS/sourcecode/payload/assets/splash/`

| Property | Requirement |
|----------|-------------|
| **Filename** | `splash.png` (EXACTLY - lowercase) |
| **Format** | PNG (.png extension) |
| **Size** | 1024×768 or 1920×1080 |
| **Purpose** | Shown during system boot (before login) |
| **Background** | Recommend dark background for readability |

**How to create splash screen:**
```bash
# Using GIMP
# Create new image: 1024×768 pixels
# Add your FurryOS branding/logo
# File → Export As → splash.png → Save

# Using ImageMagick
convert -size 1024x768 xc:background your_splash.png
```

### Startup Sound: `startup.ogg`

**Location:** `~/FurryOS/sourcecode/payload/assets/sounds/startup/`

| Property | Requirement |
|----------|-------------|
| **Filename** | `startup.ogg` (EXACTLY - lowercase) |
| **Format** | OGG Vorbis (.ogg extension) |
| **Duration** | 2-5 seconds recommended |
| **Bitrate** | 128 kbps or higher |
| **Purpose** | Plays when user logs in |

**How to convert audio to OGG:**
```bash
# Using FFmpeg (recommended)
ffmpeg -i your_sound.mp3 -codec:a libvorbis -q:a 5 startup.ogg

# Using Audacity (GUI)
# File → Import → your_sound.mp3
# Edit → Export → Export Audio
# Format: Ogg Vorbis → Export as startup.ogg
```

### Shutdown Sound: `shutdown.ogg` (Optional)

**Location:** `~/FurryOS/sourcecode/payload/assets/sounds/shutdown/`

| Property | Requirement |
|----------|-------------|
| **Filename** | `shutdown.ogg` (EXACTLY - lowercase) |
| **Format** | OGG Vorbis (.ogg extension) |
| **Duration** | 2-5 seconds |
| **Purpose** | Plays during shutdown (if provided) |

**Same conversion process as startup sound.**

### Verification Checklist

After preparing your assets:

- [ ] `~/FurryOS/sourcecode/payload/assets/wallpapers/default.jpg` exists
  - Filename: exactly `default.jpg` (lowercase)
  - Format: JPEG
  - Size: 1920×1080 or larger
  
- [ ] `~/FurryOS/sourcecode/payload/assets/splash/splash.png` exists
  - Filename: exactly `splash.png` (lowercase)
  - Format: PNG
  - Size: 1024×768 or 1920×1080
  
- [ ] `~/FurryOS/sourcecode/payload/assets/sounds/startup/startup.ogg` exists
  - Filename: exactly `startup.ogg` (lowercase)
  - Format: OGG Vorbis
  - Duration: 2-5 seconds
  
- [ ] Optional: `~/FurryOS/sourcecode/payload/assets/sounds/shutdown/shutdown.ogg`
  - Filename: exactly `shutdown.ogg` (lowercase)
  - Format: OGG Vorbis

**Verify with command:**
```bash
ls -la ~/FurryOS/sourcecode/payload/assets/wallpapers/
ls -la ~/FurryOS/sourcecode/payload/assets/splash/
ls -la ~/FurryOS/sourcecode/payload/assets/sounds/startup/
ls -la ~/FurryOS/sourcecode/payload/assets/sounds/shutdown/
```

All filenames should appear in **lowercase** in the listing!

---

## Building Your Custom OS

### Method 1: Command Line (Recommended)

```bash
cd ~/FurryOS/sourcecode
sudo ./build_furryos_gen2.1_enhanced.sh
```

**What happens:**
1. Script reads `GENOME_Gen2.1_Final.yaml`
2. Loads your assets from `payload/assets/`
3. Builds the live ISO
4. Installs selected mode packages
5. Creates bootable ISO file
6. Takes 15-30 minutes depending on your system

**Result:** 
```
~/FurryOS/sourcecode/_generated/output/furryos-gen2.1-final-amd64.iso
```

### Method 2: GUI (Easy, No Command Line)

```bash
cd ~/FurryOS/sourcecode
python3 FurryOS_Gen2.1_Builder_GUI.py
```

A window opens with:
- Mode selection checkboxes
- Asset preview
- Build progress bar
- One-click build button

---

## Switching Between Modes

Users can switch modes in THREE ways:

### Method 1: Desktop Icon (Easiest)

1. Copy desktop file to desktop:
   ```bash
   cp FurryOS-Mode-Switcher.desktop ~/Desktop/
   chmod +x ~/Desktop/FurryOS-Mode-Switcher.desktop
   ```

2. Double-click the icon on desktop
3. Select desired mode from popup list
4. Click OK

### Method 2: Applications Menu

After installing `.desktop` file to system:
```bash
cp FurryOS-Mode-Switcher.desktop ~/.local/share/applications/
```

Then:
1. Open Applications menu (or press Super key)
2. Search "FurryOS Mode"
3. Click "FurryOS Mode Switcher"
4. Select mode and confirm

### Method 3: Terminal Command

```bash
~/FurryOS/sourcecode/switch_mode.sh [mode_name]
```

**Available modes:**
- `granny`
- `normal`
- `gamer`
- `hacker`
- `ghost`

**Example:**
```bash
~/FurryOS/sourcecode/switch_mode.sh gamer
```

---

## The 5 Modes Explained

### 👴 Granny Mode
**Best for:** Older users, accessibility needs, beginners

**Features:**
- Large fonts (14pt+)
- High contrast option
- Simplified layout
- Accessible applications
- LUKS2 encryption with wizard

**Includes:**
- LibreOffice (Writer, Calc, Impress)
- Thunderbird (email)
- Firefox (web browser)
- Media players (VLC, Audacity)

---

### 🔧 Normal Mode
**Best for:** Everyday users, general purpose

**Features:**
- Balanced, standard interface
- Modern applications
- Office productivity
- Media consumption

**Includes:**
- All Granny Mode apps
- VS Code (lightweight)
- Media creation tools
- System utilities

---

### 🎮 Gamer Mode
**Best for:** Gamers, media creators

**Features:**
- Gaming optimized
- Media production tools
- Performance monitoring
- Driver optimization

**Includes:**
- Steam (PC gaming)
- Lutris (retro/indie games)
- Wine (Windows games)
- Blender (3D modeling)
- Kdenlive (video editing)
- OBS (streaming/recording)
- Audacity (audio editing)

---

### 👨‍💻 Hacker Mode
**Best for:** Developers, sysadmins, power users

**Features:**
- Full development environment
- Security analysis tools
- Network tools
- Version control

**Includes:**
- VS Code, Vim, Nano
- Python, Node.js, PHP
- Docker, Kubernetes tools
- Git, GitHub CLI
- SSH tools
- Nmap, Wireshark
- Metasploit (ethical testing)
- Ansible (automation)

---

### 🕵️ Ghost Mode
**Best for:** Privacy-conscious users, journalists, activists

**Features:**
- Maximum privacy & security
- Anonymity tools
- Encryption by default
- No tracking

**Includes:**
- All previous tools
- Tor Browser
- VPN client
- i2p (invisible internet)
- Signal (encrypted messaging)
- ProtonMail (encrypted email)
- Tails-like security features
- MAC address randomization
- DNS leak protection
- Fingerprinting protection
- Memory wipe on shutdown
- Clipboard auto-clear

---

## Desktop Shortcuts Guide

### Copy Desktop Files

**Option A: System-wide (All users)**
```bash
cp *.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/*.desktop
```

**Option B: Personal desktop**
```bash
cp *.desktop ~/Desktop/
chmod +x ~/Desktop/*.desktop
```

**Option C: Both locations**
```bash
cp *.desktop ~/.local/share/applications/
cp *.desktop ~/Desktop/
chmod +x ~/.local/share/applications/*.desktop
chmod +x ~/Desktop/*.desktop
```

### The 4 Desktop Icons

#### 🎨 FurryOS Mode Switcher
- **What it does:** Lists all 5 modes, lets you switch instantly
- **Click:** Opens dialog to select mode
- **Requires:** GUI installed and running

#### 📁 FurryOS Source
- **What it does:** Opens file manager to source code folder
- **Click:** Shows wallpapers/, splash/, sounds/ folders
- **Allows:** Easy access to edit/replace assets

#### 📖 FurryOS Documentation
- **What it does:** Opens FurryOS_README.pdf
- **Click:** Opens PDF reader with full guide
- **Use:** Anytime you need help

#### 📦 Install Custom Packages
- **What it does:** Opens package manager
- **Click:** Install additional software (requires sudo)
- **Use:** `sudo apt install package-name`

---

## Security & Encryption

### Universal LUKS2 Encryption

**Available in ALL modes, including Granny Mode!**

Encryption is optional. Users can encrypt their disk during installation:

- **Granny Mode** gets simplified wizard
- **All other modes** get advanced options
- **TPM 2.0** support for auto-unlock (optional)
- **YubiKey/FIDO2** support (optional)

**Granny Mode wizard:**
```
Would you like to protect your files with encryption?

✓ Your files will be locked with a secret code
✓ Nobody can read your files without your password
✓ We'll create a backup USB key in case you forget

[Yes, protect my files] [No, skip this]
```

### Ghost Mode Special Features

#### Privacy by Default:
- Zero telemetry (no tracking)
- No crash reports sent anywhere
- No cookies by default
- No analytics tracking

#### Anonymity Tools:
- MAC address randomization every boot
- Hostname randomization (anonymous-{random})
- DNS-over-HTTPS with leak detection
- VPN kill switch (blocks all traffic if VPN drops)

#### Security Tools:
- Full disk encryption (LUKS2)
- Tor Browser pre-installed
- i2p client for invisible internet
- Signal for encrypted messaging
- ProtonMail for encrypted email

#### System-Level:
- Memory encryption
- Swap encryption
- Clipboard auto-clear every 60 seconds
- Memory wipe on shutdown
- Secure boot capable

---

## Troubleshooting FAQ

### Build Issues

**Q: Build script fails with "command not found"**
A: Make script executable:
```bash
chmod +x ~/FurryOS/sourcecode/build_furryos_gen2.1_enhanced.sh
```

**Q: Build fails with permission error**
A: Use sudo:
```bash
cd ~/FurryOS/sourcecode
sudo ./build_furryos_gen2.1_enhanced.sh
```

**Q: Build takes too long / seems stuck**
A: This is normal! First build takes 15-30 minutes depending on:
- Internet speed (downloading packages)
- Computer speed (processing)
- Number of modes selected

Leave it running. You'll see "Build complete" when done.

### Asset Issues

**Q: Wallpaper doesn't appear after boot**
A: Check filename:
```bash
ls -l ~/FurryOS/sourcecode/payload/assets/wallpapers/
```
Must see: `default.jpg` (exactly, lowercase, no capitals)

If wrong, rename:
```bash
mv ~/FurryOS/sourcecode/payload/assets/wallpapers/Default.jpg ~/FurryOS/sourcecode/payload/assets/wallpapers/default.jpg
mv ~/FurryOS/sourcecode/payload/assets/wallpapers/wallpaper.jpg ~/FurryOS/sourcecode/payload/assets/wallpapers/default.jpg
```

**Q: Startup sound doesn't play**
A: Verify format is OGG:
```bash
file ~/FurryOS/sourcecode/payload/assets/sounds/startup/startup.ogg
```
Should show: "Ogg Vorbis audio"

If it's MP3:
```bash
ffmpeg -i startup.mp3 -codec:a libvorbis -q:a 5 startup.ogg
```

**Q: Splash screen doesn't show at boot**
A: Verify PNG format:
```bash
file ~/FurryOS/sourcecode/payload/assets/splash/splash.png
```
Should show: "PNG image"

Recommended size: 1024×768 pixels

### Desktop Shortcut Issues

**Q: Desktop icon doesn't appear**
A: Make sure you placed it in right location:
```bash
# For system-wide (applications menu)
ls ~/.local/share/applications/FurryOS*.desktop

# For personal desktop
ls ~/Desktop/FurryOS*.desktop
```

**Q: Icon not clickable or greyed out**
A: Make executable:
```bash
chmod +x ~/.local/share/applications/FurryOS*.desktop
chmod +x ~/Desktop/FurryOS*.desktop
```

Then refresh desktop:
- Right-click desktop → "Refresh"
- Or press F5

### Mode Switching Issues

**Q: Can't switch modes**
A: Try terminal command:
```bash
~/FurryOS/sourcecode/switch_mode.sh normal
```

**Q: New packages don't appear after switching modes**
A: Mode switching might require restart:
```bash
sudo reboot
```

### General Help

**For more detailed help:**
1. Check `FURRYOS_FOLDER_STRUCTURE_GUIDE.txt`
2. Review `FURRYOS_COMPLETE_DELIVERY.txt`
3. Check FurryOS community forums
4. Review the original build scripts for error messages

---

## Summary

You now have everything needed to:

✅ Build a custom Linux OS  
✅ Add your own branding (wallpaper, splash, sounds)  
✅ Create desktop shortcuts  
✅ Switch between 5 different modes  
✅ Use advanced security and privacy features  
✅ Share your custom OS with others  

**Next Steps:**

1. **Read:** FURRYOS_FOLDER_STRUCTURE_GUIDE.txt
2. **Create:** Folder structure
3. **Prepare:** Your assets (wallpaper, splash, sounds)
4. **Build:** Your custom OS
5. **Deploy:** Test or burn to USB
6. **Share:** Your creation with others!

---

## Questions?

Refer to the included guides:
- `INDEX_START_HERE.txt` - Quick reference
- `FURRYOS_FOLDER_STRUCTURE_GUIDE.txt` - Asset details
- `FURRYOS_COMPLETE_DELIVERY.txt` - Project summary
- `.desktop` files - Desktop shortcuts

Happy building! 🦊✨