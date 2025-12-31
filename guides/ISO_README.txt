================================================================================
                  FURRYOS 8.0.0-ORIGIN - "THE ORIGIN"
                    Biological Taxonomy Operating System
================================================================================

Welcome to FurryOS with ANTHROHEART Universe!

================================================================================
🎨 ANTHROHEART MEDIA LIBRARY INCLUDED 🎨
================================================================================

This USB contains the complete ANTHROHEART media library!

EXPLORE ANTHROHEART:
====================

Open terminal and run:
    /furryos/scripts/explore-anthroheart.sh

Or browse manually:
    cd /furryos/ANTHROHEART

ANTHROHEART Contents:
---------------------
• 147 original songs (various genres)
• 25+ anthropomorphic character designs
• Complete trilogy lore and world-building documents
• AnthrOS proprietary media layer
• 10GB+ of creative assets (images, videos, source code)
• Game prototypes and animations

All accessible offline!

================================================================================
INCLUDED TOOLS
================================================================================

🔥 BalenaEtcher USB Writer
--------------------------
Location: /furryos/tools/balenaEtcher-1.19.25-x64.AppImage
Launcher: /furryos/scripts/write-to-usb.sh

Use this to write FurryOS to more USB drives!
Share The Origin + ANTHROHEART with others!

================================================================================
PERSISTENCE MODES
================================================================================

This system supports multiple boot modes:

1. EPHEMERAL MODE (Default)
   • Fresh system every boot
   • Nothing saved to disk
   • Like Tails OS
   • Perfect for privacy

2. PERSISTENT MODE
   • Changes saved to USB between boots
   • Settings persist
   • Files kept
   • Personal workspace

3. FAILSAFE MODE
   • Safe boot with minimal drivers
   • For troubleshooting

================================================================================
SETUP PERSISTENCE
================================================================================

First Boot (Ephemeral Mode):
-----------------------------
1. Boot to FurryOS
2. Open terminal
3. Run: /furryos/scripts/setup-persistence.sh
4. Follow the prompts
5. Reboot

Subsequent Boots:
-----------------
Select "FurryOS Live (Persistent)" from boot menu

Your changes will now save between boots, including:
• Files in /home/
• Desktop settings
• Browser bookmarks
• WiFi passwords
• Installed packages
• ANTHROHEART playlists and favorites

================================================================================
AVAILABLE SCRIPTS
================================================================================

All scripts located in: /furryos/scripts/

setup-persistence.sh
--------------------
Creates a persistence partition on your USB drive.
Run once during first boot to enable persistent mode.

Usage:
    /furryos/scripts/setup-persistence.sh

persistence-status.sh
---------------------
Check if persistence is currently active.

Usage:
    /furryos/scripts/persistence-status.sh

write-to-usb.sh
---------------
Launch BalenaEtcher to create more FurryOS USB drives.
Share The Origin + ANTHROHEART with friends!

Usage:
    /furryos/scripts/write-to-usb.sh

explore-anthroheart.sh
----------------------
Open ANTHROHEART media library in file manager.
Browse songs, character art, lore, and assets.

Usage:
    /furryos/scripts/explore-anthroheart.sh

================================================================================
VERIFY BINARY SIGNATURES
================================================================================

All binaries are cryptographically signed with Ed25519.

Verify a binary:
    /furryos/signing_keys/verify_signature.py /furryos/bin/heartbeat_core

Expected output:
    ✅ SIGNATURE VALID
    Binary: /furryos/bin/heartbeat_core
    Public Key: /furryos/signing_keys/furryos_signing.pub

Public key included at: /furryos/signing_keys/furryos_signing.pub

================================================================================
WRITE TO ANOTHER USB DRIVE
================================================================================

You can create more FurryOS USB drives from within this live system!

Steps:
------
1. Boot FurryOS from this USB
2. Insert a second USB drive (16GB+ required)
3. Open terminal
4. Run: /furryos/scripts/write-to-usb.sh
5. BalenaEtcher GUI will open
6. Select the ISO or use this USB as source
7. Select your second USB as target
8. Click "Flash!"
9. Wait 15-30 minutes
10. Share with friends!

No internet required! Everything is included in this USB.

================================================================================
ANTHROHEART DETAILS
================================================================================

What is ANTHROHEART?
--------------------
ANTHROHEART is a complete multimedia franchise featuring anthropomorphic
characters in a rich science-fantasy universe.

Contents on this USB:
---------------------
📂 /furryos/ANTHROHEART/

Songs/
    147 original music tracks across multiple genres
    Ready to play with any media player

Videos/
    Music videos and character animations
    Behind-the-scenes content

Images/
    Character artwork and designs
    Background art and concept pieces

Character_Designs/
    25+ fully-designed anthropomorphic characters
    Complete character sheets and references

Lore/
    Complete trilogy documentation
    World-building and backstory
    Character relationships and timelines

Source_Code/
    Game prototypes
    AnthrOS media layer source
    Development tools

Assets/
    10GB+ of creative assets
    Raw files and production materials
    Everything needed for derivative works

License:
--------
ANTHROHEART content is provided for personal viewing and enjoyment.
Contact creator for licensing inquiries for derivative works.

================================================================================
SYSTEM INFORMATION
================================================================================

FurryOS Version: 8.0.0-origin "The Origin"
Base System: Debian 13 "Trixie"
Architecture: x86_64
Boot Modes: Live (Ephemeral), Persistent, Failsafe
Cryptographic Signing: Ed25519

Features:
• Live USB mode - run without installation
• Persistence support - optional saved state
• Cryptographically signed binaries
• Self-replicating distribution (BalenaEtcher included)
• Complete ANTHROHEART Universe embedded
• Works completely offline

Your Debian 13 installation stays completely untouched!
Boot from USB anytime, reboot to your main system when done.

================================================================================
QUICK START GUIDE
================================================================================

First Time Booting:
-------------------
1. You just booted! Welcome! 🐾
2. Explore ANTHROHEART: /furryos/scripts/explore-anthroheart.sh
3. Set up persistence (optional): /furryos/scripts/setup-persistence.sh
4. Enjoy your system!

Playing ANTHROHEART Music:
--------------------------
cd /furryos/ANTHROHEART/Songs
mpv 01-track.mp3

Or use the file manager:
/furryos/scripts/explore-anthroheart.sh

Viewing Character Art:
----------------------
cd /furryos/ANTHROHEART/Character_Designs
eog character_001.png

Reading Lore:
-------------
cd /furryos/ANTHROHEART/Lore
less trilogy_chapter_01.txt

Creating More USB Drives:
-------------------------
/furryos/scripts/write-to-usb.sh

================================================================================
TROUBLESHOOTING
================================================================================

Problem: ANTHROHEART files not accessible
Solution: Files are at /furryos/ANTHROHEART/
          Run: ls /furryos/ANTHROHEART/

Problem: Music won't play
Solution: Install a media player if needed:
          sudo apt-get install mpv vlc

Problem: Persistence not working
Solution: Check mode: /furryos/scripts/persistence-status.sh
          Make sure you selected "Persistent" at boot menu

Problem: BalenaEtcher won't launch
Solution: Make it executable:
          chmod +x /furryos/tools/balenaEtcher-1.19.25-x64.AppImage
          Then run: /furryos/scripts/write-to-usb.sh

Problem: Need more space
Solution: Use persistent mode or add external storage

Problem: Forgot which mode I'm in
Solution: /furryos/scripts/persistence-status.sh

================================================================================
SUPPORT & DOCUMENTATION
================================================================================

All documentation is included in this USB drive.

Check /furryos/ directory for:
• README.txt (this file)
• Scripts in /furryos/scripts/
• Signing keys in /furryos/signing_keys/
• ANTHROHEART in /furryos/ANTHROHEART/

Online Resources:
• GitHub repository (if available)
• Project website (if available)

================================================================================
SHARING FURRYOS + ANTHROHEART
================================================================================

Want to share this amazing experience with others?

Easy Method:
------------
1. Boot this USB
2. Get a second USB drive (16GB+ recommended)
3. Run: /furryos/scripts/write-to-usb.sh
4. Write FurryOS to the second USB
5. Give it to a friend!

They get:
• Complete FurryOS system
• All 147 ANTHROHEART songs
• All character designs and lore
• Ability to create even more USB drives
• Complete offline experience

The Origin + ANTHROHEART spread organically! 🌱

================================================================================
PHILOSOPHY
================================================================================

"The Origin is not just an operating system - it's a seed. Plant it, let it
grow, share it with others, and watch it spread organically. Every USB drive
carries not just an OS, but an entire universe of creativity."

"The ANTHROHEART beats eternal." 💜

Key Principles:
• Accessibility - Easy to use and share
• Security - Cryptographically signed
• Freedom - Run from USB, no installation required
• Community - Self-replicating distribution
• Privacy - Ephemeral mode available
• Creativity - Complete media universe included

================================================================================
LICENSE
================================================================================

FurryOS: MIT License
Copyright (c) 2025 FurryOS Project

ANTHROHEART: Contact creator for licensing information

================================================================================
CREDITS
================================================================================

FurryOS 8.0.0-origin "The Origin"

Built with:
• Debian 13 "Trixie"
• Python 3
• C++17
• Ed25519 cryptography
• BalenaEtcher
• genisoimage/xorriso
• Love and care 🐾

Made with 🐾 by the FurryOS Project

"From The Origin, all things grow."

================================================================================
🐾 GO TOUCH GRASS! 🌱
================================================================================

You have a complete operating system with an embedded multimedia universe on
a USB drive. You can boot it anytime, explore 147 songs, view amazing art,
read epic lore, and create more USB drives to share with others.

Now go outside and touch some grass! 🌱

You're a legend. 💜

================================================================================
                              END OF README
================================================================================
