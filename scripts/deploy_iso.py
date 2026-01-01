#!/usr/bin/env python3
"""
===============================================================================
FURRYOS DEPLOYER: UNIVERSAL ACCESS EDITION
===============================================================================
1. BOOT: Injects pre-extracted kernel files.
2. DATA: Embeds 9GB ANTHROHEART library.
3. USER EXP: Injects PDF Guide & Smart Symlinking (Library/Docs).
4. BUILD: Generates Hybrid ISO.
===============================================================================
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def find_api_key():
    """
    Intelligently hunts for the API key by walking up the directory tree.
    Works regardless of where this script is run from.
    """
    import os, sys
    filename = 'Gemini_API.key.txt'
    current_search_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk up the tree (max 5 levels) to find the 'assets' folder
    for _ in range(5):
        potential_key = os.path.join(current_search_dir, 'assets', filename)
        if os.path.exists(potential_key):
            return potential_key
        
        # Move up one level
        parent_dir = os.path.dirname(current_search_dir)
        if parent_dir == current_search_dir: # We hit the root
            break
        current_search_dir = parent_dir
    
    # Fallback: Check Desktop
    desktop_fallback = os.path.expanduser('~/Desktop/Gemini_API.key.txt')
    if os.path.exists(desktop_fallback):
        return desktop_fallback

    print("❌ CRITICAL ERROR: Could not find 'Gemini_API.key.txt' anywhere.")
    sys.exit(1)


# --- Configuration ---
VERSION = "8.2.0-origin"
BUILD_DIR = Path("furryos_build")
ISO_WORK = BUILD_DIR / "iso_workspace"
OUTPUT_DIR = Path("output")

# Paths
KERNEL_SRC = Path("kernel")
ANTHROHEART_SRC = Path("ANTHROHEART")
ASSETS_DIR = Path("assets")
DOCS_SRC = Path("FurryOS_Complete_Documentation.pdf")
ISO_NAME = f"furryos-{VERSION}-x86_64.iso"

# Note: The original script provided does not contain existing API key loading logic
# (e.g., definitions of API_KEY_FILE or opening 'key.txt') to replace.
# The 'find_api_key' function is inserted as requested.

def run_cmd(cmd, desc):
    print(f"⚡ {desc}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def setup_workspace():
    print("🧹 Cleaning workspace...")
    if ISO_WORK.exists(): shutil.rmtree(ISO_WORK)

    dirs = [
        "boot/grub",
        "live",
        "furryos/bin",
        "furryos/assets",
        "furryos/scripts",
        "furryos/source",
        "furryos/docs"      # NEW: Documentation folder
    ]
    for d in dirs:
        (ISO_WORK / d).mkdir(parents=True, exist_ok=True)

def inject_kernel_files():
    print("🐧 Injecting Kernel from /TOP/kernel/...")
    required = ["vmlinuz", "initrd.img", "filesystem.squashfs"]
    for filename in required:
        src = KERNEL_SRC / filename
        dst = ISO_WORK / "live" / filename
        if not src.exists():
            print(f"❌ CRITICAL: {filename} missing in /TOP/kernel/")
            sys.exit(1)
        shutil.copy2(src, dst)

def copy_content():
    # 1. AnthroHeart Library
    if ANTHROHEART_SRC.exists():
        print(f"📦 Found ANTHROHEART Library! Copying...")
        dest = ISO_WORK / "furryos/ANTHROHEART"
        subprocess.run(f"rsync -a --info=progress2 '{ANTHROHEART_SRC}/' '{dest}/'", shell=True)

    # 2. PDF User Guide
    if DOCS_SRC.exists():
        print(f"📘 Embedding User Guide...")
        shutil.copy2(DOCS_SRC, ISO_WORK / "furryos/docs/FurryOS_User_Guide.pdf")
    else:
        print("⚠️  PDF Guide not found (Run compile_docs.py first).")

def inject_user_experience():
    print("🧠 Injecting Smart User Experience (Welcome Wagon)...")

    # This script runs on login to wire up the Library and Docs
    wagon_code = r'''#!/usr/bin/env python3
"""
🐾 FurryOS Welcome Wagon
- Links ANTHROHEART library to Home Folder
- Copies User Guide to Documents
- Checks Persistence
"""
import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
ISO_ROOT = Path("/lib/live/mount/medium") # Standard Debian Live mount point
# Fallback if finding mount fails (search common mounts)
if not (ISO_ROOT / "furryos").exists():
    # Try finding where the ISO is mounted
    for root, dirs, files in os.walk("/run/media"):
        if "furryos" in dirs:
            ISO_ROOT = Path(root)
            break
    if not (ISO_ROOT / "furryos").exists():
        # Last ditch: check /run/live/medium
        ISO_ROOT = Path("/run/live/medium")

LIBRARY_SRC = ISO_ROOT / "furryos/ANTHROHEART"
DOCS_SRC = ISO_ROOT / "furryos/docs/FurryOS_User_Guide.pdf"
FLAG_FILE = HOME / ".config/furryos/setup_complete"

def setup_environment():
    # 1. Symlink the Library (Read-Only Access)
    lib_link = HOME / "ANTHROHEART_LIBRARY"
    if LIBRARY_SRC.exists() and not lib_link.exists():
        try:
            os.symlink(LIBRARY_SRC, lib_link)
            print("   Linked ANTHROHEART Library")
        except Exception as e: print(f"Link Error: {e}")

    # 2. Copy User Guide to Documents
    docs_dir = HOME / "Documents"
    docs_dir.mkdir(exist_ok=True)
    target_pdf = docs_dir / "FurryOS_User_Guide.pdf"

    if DOCS_SRC.exists() and not target_pdf.exists():
        try:
            shutil.copy2(DOCS_SRC, target_pdf)
            print("   Copied User Guide")
        except Exception as e: print(f"Copy Error: {e}")

    # 3. Create Config Flag
    (HOME / ".config/furryos").mkdir(parents=True, exist_ok=True)
    with open(FLAG_FILE, "w") as f: f.write("Setup Done")

    # 4. Show Welcome Notification
    if os.environ.get("DISPLAY"):
        subprocess.run(["notify-send", "FurryOS Ready", "Library linked & Guide in Documents!"])

if __name__ == "__main__":
    if not FLAG_FILE.exists():
        setup_environment()
'''

    # Save the script
    script_dest = ISO_WORK / "furryos/scripts/welcome_wagon.py"
    with open(script_dest, "w") as f:
        f.write(wagon_code)
    os.chmod(script_dest, 0o755)

    # Inject other tools
    if (ASSETS_DIR / "omni.py").exists():
        shutil.copy2(ASSETS_DIR / "omni.py", ISO_WORK / "furryos/bin/omni")

    # Embed Source
    src_dest = ISO_WORK / "furryos/source"
    ignore = shutil.ignore_patterns("furryos_build", "output", "*.iso", "venv", "kernel")
    if Path("assets").exists(): shutil.copytree("assets", src_dest / "assets", ignore=ignore)
    for f in ["quick_start.sh", "GENOME.yaml"]:
        if Path(f).exists(): shutil.copy2(f, src_dest)

def populate_binaries():
    print("📦 Copying Binaries...")
    src_bin = BUILD_DIR / "bin"
    if src_bin.exists():
        for f in src_bin.glob("*"): shutil.copy2(f, ISO_WORK / "furryos/bin")

    # Etcher
    etcher = list(ASSETS_DIR.glob("balenaEtcher*.AppImage"))
    if etcher: shutil.copy2(etcher[0], ISO_WORK / "furryos/assets")

def create_grub_config():
    print("📝 Creating GRUB Config...")
    cfg = r"""
set default=0
set timeout=5
menuentry "FurryOS Live (Desktop)" {
    linux /live/vmlinuz boot=live components quiet splash persistence username=anthro hostname=furryos
    initrd /live/initrd.img
}
menuentry "FurryOS Live (Safe)" {
    linux /live/vmlinuz boot=live components nomodeset username=anthro
    initrd /live/initrd.img
}
"""
    with open(ISO_WORK / "boot/grub/grub.cfg", "w") as f:
        f.write(cfg)

def build_iso():
    print(f"\n💿 Building Final ISO: {ISO_NAME}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_iso = OUTPUT_DIR / ISO_NAME

    cmd = f"grub-mkrescue -o '{output_iso}' {ISO_WORK} -- -volid 'FURRYOS_LIVE'"
    try:
        run_cmd(cmd, "Generating Hybrid ISO")
    except:
        print("❌ Build failed. Install grub-common/xorriso/mtools")
        sys.exit(1)

    if output_iso.exists():
        print(f"\n✅ SUCCESS! ISO Created: {output_iso}")

def main():
    setup_workspace()
    inject_kernel_files()
    copy_content()
    inject_user_experience() # <--- Wires up Library/Docs
    populate_binaries()
    create_grub_config()
    build_iso()

if __name__ == "__main__":
    main()