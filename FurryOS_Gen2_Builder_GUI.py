#!/usr/bin/env python3
"""
FurryOS Gen2 Builder - Complete GUI
One-click asset management + ISO building
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
        self.title("FurryOS Gen2 Builder")
        self.geometry("950x750")
        self.minsize(950, 750)

        self._create_widgets()

    def _create_widgets(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=15)
        ttk.Label(header, text="🐾 FurryOS Gen2 Builder", font=("Sans", 18, "bold")).pack()
        ttk.Label(header, text="Simplified workflow: Copy assets → Build ISO",
                 foreground="#666", font=("Sans", 10)).pack()

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

        # Tab 3: Full Guide
        tab_guide = ttk.Frame(nb)
        nb.add(tab_guide, text="📖 Full Guide")
        self._build_guide_tab(tab_guide)

        # Status bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.status_label = ttk.Label(status_frame, text="Ready to build",
                                      foreground="#28a745", font=("Sans", 10, "bold"))
        self.status_label.pack(side="left")

        ttk.Button(status_frame, text="Edit GENOME.yaml", command=self.edit_genome).pack(side="right", padx=(5, 0))
        ttk.Button(status_frame, text="Quit", command=self.quit).pack(side="right")

    def _build_quickstart_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        # Big button workflow
        ttk.Label(frame, text="Three Simple Steps:", font=("Sans", 14, "bold")).pack(anchor="w", pady=(0, 20))

        # Step 1: Open all folders
        step1 = ttk.LabelFrame(frame, text="1️⃣  Open Asset Folders", padding=20)
        step1.pack(fill="x", pady=10)

        ttk.Label(step1, text="Open all 8 asset folders at once. Copy your files into them:",
                 font=("Sans", 11)).pack(anchor="w", pady=(0, 15))

        items = [
            "• desktop/ → README.txt, installer scripts, icons",
            "• wallpapers/ → default.jpg (1920x1080+)",
            "• splash/ → splash.png (boot screen)",
            "• sounds/ → startup.ogg (login sound)",
            "• music/ → background music files",
            "• docs/ → PDF documentation",
            "• images/ → any images you want included"
        ]

        for item in items:
            ttk.Label(step1, text=item, font=("Monospace", 9)).pack(anchor="w", padx=20)

        ttk.Button(step1, text="▶ Open All Asset Folders",
                  command=self.open_all_folders, style="Accent.TButton").pack(anchor="w", pady=(15, 0))

        # Step 2: Build ISO
        step2 = ttk.LabelFrame(frame, text="2️⃣  Build Your Custom ISO", padding=20)
        step2.pack(fill="x", pady=10)

        ttk.Label(step2, text="After copying your assets, click to build the ISO:",
                 font=("Sans", 11)).pack(anchor="w", pady=(0, 10))
        ttk.Label(step2, text="• Extracts base Debian ISO (first time only)",
                 font=("Monospace", 9)).pack(anchor="w", padx=20)
        ttk.Label(step2, text="• Copies your assets into the filesystem",
                 font=("Monospace", 9)).pack(anchor="w", padx=20)
        ttk.Label(step2, text="• Builds bootable FurryOS ISO",
                 font=("Monospace", 9)).pack(anchor="w", padx=20)
        ttk.Label(step2, text="• Takes ~15-25 minutes total",
                 font=("Monospace", 9)).pack(anchor="w", padx=20)

        ttk.Button(step2, text="🔨 Build FurryOS ISO",
                  command=self.build_iso, style="Accent.TButton").pack(anchor="w", pady=(15, 0))

        # Step 3: Get ISO
        step3 = ttk.LabelFrame(frame, text="3️⃣  Get Your ISO", padding=20)
        step3.pack(fill="x", pady=10)

        ttk.Label(step3, text="When done, your ISO will be here:",
                 font=("Sans", 11)).pack(anchor="w", pady=(0, 10))
        ttk.Label(step3, text="_generated/output/FurryOS-Gen2-amd64.iso",
                 font=("Monospace", 10, "bold"), foreground="#007bff").pack(anchor="w", padx=20, pady=5)

        ttk.Button(step3, text="📂 Open Output Folder",
                  command=self.open_generated).pack(anchor="w", pady=(10, 0))

    def _build_assets_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Asset Folders - Click to open each folder:",
                 font=("Sans", 12, "bold")).pack(anchor="w", pady=(0, 15))

        # Create scrollable frame
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

        # Add folder rows
        for name, path in ASSET_FOLDERS.items():
            self._add_folder_row(scrollable_frame, name, path)

        # Open all button
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(frame, text="Open All Folders at Once",
                  command=self.open_all_folders).pack(pady=10)

    def _add_folder_row(self, parent, label, path):
        row = ttk.Frame(parent, padding=8)
        row.pack(fill="x", pady=3)

        lbl = ttk.Label(row, text=label + ":", width=20, anchor="w", font=("Sans", 10, "bold"))
        lbl.pack(side="left", padx=(0, 10))

        path_lbl = ttk.Label(row, text=path, foreground="#666", font=("Monospace", 9))
        path_lbl.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn = ttk.Button(row, text="Open", command=lambda: self.open_folder(path))
        btn.pack(side="right")

    def _build_guide_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill="both", expand=True)

        guide = scrolledtext.ScrolledText(frame, wrap="word", font=("Monospace", 10))
        guide.pack(fill="both", expand=True)

        guide.insert("1.0", """╔══════════════════════════════════════════════════════════════════════╗
║                     FurryOS Gen2 Builder Guide                       ║
╚══════════════════════════════════════════════════════════════════════╝

📦 WHAT THIS TOOL DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Builds a custom Debian Live ISO with:
  • Your wallpapers, sounds, and splash screens
  • Custom desktop scripts and documentation
  • MATE desktop environment
  • All settings from GENOME.yaml


🚀 SIMPLIFIED WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Copy Your Assets
  → Use "Quick Start" tab
  → Click "Open All Asset Folders"
  → Copy your files into the opened folders

Step 2: Build ISO
  → Click "Build FurryOS ISO" button
  → Enter sudo password when prompted
  → Wait ~15-25 minutes for build to complete

Step 3: Get Your ISO
  → Find it in: _generated/output/FurryOS-Gen2-amd64.iso
  → Test it in a VM or write to USB


📁 REQUIRED FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Desktop Assets (payload/assets/desktop/):
  ✓ README.txt - Text file for desktop
  ✓ FurryOS-Installer.sh - Installer launcher script
  ✓ FurryOS-Installer.desktop - Desktop entry
  ✓ install-desktop-scripts.sh - Installation script
  ✓ icons/furryos-installer.png - 128x128 icon

Wallpapers (payload/assets/wallpapers/):
  ✓ default.jpg - Default wallpaper (1920x1080 recommended)

Splash (payload/assets/splash/):
  ✓ splash.png - Boot splash screen (1920x1080)

Sounds (payload/assets/sounds/):
  ✓ startup.ogg - Login sound (OGG format, ~10 seconds)

Optional:
  • music/ - Background music files
  • docs/ - PDF documentation
  • images/ - Any images you want included


⚙️  HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The build script (build_furryos.sh) does everything:

Phase 1: Validation
  → Checks for Debian ISO
  → Validates GENOME.yaml

Phase 2: Build Plan
  → Generates asset installation plan

Phase 5: Extract ISO (first run only)
  → Mounts Debian Live ISO
  → Extracts filesystem.squashfs

Phase 6: Apply Assets
  → Copies wallpapers to /usr/share/backgrounds/furryos/
  → Copies sounds to /usr/share/sounds/furryos/
  → Copies splash to /usr/share/plymouth/themes/furryos/
  → Copies music, docs, images

Phase 7: Desktop Scripts
  → Installs desktop launcher and README
  → Sets up installer icon

Phase 8: Repack ISO
  → Rebuilds squashfs filesystem
  → Creates bootable ISO

Phase 9: Finalize
  → Generates SHA256 checksum
  → Creates provenance notes


💾 OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Final ISO location:
  _generated/output/FurryOS-Gen2-amd64.iso (3-4GB)

Also includes:
  _generated/output/FurryOS-Gen2-amd64.iso.sha256 (checksum)
  _generated/specs/FurryOS-Gen2-PROVENANCE.txt (build info)


🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If build fails:
  1. Clean up: sudo rm -rf _generated
  2. Retry build

If assets don't appear in ISO:
  1. Check files exist in payload/assets/
  2. Check Phase 6 output during build
  3. Verify paths in GENOME.yaml


🐾 READY TO BUILD!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Go to the "Quick Start" tab to begin!
""")

        guide.config(state="disabled")

    def open_folder(self, path):
        os.makedirs(path, exist_ok=True)
        try:
            subprocess.Popen(["xdg-open", path])
            self.status_label.config(text=f"✓ Opened: {os.path.basename(path)}", foreground="#28a745")
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
            self.status_label.config(text=f"✓ Opened {opened} asset folders", foreground="#28a745")
        else:
            messagebox.showerror("Error", "Failed to open folders")

    def build_iso(self):
        if not os.path.exists(BUILD_SCRIPT):
            messagebox.showerror("Script Not Found", f"Cannot find:\n{BUILD_SCRIPT}")
            return

        confirm = messagebox.askyesno(
            "Build FurryOS ISO?",
            "This will:\n"
            "1. Extract Debian ISO (if first run)\n"
            "2. Copy your assets\n"
            "3. Build custom FurryOS ISO\n\n"
            "Time: ~15-25 minutes\n\n"
            "Continue?"
        )

        if not confirm:
            return

        self.status_label.config(text="🔨 Building ISO in terminal...", foreground="#007bff")
        self.update()

        try:
            subprocess.Popen([
                "x-terminal-emulator", "-e",
                f"bash -c 'cd {PROJECT_ROOT} && sudo ./build_furryos.sh; echo; echo \"Press Enter to close...\"; read'"
            ])
            self.status_label.config(text="✓ Build started in terminal", foreground="#28a745")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch:\n{e}")
            self.status_label.config(text="✗ Build failed to start", foreground="#dc3545")

    def open_generated(self):
        gen_dirs = [
            os.path.join(PROJECT_ROOT, "_generated", "output"),
            os.path.join(PROJECT_ROOT, "generated", "iso"),
            os.path.join(PROJECT_ROOT, "_generated"),
            os.path.join(PROJECT_ROOT, "generated")
        ]

        for gd in gen_dirs:
            if os.path.exists(gd):
                try:
                    subprocess.Popen(["xdg-open", gd])
                    self.status_label.config(text=f"✓ Opened output folder", foreground="#28a745")
                    return
                except:
                    pass

        messagebox.showinfo("Not Found",
                           "No output folder exists yet.\n\nBuild your ISO first!")
        self.status_label.config(text="⚠ No output yet", foreground="#ffc107")

    def edit_genome(self):
        if not os.path.exists(GENOME_FILE):
            messagebox.showerror("File Not Found", f"Cannot find:\n{GENOME_FILE}")
            return

        try:
            subprocess.Popen(["xdg-open", GENOME_FILE])
            self.status_label.config(text="✓ Opened GENOME.yaml", foreground="#28a745")
        except:
            messagebox.showinfo("GENOME.yaml", f"Open manually:\n{GENOME_FILE}")

if __name__ == "__main__":
    app = FurryOSBuilder()
    app.mainloop()
