import os
import shutil
import datetime
from pathlib import Path
import sys

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


# --- Configuration Constants ---
# Use pathlib for robust and platform-agnostic path manipulation
PROJECT_ROOT: Path = Path.cwd()

# Define paths for key files and directories relative to PROJECT_ROOT
API_KEY_FILE: Path = Path(find_api_key())

# Archive directory will be timestamped to prevent overwriting across runs
ARCHIVE_DIR_NAME: str = 'ARCHIVE_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ARCHIVE_DIR: Path = PROJECT_ROOT / ARCHIVE_DIR_NAME

# Define the desired new project structure directories (names only)
# These will be created directly under PROJECT_ROOT if they don't exist.
NEW_STRUCTURE_DIRS: set[str] = {
    'scripts',
    'assets',
    'config',
    'docs',
    'build',
    'tests',  # Common directory for test files
    'src',    # Common directory for core source code
    'logs'    # Common directory for log files
}

# Mapping of file extensions to their target directories within the new structure
# The keys are file extensions (including the dot), values are directory names.
FILE_EXTENSION_MAP: dict[str, str] = {
    '.sh': 'scripts',
    '.py': 'scripts',
    '.rb': 'scripts',
    '.js': 'scripts',
    '.ps1': 'scripts',
    '.bat': 'scripts',
    '.exe': 'build',  # Executables often belong to build artifacts
    '.dll': 'build',
    '.so': 'build',
    '.bin': 'build',
    '.apk': 'build',
    '.ipa': 'build',
    '.deb': 'build',
    '.rpm': 'build',
    '.dmg': 'build',
    '.iso': 'build',
    '.zip': 'build',
    '.tar.gz': 'build', # Specific handling for double extensions
    '.tgz': 'build',
    '.tar.xz': 'build',
    '.txz': 'build',
    '.tar.bz2': 'build',
    '.tbz2': 'build',
    '.rar': 'build',
    '.7z': 'build',

    '.png': 'assets',
    '.jpg': 'assets',
    '.jpeg': 'assets',
    '.gif': 'assets',
    '.svg': 'assets',
    '.ico': 'assets',
    '.webp': 'assets',
    '.mp3': 'assets',
    '.wav': 'assets',
    '.mp4': 'assets',
    '.avi': 'assets',
    '.mov': 'assets',

    '.yaml': 'config',
    '.yml': 'config',
    '.conf': 'config',
    '.json': 'config',
    '.ini': 'config',
    '.toml': 'config',
    '.env': 'config',

    '.md': 'docs',
    '.txt': 'docs',
    '.rst': 'docs',
    '.rtf': 'docs',
    '.pdf': 'docs',
    '.log': 'logs',

    '.test': 'tests',
    '.spec': 'tests',
    '.e2e': 'tests',
}

# Directories that os.walk should entirely skip scanning (absolute paths)
# This prevents scanning into version control, virtual environments, caches,
# and the archive directory itself, as well as the target structure directories
# where files are meant to end up.
IGNORED_DIRS_TO_SKIP: set[Path] = {
    PROJECT_ROOT / '.git',
    PROJECT_ROOT / '__pycache__',
    PROJECT_ROOT / '.venv',
    PROJECT_ROOT / 'venv',
    ARCHIVE_DIR,
}
# Add all target NEW_STRUCTURE_DIRS to the ignored list to prevent moving
# files that are already correctly placed within these directories.
for d_name in NEW_STRUCTURE_DIRS:
    IGNORED_DIRS_TO_SKIP.add(PROJECT_ROOT / d_name)

# --- Helper Functions ---

def verify_api_key(api_key_path: Path) -> bool:
    """
    Verifies if the API key file exists and contains a non-empty key.

    Args:
        api_key_path: The absolute path to the API key file.

    Returns:
        True if the API key is found and not empty, False otherwise.
    """
    try:
        if not api_key_path.is_file():
            print(f"⚠️  API Key file not found at {api_key_path}.")
            return False

        key = api_key_path.read_text(encoding='utf-8').strip()
        if not key:
            print(f"⚠️  API Key file at {api_key_path} is empty.")
            return False

        print(f"✅ API Key found in {api_key_path.name}.")
        return True
    except IOError as e:
        print(f"❌ Error reading API Key file {api_key_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred while verifying API key: {e}")
        return False

def suggest_moves(root_dir: Path, ignored_paths: set[Path]) -> list[tuple[Path, Path]]:
    """
    Scans the project directory and suggests files to move based on their extension.

    Args:
        root_dir: The root directory of the project to scan.
        ignored_paths: A set of absolute paths to directories that should be skipped
                       during the scan.

    Returns:
        A list of tuples, where each tuple contains (old_file_path, target_directory_path).
    """
    print(f"\nScanning '{root_dir.name}' for organization suggestions...")
    suggested_moves: list[tuple[Path, Path]] = []
    # Get the name of this script file to avoid suggesting moving itself
    current_script_name = Path(__file__).name

    for current_walk_root, dirs, files in os.walk(root_dir):
        current_path_obj = Path(current_walk_root)

        # Optimize os.walk: modify 'dirs' in place to prevent descending into ignored directories
        # Create a new list for dirs to allow modification
        dirs_to_process = []
        for d in dirs:
            dir_path = current_path_obj / d
            # If the directory or any of its parent is in the ignored list, skip it
            if any(dir_path.is_relative_to(ignored_p) for ignored_p in ignored_paths):
                print(f"   Skipping directory: {dir_path.relative_to(PROJECT_ROOT)}")
                continue
            dirs_to_process.append(d)
        dirs[:] = dirs_to_process # Update dirs in-place for os.walk

        # If the current_path_obj itself is an ignored path, skip processing its files
        if any(current_path_obj.is_relative_to(ignored_p) for ignored_p in ignored_paths):
            continue

        for file_name in files:
            # Skip this script file
            if file_name == current_script_name:
                continue

            file_path = current_path_obj / file_name
            suffix = file_path.suffix.lower()  # e.g., '.py', '.txt'

            # Handle common double extensions like .tar.gz
            full_ext = suffix
            if suffix in ['.gz', '.bz2', '.xz'] and file_path.stem.lower().endswith('.tar'):
                full_ext = '.tar' + suffix
            elif suffix == '.tgz': # Often an alias for .tar.gz
                full_ext = '.tar.gz'
            elif suffix == '.tbz2': # Often an alias for .tar.bz2
                full_ext = '.tar.bz2'
            elif suffix == '.txz': # Often an alias for .tar.xz
                full_ext = '.tar.xz'


            target_dir_name = FILE_EXTENSION_MAP.get(full_ext)

            if target_dir_name:
                target_dir_path = root_dir / target_dir_name

                # If the file's current parent directory is NOT its target directory,
                # then suggest a move. This covers files in the root or in incorrect subfolders.
                if file_path.parent != target_dir_path:
                    suggested_moves.append((file_path, target_dir_path))
    return suggested_moves

def execute_organization(moves: list[tuple[Path, Path]], archive_path: Path, new_structure_folder_names: set[str]) -> None:
    """
    Executes the suggested file moves, creating new directories and archiving old versions.

    Args:
        moves: A list of (source_path, target_directory_path) tuples.
        archive_path: The absolute path to the directory where old versions will be archived.
        new_structure_folder_names: A set of directory names (strings) to create
                                    at the project root.
    """
    if not moves:
        print("Everything looks organized already, no files to move!")
        return

    print(f"\nPreparing to organize {len(moves)} files.")

    # 1. Create the archive directory if it doesn't exist
    try:
        archive_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Ensured archive directory exists: {archive_path.relative_to(PROJECT_ROOT)}")
    except OSError as e:
        print(f"❌ Error creating archive directory {archive_path}: {e}")
        sys.exit(1)  # Critical error, cannot proceed without archive

    # 2. Create new structure folders at the project root
    for folder_name in new_structure_folder_names:
        target_folder_path = PROJECT_ROOT / folder_name
        try:
            target_folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Ensured target directory exists: {target_folder_path.relative_to(PROJECT_ROOT)}")
        except OSError as e:
            print(f"❌ Error creating new structure directory {target_folder_path}: {e}")
            # Non-critical, but report and continue
            pass

    print(f"\nPlanning to move {len(moves)} files.")
    print("WARNING: Files with the same name in the target directory will be backed up.")
    confirm = input("Type 'yes' to proceed with moving files: ").lower()

    if confirm == 'yes':
        success_count = 0
        failure_count = 0
        for old_path, target_dir_path in moves:
            file_name = old_path.name
            new_path = target_dir_path / file_name

            try:
                # If a file with the same name already exists at the new target,
                # move it to the archive with a unique timestamped backup name.
                if new_path.is_file():
                    # Generate a timestamp with milliseconds for unique backups
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                    backup_name = f"{file_name}.{timestamp}.bak"
                    backup_path = archive_path / backup_name
                    shutil.move(new_path, backup_path)
                    print(f"   Backed up existing '{new_path.name}' to '{backup_path.relative_to(PROJECT_ROOT)}'")

                # Now move the original file from its old location to the new organized location
                shutil.move(old_path, new_path)
                print(f"✅ Moved: '{old_path.relative_to(PROJECT_ROOT)}' -> '{new_path.relative_to(PROJECT_ROOT)}'")
                success_count += 1
            except FileNotFoundError:
                print(f"❌ Failed to move '{old_path.relative_to(PROJECT_ROOT)}': Source file not found.")
                failure_count += 1
            except PermissionError:
                print(f"❌ Failed to move '{old_path.relative_to(PROJECT_ROOT)}': Permission denied.")
                failure_count += 1
            except shutil.Error as e:
                print(f"❌ Failed to move '{old_path.relative_to(PROJECT_ROOT)}': {e}")
                failure_count += 1
            except Exception as e:
                print(f"❌ An unexpected error occurred while moving '{old_path.relative_to(PROJECT_ROOT)}': {e}")
                failure_count += 1

        print(f"\n--- Organization Summary ---")
        print(f"✅ Successfully moved {success_count} files.")
        if failure_count > 0:
            print(f"❌ Failed to move {failure_count} files. Please check the logs above.")
        print("✅ Organization process complete.")
    else:
        print("❌ Organization aborted by user.")

# --- Main Execution ---

if __name__ == "__main__":
    print(f"Starting FurryOS Project Organizer in '{PROJECT_ROOT}'")

    # Verify API key. This step is independent of file organization,
    # so execution continues even if the key is missing/invalid.
    verify_api_key(API_KEY_FILE)

    # Suggest file moves based on defined rules and ignored directories
    moves_to_perform = suggest_moves(PROJECT_ROOT, IGNORED_DIRS_TO_SKIP)

    # Execute the organization if any moves are suggested
    execute_organization(moves_to_perform, ARCHIVE_DIR, NEW_STRUCTURE_DIRS)