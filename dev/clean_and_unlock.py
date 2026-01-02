import os
import shutil
import subprocess
import sys
import getpass

# --- CONFIGURATION ---
ROOT_DIR = os.getcwd()

# Folders created by live-build that get locked by root
LOCKED_FOLDERS = [
    'chroot',
    'binary',
    'cache',
    '.build',
    'local',
    'config/binary',
    'config/bootstrap',
    'config/chroot',
    'config/common',
    'config/source'
]

FILES_TO_REMOVE = [
    'build.log',
    'binary.hybrid.iso',
    'live-image-amd64.hybrid.iso'
]

def run_as_root():
    """Checks if running as root, if not, restarts with sudo."""
    if os.geteuid() != 0:
        print("🔒 This script needs Root permissions to delete build artifacts.")
        print("   Relaunching with sudo...")
        try:
            # Re-execute the current script with sudo
            args = ['sudo', sys.executable] + sys.argv
            os.execvp('sudo', args)
        except Exception as e:
            print(f"❌ Failed to relaunch: {e}")
            sys.exit(1)

def get_real_user():
    """Finds the actual user (not root) to give ownership back to."""
    # When running under sudo, SUDO_USER holds the original username
    user = os.environ.get('SUDO_USER')
    if not user:
        print("⚠️  Could not detect original user. Defaulting to current owner of build.sh")
        # Fallback: check owner of a file
        stat_info = os.stat('build.sh')
        import pwd
        user = pwd.getpwuid(stat_info.st_uid).pw_name
    return user

def clean_artifacts():
    print("🧹 Cleaning up build artifacts...")

    # 1. Run standard live-build clean
    try:
        print("   Exec: lb clean --purge")
        subprocess.run(['lb', 'clean', '--purge'], check=False)
    except FileNotFoundError:
        print("   (live-build not installed, skipping lb clean)")

    # 2. Force delete locked folders
    for folder in LOCKED_FOLDERS:
        path = os.path.join(ROOT_DIR, folder)
        if os.path.exists(path):
            try:
                print(f"   🗑️  Removing: {folder}/")
                shutil.rmtree(path)
            except Exception as e:
                print(f"   ⚠️  Could not remove {folder}: {e}")

    # 3. Remove stray files
    for file in FILES_TO_REMOVE:
        path = os.path.join(ROOT_DIR, file)
        if os.path.exists(path):
            os.remove(path)

def unlock_project(user):
    print(f"🔓 Unlocking project for user: '{user}'...")

    # Force change ownership of EVERYTHING in this folder back to the user
    try:
        subprocess.run(['chown', '-R', f'{user}:{user}', ROOT_DIR], check=True)
        # Fix permissions so you can write/delete
        subprocess.run(['chmod', '-R', 'u+rwX', ROOT_DIR], check=True)
        print("   ✅ Ownership reclaimed.")
    except Exception as e:
        print(f"   ❌ Error fixing permissions: {e}")

if __name__ == "__main__":
    print("🛡️  FurryOS Cleanup & Unlock Tool")

    # 1. Ensure we have power
    run_as_root()

    # 2. Identify the human user
    human_user = get_real_user()

    # 3. Nuke the mess
    clean_artifacts()

    # 4. Give the folder back to the human
    unlock_project(human_user)

    print("\n✨ Done! Your project folder is clean and unlocked.")
