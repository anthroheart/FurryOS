import os
import shutil
import sys
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_ROOT = Path.cwd()
# Destination is one level up: /TOP/GitHub/FurryOS_Artifacts/
ARTIFACT_DIR = PROJECT_ROOT.parent / "FurryOS_Artifacts"

# 🟢 WHITELIST: These are the ONLY things that stay in the repo.
# Everything else in the root folder gets moved out.
KEEP_ROOT_ITEMS = {
    '.git',
    '.gitignore',
    'assets',         # We scan inside this later to remove keys
    'config',
    'docs',
    'lore',
    'scripts',
    'src',
    'build.sh',
    'clean_and_unlock.sh',
    'setup_venv.sh',
    'requirements.txt',
    'README.md',
    'LICENSE',
    # Keep the python tools we made
    'finalize_project.py',
    'create_final_handbook.py',
    'generate_icons.py',
    'tag_music.py',
    'patch_neofetch.py',
    'update_admin_panel.py',
    'prepare_for_github.py', # Keep this script itself
    'FurryOS_Official_Handbook.pdf' # Keep the PDF documentation
}

# 🔴 SECURITY BLACKLIST: These specific files are moved no matter where they are.
SENSITIVE_FILES = {
    'Gemini_API.key.txt',
    'anthro_identity.key',
    'furryos_signing.key',
    'private.pem'
}

def move_item(item_path, dest_folder):
    """Safely moves a file or folder, overwriting destination if it exists."""
    try:
        dest_path = dest_folder / item_path.name

        # If destination exists, delete it first to avoid collision errors
        if dest_path.exists():
            if dest_path.is_dir():
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)

        shutil.move(str(item_path), str(dest_path))
        print(f"   ➡️  Moved: {item_path.name}")
        return True
    except PermissionError:
        print(f"   ❌ PERMISSION DENIED: {item_path.name} (Are you root? Try 'sudo')")
        return False
    except Exception as e:
        print(f"   ⚠️ Error moving {item_path.name}: {e}")
        return False

def main():
    print("🧹 Starting GitHub Preparation & Cleanup...")
    print(f"📍 Source: {PROJECT_ROOT}")
    print(f"📦 Storage: {ARTIFACT_DIR}")

    # 1. Create Storage Directory
    if not ARTIFACT_DIR.exists():
        try:
            os.makedirs(ARTIFACT_DIR)
            print("   ✅ Created artifact storage directory.")
        except PermissionError:
            print("   ❌ Critical: Cannot create storage directory. Run with sudo.")
            sys.exit(1)

    # 2. Clean Root Directory
    print("\n[1/3] Sweeping Root Directory...")
    moved_count = 0
    for item in PROJECT_ROOT.iterdir():
        # Skip items in the Keep List
        if item.name in KEEP_ROOT_ITEMS:
            continue

        # Move everything else (build folders, ISOs, logs, venv, backups)
        if move_item(item, ARTIFACT_DIR):
            moved_count += 1

    # 3. Security Scan (Recursive)
    print("\n[2/3] Scanning for Sensitive Keys...")
    key_count = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Don't scan inside .git
        if '.git' in root: continue

        for file in files:
            is_sensitive = False

            # Check filename against blacklist
            if file in SENSITIVE_FILES: is_sensitive = True
            if file.endswith('.key'): is_sensitive = True
            if file.endswith('.iso'): is_sensitive = True # Catch stray ISOs in subfolders

            if is_sensitive:
                src_path = Path(root) / file
                # Determine destination (flattened into artifacts root for safety)
                print(f"   🔐 Securing sensitive file: {src_path.relative_to(PROJECT_ROOT)}")
                move_item(src_path, ARTIFACT_DIR)
                key_count += 1

    # 4. Generate .gitignore if missing
    print("\n[3/3] Final Checks...")
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("*.iso\n*.key\n*.key.txt\nvenv/\nfurryos_venv/\n__pycache__/\nbuild.log\n.DS_Store\n")
        print("   ✅ Created .gitignore")

    print("\n" + "="*60)
    print("✨ CLEANUP COMPLETE")
    print("="*60)
    print(f"Moved {moved_count} root items and {key_count} sensitive files.")
    print(f"Your clean project is ready in: {PROJECT_ROOT}")
    print(f"Your ISOs and Keys are safe in: {ARTIFACT_DIR}")
    print("\nTo upload to GitHub:")
    print("1. git init")
    print("2. git add .")
    print("3. git commit -m 'Initial Commit of FurryOS Golden Master'")
    print("4. git push")

if __name__ == "__main__":
    # Check for root if we see build folders owned by root
    if os.geteuid() != 0 and (PROJECT_ROOT / "chroot").exists():
        print("⚠️  WARNING: Build artifacts detected. You probably need to run this with 'sudo'.")
        print("   Command: sudo python3 prepare_for_github.py")
        print("   (You can fix ownership later with: sudo chown -R $USER:$USER .)")
        sys.exit(1)

    main()
