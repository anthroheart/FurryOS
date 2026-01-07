#!/usr/bin/env python3
"""
FurryOS Gen2.1 Builder - Complete GUI
One-click asset management + ISO building with automatic live boot setup
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess

PROJECT_ROOT = os.getcwd()
BUILD_SCRIPT = os.path.join(PROJECT_ROOT, "build_furryos.sh")
GENOME_FILE = os.path.join(PROJECT_ROOT, "GENOME.yaml")
PAYLOAD_DIR = os.path.join(PROJECT_ROOT, "payload")

ASSET_FOLDERS = {
    "Desktop Files": os.path.join(PAYLOAD_DIR, "assets", "desktop"),
    "Wallpapers": os.path.join(PAYLOAD_DIR, "assets", "wallpapers"),
    "Splash Screens": os.path.join(PAYLOAD_DIR, "assets", "splash"),
    "Sounds": os.path.join(PAYLOAD_DIR, "assets", "sounds"),
    "Images": os.path.join(PAYLOAD_DIR, "assets", "images"),
    "Icons": os.path.join(PAYLOAD_DIR, "assets", "images", "icons"),
    "Music": os.path.join(PAYLOAD_DIR, "assets", "music"),
    "Docs": os.path.join(PAYLOAD_DIR, "assets", "docs"),
}


class FurryOSBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FurryOS Gen2.1 Builder")
        self.geometry("950x800")
        self.minsize(950, 800)
        self._create_widgets()

    def _create_widgets(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=15)
        ttk.Label(header, text="🐾 FurryOS Gen2.1 Builder",
                  font=("Sans", 18, "bold")).pack()
        ttk.Label(header, text="Enhanced: Auto-setup on live boot • Full asset deployment",
                  foreground="#0066cc", font=("Sans", 10, "bold")).pack()

        # Notebook tabs
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Tab 1: Quick Start
        tab_start = ttk.Frame(nb)
        nb.add(tab_start, text="🚀 Quick Start")
        self._build_quickstart_tab(tab_start)

        # Tab 2: Asset Folders
        tab_assets = ttk.Frame(nb)
        nb.add(tab_assets, text="📁 Asset Folders")
        self._build_assets_tab(tab_assets)

        # Tab 3: What's New
        tab_new = ttk.Frame(nb)
        nb.add(tab_new, text="✨ Gen2.1 Features")
        self._build_whats_new_tab(tab_new)

        # Tab 4: Full Guide
        tab_guide = ttk.Frame(nb)
        nb.add(tab_guide, text="📖 Full Guide")
        self._build_guide_tab(tab_guide)

        # Status bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.status_label = ttk.Label(status_frame, text="Ready to build Gen2.1",
                                      foreground="#28a745", font=("Sans", 10, "bold"))
        self.status_label.pack(side="left")
        ttk.Button(status_frame, text="Edit GENOME.yaml",
                  command=self.edit_genome).pack(side="right", padx=(5, 0))
        ttk.Button(status_frame, text="Quit", command=self.quit).pack(side="right")

    def _build_quickstart_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Three Simple Steps:",
                  font=("Sans", 14, "bold")).pack(anchor="w", pady=(0, 20))

        # Step 1
        step1 = ttk.LabelFrame(frame, text="1️⃣ Open Asset Folders", padding=20)
        step1.pack(fill="x", pady=10)
        ttk.Label(step1, text="Copy your files into these folders:",
                  font=("Sans", 11)).pack(anchor="w", pady=(0, 10))

        items = [
            "• desktop/ → .desktop launcher files, README.txt",
            "• wallpapers/ → default.jpg (1920x1080+ recommended)",
            "• splash/ → splash.png (boot screen)",
            "• sounds/ → startup.ogg (login sound)",
            "• music/ → background music files",
            "• docs/ → PDF documentation",
            "• images/ → images for ~/FurryOS folder"
        ]
        for item in items:
            ttk.Label(step1, text=item, font=("Monospace", 9)).pack(anchor="w", padx=20)

        ttk.Button(step1, text="▶ Open All Asset Folders",
                  command=self.open_all_folders).pack(anchor="w", pady=(15, 0))

        # Step 2
        step2 = ttk.LabelFrame(frame, text="2️⃣ Build Your Gen2.1 ISO", padding=20)
        step2.pack(fill="x", pady=10)
        ttk.Label(step2, text="Build ISO with automatic live boot setup:",
                  font=("Sans", 11)).pack(anchor="w", pady=(0, 10))

        features = [
            "• Copies ALL assets to /usr/share/furryos",
            "• Sets up autostart for multimedia configuration",
            "• Desktop files appear automatically",
            "• Wallpaper sets on live boot",
            "• Startup sound plays on login",
            "• Creates ~/FurryOS folder in file manager sidebar"
        ]
        for feat in features:
            ttk.Label(step2, text=feat, font=("Monospace", 9),
                     foreground="#0066cc").pack(anchor="w", padx=20)

        ttk.Button(step2, text="🔨 Build FurryOS Gen2.1 ISO",
                  command=self.build_iso).pack(anchor="w", pady=(15, 0))

        # Step 3
        step3 = ttk.LabelFrame(frame, text="3️⃣ Test Your ISO", padding=20)
        step3.pack(fill="x", pady=10)
        ttk.Label(step3, text="Your ISO will be ready here:",
                  font=("Sans", 11)).pack(anchor="w", pady=(0, 10))
        ttk.Label(step3, text="_generated/output/furryos-gen2.1-amd64.iso",
                  font=("Monospace", 10, "bold"),
                  foreground="#007bff").pack(anchor="w", padx=20, pady=5)
        ttk.Button(step3, text="📂 Open Output Folder",
                  command=self.open_generated).pack(anchor="w", pady=(10, 0))

    def _build_assets_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Asset Folders - Click to open:",
                  font=("Sans", 12, "bold")).pack(anchor="w", pady=(0, 15))

        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for name, path in ASSET_FOLDERS.items():
            self._add_folder_row(scrollable_frame, name, path)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(frame, text="Open All Folders at Once",
                  command=self.open_all_folders).pack(pady=10)

    def _build_whats_new_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="✨ What's New in Gen2.1",
                  font=("Sans", 16, "bold")).pack(anchor="w", pady=(0, 20))

        features = scrolledtext.ScrolledText(frame, wrap="word",
                                             font=("Monospace", 10), height=25)
        features.pack(fill="both", expand=True)

        features.insert("1.0", """╔══════════════════════════════════════════════════════════════════╗
║                   FurryOS Gen2.1 New Features                    ║
╚══════════════════════════════════════════════════════════════════╝

🎯 AUTOMATIC LIVE BOOT SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you boot the Gen2.1 ISO in live mode, it now automatically:

✓ Creates ~/FurryOS folder in your home directory
✓ Copies ALL payload assets to ~/FurryOS
✓ Sets your custom wallpaper immediately
✓ Plays startup sound on login
✓ Places all .desktop files on the Desktop
✓ Adds FurryOS to file manager sidebar (like Documents, Pictures)

📁 COMPLETE ASSET DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gen2.1 fixes the asset deployment issues from Gen2:

Before (Gen2):
  • Only one .desktop file appeared
  • Had to manually run setup script
  • Wallpaper didn't change
  • Startup sound didn't play
  • Assets stayed in /usr/share/furryos

After (Gen2.1):
  • ALL .desktop files appear automatically
  • Setup runs automatically on first boot
  • Wallpaper applies immediately
  • Startup sound plays on login
  • Full ~/FurryOS folder created with all content

🗂️ FILE MANAGER INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your FurryOS content now appears in the file manager sidebar
alongside standard folders:

📁 Home
  ├─ 📁 Desktop
  ├─ 📁 Documents
  ├─ 📁 Downloads
  ├─ 📁 Music
  ├─ 📁 Pictures
  ├─ 📁 Videos
  └─ 🐾 FurryOS  ← NEW! Your complete payload here

🔧 TECHNICAL IMPROVEMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• XDG autostart integration
  → furryos-live-setup runs automatically on login

• Proper dconf/gsettings wallpaper setting
  → Multiple methods ensure wallpaper applies

• PulseAudio/ALSA startup sound support
  → Tries multiple audio backends

• /etc/skel integration
  → Live user gets full desktop setup automatically

• Centralized asset storage
  → All assets in /usr/share/furryos, copied to ~/FurryOS

🚀 WORKFLOW IMPROVEMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gen2.1 simplifies everything:

1. Copy your assets to payload/ folders
2. Click "Build FurryOS Gen2.1 ISO"
3. Boot the ISO
4. EVERYTHING WORKS AUTOMATICALLY ✨

No manual script execution needed!
No missing desktop files!
No manual wallpaper setting!
No missing startup sound!

📋 COMPATIBILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Uses same GENOME.yaml as Gen2
• Same payload structure
• Same asset folders
• Fully backward compatible with Gen2 assets
• Just run the new build script!

""")
        features.config(state="disabled")

    def _build_guide_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        guide = scrolledtext.ScrolledText(frame, wrap="word", font=("Monospace", 10))
        guide.pack(fill="both", expand=True)

        guide.insert("1.0", """╔══════════════════════════════════════════════════════════════════╗
║               FurryOS Gen2.1 Builder Complete Guide              ║
╚══════════════════════════════════════════════════════════════════╝

📦 WHAT THIS TOOL DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Builds a custom Debian Live ISO that automatically sets up your
complete FurryOS environment when booted in live mode.

🚀 QUICK START WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Prepare Assets
  → Click "Open All Asset Folders"
  → Copy your files to the opened folders

Step 2: Build ISO
  → Click "Build FurryOS Gen2.1 ISO"
  → Wait 15-25 minutes for build

Step 3: Test
  → Boot ISO in VM or USB
  → Everything auto-configures on first login!

📁 REQUIRED ASSETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

payload/assets/wallpapers/
  ✓ default.jpg - Main wallpaper (1920x1080+)

payload/assets/sounds/
  ✓ startup.ogg - Login sound

payload/assets/desktop/
  ✓ *.desktop - Desktop launcher files
  ✓ README.txt - Desktop readme

payload/assets/ (optional)
  • music/ - Background music
  • docs/ - Documentation PDFs
  • images/ - Additional images
  • splash/ - Boot splash screen

⚙️ HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Build Process:
  1. Downloads Debian Live MATE ISO (first time only)
  2. Extracts filesystem
  3. Copies ALL assets to /usr/share/furryos
  4. Installs autostart script
  5. Configures /etc/skel for live user
  6. Repacks into bootable ISO

Live Boot Process:
  1. User boots ISO
  2. Logs into live desktop
  3. Autostart script runs automatically:
     • Creates ~/FurryOS folder
     • Copies assets from /usr/share/furryos
     • Sets wallpaper
     • Plays startup sound
     • Places desktop files
     • Adds to file manager sidebar

🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If wallpaper doesn't change:
  → Check payload/assets/wallpapers/default.jpg exists
  → File must be named exactly "default.jpg"

If startup sound doesn't play:
  → Check payload/assets/sounds/startup.ogg exists
  → Must be OGG format
  → Keep under 10 seconds for best results

If desktop files don't appear:
  → Check payload/assets/desktop/*.desktop exist
  → Must have .desktop extension
  → Must be valid desktop entry format

If build fails:
  1. Clean up: sudo rm -rf _generated
  2. Retry build

💡 TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Test in VirtualBox first before writing to USB
• Keep wallpaper under 5MB for faster loading
• Use OGG format for sounds (better compression)
• Desktop files must be executable (chmod +x)
• First build takes longest (downloads 3GB ISO)
• Subsequent builds are faster (reuses extracted ISO)

🐾 READY TO BUILD!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Go to "Quick Start" tab to begin building FurryOS Gen2.1!
""")
        guide.config(state="disabled")

    def _add_folder_row(self, parent, label, path):
        row = ttk.Frame(parent, padding=8)
        row.pack(fill="x", pady=3)

        lbl = ttk.Label(row, text=label + ":", width=20, anchor="w",
                       font=("Sans", 10, "bold"))
        lbl.pack(side="left", padx=(0, 10))

        path_lbl = ttk.Label(row, text=path, foreground="#666",
                            font=("Monospace", 9))
        path_lbl.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn = ttk.Button(row, text="Open", command=lambda: self.open_folder(path))
        btn.pack(side="right")

    def open_folder(self, path):
        os.makedirs(path, exist_ok=True)
        try:
            subprocess.Popen(["xdg-open", path])
            self.status_label.config(
                text=f"✓ Opened: {os.path.basename(path)}",
                foreground="#28a745")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open:\n{path}\n\n{e}")

    def open_all_folders(self):
        opened = 0
        for name, path in ASSET_FOLDERS.items():
            os.makedirs(path, exist_ok=True)
            try:
                subprocess.Popen(["xdg-open", path])
                opened += 1
            except:
                pass

        if opened > 0:
            self.status_label.config(
                text=f"✓ Opened {opened} asset folders",
                foreground="#28a745")
        else:
            messagebox.showerror("Error", "Failed to open folders")

    def build_iso(self):
        if not os.path.exists(BUILD_SCRIPT):
            messagebox.showerror("Script Not Found",
                               f"Cannot find:\n{BUILD_SCRIPT}")
            return

        confirm = messagebox.askyesno(
            "Build FurryOS Gen2.1 ISO?",
            "This will:\n"
            "1. Extract Debian ISO (if first run)\n"
            "2. Copy all assets to /usr/share/furryos\n"
            "3. Configure automatic live boot setup\n"
            "4. Build bootable Gen2.1 ISO\n\n"
            "Time: ~15-25 minutes\n\n"
            "Continue?"
        )

        if not confirm:
            return

        self.status_label.config(text="🔨 Building Gen2.1 ISO...",
                                foreground="#007bff")
        self.update()

        try:
            subprocess.Popen([
                "x-terminal-emulator", "-e",
                f"bash -c 'cd {PROJECT_ROOT} && sudo ./build_furryos.sh; "
                f"echo; echo \"Press Enter to close...\"; read'"
            ])
            self.status_label.config(text="✓ Gen2.1 build started",
                                    foreground="#28a745")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch:\n{e}")
            self.status_label.config(text="✗ Build failed to start",
                                    foreground="#dc3545")

    def open_generated(self):
        gen_dirs = [
            os.path.join(PROJECT_ROOT, "_generated", "output"),
            os.path.join(PROJECT_ROOT, "_generated")
        ]

        for gd in gen_dirs:
            if os.path.exists(gd):
                try:
                    subprocess.Popen(["xdg-open", gd])
                    self.status_label.config(text="✓ Opened output folder",
                                           foreground="#28a745")
                    return
                except:
                    pass

        messagebox.showinfo("Not Found",
                          "No output folder exists yet.\n\nBuild your ISO first!")
        self.status_label.config(text="⚠ No output yet", foreground="#ffc107")

    def edit_genome(self):
        if not os.path.exists(GENOME_FILE):
            messagebox.showerror("File Not Found",
                               f"Cannot find:\n{GENOME_FILE}")
            return

        try:
            subprocess.Popen(["xdg-open", GENOME_FILE])
            self.status_label.config(text="✓ Opened GENOME.yaml",
                                   foreground="#28a745")
        except:
            messagebox.showinfo("GENOME.yaml", f"Open manually:\n{GENOME_FILE}")


if __name__ == "__main__":
    app = FurryOSBuilder()
    app.mainloop()
