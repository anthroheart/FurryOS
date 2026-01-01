import os
import shutil
import sys
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_ROOT = Path.cwd()
ARTIFACT_DIR = PROJECT_ROOT.parent / "FurryOS_Artifacts"

# 🔍 THE HIT LIST: If a file ends with these, it gets moved.
# This prevents 1GB system files or compiled EXEs from hitting GitHub.
BINARY_EXTENSIONS = {
    '.iso', '.squashfs', '.img', '.bin',          # OS Images (Massive)
    '.exe', '.dll', '.so', '.elf', '.o', '.obj',  # Compiled Code
    '.pyc',                                       # Python Bytecode
    '.cpt', '.bak', '.swp',                       # Backups/Temp
    '.key', '.pem'                                # Secrets
}

# 🔍 FOLDER HIT LIST: These folders are completely moved if found
BAD_FOLDERS = {
    '__pycache__',
    'venv',
    'furryos_venv',
    'chroot',          # Live-build artifact (Root owned, very heavy)
    'binary',          # Live-build artifact
    '.build',          # Live-build artifact
    'cache',           # Live-build artifact
    'local'            # Live-build artifact
}

def move_artifact(path):
    try:
        # Recreate the folder structure in the artifacts dir so we don't lose where it came from
        rel_path = path.relative_to(PROJECT_ROOT)
        dest_path = ARTIFACT_DIR / rel_path

        # Make sure parent directory exists in destination
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(path), str(dest_path))
        print(f"   🚀 Moved heavy/binary file: {rel_path}")
    except Exception as e:
        print(f"   ⚠️ Could not move {path.name}: {e}")

def deep_clean():
    print("🧹 Starting Deep Binary Sweep...")

    if not ARTIFACT_DIR.exists():
        os.makedirs(ARTIFACT_DIR, exist_ok=True)

    # 1. Sweep specifically for the Heavy OS files in src/kernel
    # (These are the most likely cause of the Git hang)
    kernel_dir = PROJECT_ROOT / "src" / "kernel"
    if kernel_dir.exists():
        print(f"   🔎 Scanning {kernel_dir} for OS images...")
        for file in kernel_dir.iterdir():
            if file.suffix in BINARY_EXTENSIONS:
                move_artifact(file)

    # 2. General Recursive Sweep
    print("   🔎 Scanning entire project for stray binaries...")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip .git folder
        if '.git' in dirs:
            dirs.remove('.git')

        root_path = Path(root)

        # CHECK FOLDERS
        # We iterate a copy of list to allow modifying the original for traversal
        for dirname in dirs[:]:
            if dirname in BAD_FOLDERS:
                full_dir_path = root_path / dirname
                print(f"   📦 Moving heavy folder: {dirname}")
                try:
                    shutil.move(str(full_dir_path), str(ARTIFACT_DIR / dirname))
                    dirs.remove(dirname) # Don't walk inside moved folder
                except PermissionError:
                    print(f"   ❌ Permission Denied on {dirname}. Run with sudo!")

        # CHECK FILES
        for filename in files:
            file_path = root_path / filename
            if file_path.suffix in BINARY_EXTENSIONS:
                move_artifact(file_path)

    # 3. Create a Robust .gitignore
    # This prevents Git from ever looking at these files again
    print("\n🛡️  Generating .gitignore firewall...")
    gitignore_content = """
# OS Artifacts (Heavy)
*.iso
*.squashfs
*.img
*.bin

# Compiled Binaries
*.exe
*.dll
*.so
*.o
*.obj
*.elf

# Build Systems
chroot/
binary/
cache/
.build/
local/
build_artifacts/

# Python
__pycache__/
*.pyc
venv/
furryos_venv/

# Secrets
*.key
*.pem
Gemini_API.key.txt
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

    print("\n✅ Deep Clean Complete.")
    print("   Your project is now lightweight text and source code.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  Warning: You should probably run this with 'sudo' to move locked build folders.")
    deep_clean()
