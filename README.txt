╔═══════════════════════════════════════════════════════════════════════════════╗
║              🦊 FurryOS Gen2.1 Active Development Folder 🦊                  ║
║                        Quick Start Guide                                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This folder contains everything you need to create your custom FurryOS assets
and generate the distribution ZIP file.

═══════════════════════════════════════════════════════════════════════════════
🚀 QUICK START (3 STEPS)
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Open Asset Folders
────────────────────────────────────────────────────────────────────────────────

cd scripts
chmod +x open_asset_folders.sh
./open_asset_folders.sh

This opens all asset folders in your file manager so you can drag and drop
your files.


STEP 2: Add Your Assets
────────────────────────────────────────────────────────────────────────────────

REQUIRED (must add these):
  • payload/assets/wallpapers/default.jpg     (Desktop wallpaper, 1920×1080+)
  • payload/assets/splash/splash.png          (Boot screen, 1024×768 or 1920×1080)
  • payload/assets/sounds/startup/startup.ogg (Login sound, 2-5 seconds)

OPTIONAL (add if you want):
  • payload/assets/sounds/shutdown/shutdown.ogg (Logout sound)
  • payload/assets/images/*                     (UI images, backgrounds)
  • payload/assets/icons/*                      (Custom app icons, logos)
  • payload/assets/music/*                      (Theme music, background audio)

⚠️  ALL FILENAMES MUST BE LOWERCASE! (default.jpg not Default.jpg)

Each folder has a README.txt explaining what goes there.


STEP 3: Create the Asset ZIP
────────────────────────────────────────────────────────────────────────────────

cd scripts
chmod +x create_asset_zip.sh
./create_asset_zip.sh

This creates: FurryOS_Gen2.1_Payload_Assets.zip

Upload this ZIP to: https://furry-os.org/assets/FurryOS_Gen2.1_Payload_Assets.zip


═══════════════════════════════════════════════════════════════════════════════
📁 FOLDER STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

FurryOS_Gen2.1_Active/
├── payload/assets/              ← Your custom assets go here
│   ├── wallpapers/
│   │   ├── README.txt           (explains what goes here)
│   │   └── default.jpg          ← YOU ADD THIS (1920×1080+ JPEG)
│   ├── splash/
│   │   ├── README.txt
│   │   └── splash.png           ← YOU ADD THIS (1024×768 PNG)
│   ├── sounds/
│   │   ├── startup/
│   │   │   ├── README.txt
│   │   │   └── startup.ogg      ← YOU ADD THIS (2-5 sec OGG)
│   │   └── shutdown/
│   │       ├── README.txt
│   │       └── shutdown.ogg     ← OPTIONAL (2-5 sec OGG)
│   ├── images/
│   │   ├── README.txt
│   │   └── (your UI images)     ← OPTIONAL
│   ├── icons/
│   │   ├── README.txt
│   │   └── (your custom icons)  ← OPTIONAL
│   └── music/
│       ├── README.txt
│       └── (your theme music)   ← OPTIONAL
│
├── desktop_shortcuts/           ← Desktop shortcut files (.desktop)
│   ├── furryos-mode-switcher.desktop
│   ├── furryos-assets-browser.desktop
│   ├── furryos-documentation.desktop
│   ├── furryos-install-packages.desktop
│   └── furryos-asset-installer.desktop
│
├── scripts/                     ← Helper scripts
│   ├── open_asset_folders.sh   (opens all asset folders for you)
│   └── create_asset_zip.sh     (creates the distribution ZIP)
│
├── documentation/               ← Reference documentation
│   └── README.txt              (copy all docs here for reference)
│
└── README.txt                   ← THIS FILE


═══════════════════════════════════════════════════════════════════════════════
📋 REQUIRED FILES CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Before running create_asset_zip.sh, make sure you have:

☐ payload/assets/wallpapers/default.jpg
  • Format: JPEG
  • Size: 1920×1080 pixels MINIMUM (higher OK: 2560×1440, 3840×2160)
  • Filename: EXACTLY "default.jpg" (lowercase!)

☐ payload/assets/splash/splash.png
  • Format: PNG
  • Size: 1024×768 OR 1920×1080 pixels
  • Filename: EXACTLY "splash.png" (lowercase!)

☐ payload/assets/sounds/startup/startup.ogg
  • Format: OGG Vorbis
  • Duration: 2-5 seconds
  • Filename: EXACTLY "startup.ogg" (lowercase!)


═══════════════════════════════════════════════════════════════════════════════
🔧 WHAT EACH SCRIPT DOES
═══════════════════════════════════════════════════════════════════════════════

scripts/open_asset_folders.sh
  → Opens all asset folders in your file manager
  → Makes it easy to drag-and-drop your files
  → Shows which folders are required vs optional

scripts/create_asset_zip.sh
  → Verifies all required files exist
  → Creates FurryOS_Gen2.1_Payload_Assets.zip with correct structure
  → Shows what to upload and where


═══════════════════════════════════════════════════════════════════════════════
🖥️  DESKTOP SHORTCUTS
═══════════════════════════════════════════════════════════════════════════════

The desktop_shortcuts/ folder contains 5 .desktop files that end users will get:

1. furryos-mode-switcher.desktop
   → Switch between 5 modes (Granny/Normal/Gamer/Hacker/Ghost)

2. furryos-assets-browser.desktop
   → Browse and edit wallpapers, images, icons, music, sounds

3. furryos-documentation.desktop
   → Read FurryOS guides and documentation

4. furryos-install-packages.desktop
   → Install additional software packages

5. furryos-asset-installer.desktop
   → Run the asset installer to download/update assets

These are automatically included in the asset ZIP and installed by
install_furryos_assets.sh


═══════════════════════════════════════════════════════════════════════════════
📤 AFTER CREATING THE ZIP
═══════════════════════════════════════════════════════════════════════════════

1. Upload FurryOS_Gen2.1_Payload_Assets.zip to:
   https://furry-os.org/assets/FurryOS_Gen2.1_Payload_Assets.zip

2. Upload install_furryos_assets.sh (provided separately) to:
   https://furry-os.org/install_furryos_assets.sh

3. Test the download:
   wget https://furry-os.org/assets/FurryOS_Gen2.1_Payload_Assets.zip

4. Users will then run:
   wget https://furry-os.org/install_furryos_assets.sh
   chmod +x install_furryos_assets.sh
   ./install_furryos_assets.sh


═══════════════════════════════════════════════════════════════════════════════
⚠️  CRITICAL REMINDERS
═══════════════════════════════════════════════════════════════════════════════

1. ALL FILENAMES MUST BE LOWERCASE
   ✅ default.jpg (correct)
   ❌ Default.jpg (WRONG - capital D)
   ❌ DEFAULT.JPG (WRONG - all caps)

2. EXACT FILENAMES REQUIRED
   ✅ default.jpg (not wallpaper.jpg or desktop.jpg)
   ✅ splash.png (not boot.png or screen.png)
   ✅ startup.ogg (not login.ogg or StartUp.ogg)

3. CORRECT FILE FORMATS
   ✅ Wallpaper: JPEG (.jpg)
   ✅ Splash: PNG (.png)
   ✅ Sounds: OGG Vorbis (.ogg)

4. READ THE README.txt IN EACH FOLDER
   Each asset folder has a README.txt explaining specifications


═══════════════════════════════════════════════════════════════════════════════
❓ NEED HELP?
═══════════════════════════════════════════════════════════════════════════════

• Read README.txt files in each payload/assets/ subfolder
• Check FURRYOS_FOLDER_STRUCTURE_GUIDE.txt (in documentation/)
• Review FURRYOS_ASSET_ZIP_GUIDE.txt (in documentation/)
• Check INDEX_START_HERE.txt for quick reference


═══════════════════════════════════════════════════════════════════════════════
🦊 SUMMARY
═══════════════════════════════════════════════════════════════════════════════

1. Run: ./scripts/open_asset_folders.sh
2. Add your wallpaper, splash, and sounds to the opened folders
3. Run: ./scripts/create_asset_zip.sh
4. Upload FurryOS_Gen2.1_Payload_Assets.zip to your server
5. Users download and run install_furryos_assets.sh
6. They build FurryOS with YOUR custom assets!

═══════════════════════════════════════════════════════════════════════════════

🎉 Everything is organized and ready to use!

═══════════════════════════════════════════════════════════════════════════════
