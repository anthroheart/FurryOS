#!/usr/bin/env python3

import os
import sys

# ===== CONFIG =====
# Folders with MORE than this many files will be collapsed.
# We skip this check for the top-level folders (like ANTHROHEART)
HUGE_FILE_THRESHOLD = 100
# ==================

total_files = 0
total_dirs = 0
total_size = 0

def human(size):
    """Convert bytes to human readable string."""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.0f}{unit}"
        size /= 1024
    return f"{size:.0f}P"

def get_dir_stats(path):
    """Pre-scan a directory to count files/size recursively."""
    files_count = 0
    size_count = 0
    try:
        for root, dirs, filenames in os.walk(path):
            files_count += len(filenames)
            for f in filenames:
                try:
                    fp = os.path.join(root, f)
                    if not os.path.islink(fp):
                        size_count += os.path.getsize(fp)
                except OSError:
                    pass
    except (PermissionError, OSError):
        pass
    return files_count, size_count

def tree(path, prefix="", depth=0):
    global total_files, total_dirs, total_size

    try:
        entries = sorted(os.listdir(path))
    except (PermissionError, OSError):
        print(f"{prefix}└── [Access Denied]")
        return

    # Filter valid entries
    valid_entries = []
    for e in entries:
        full_path = os.path.join(path, e)
        if os.path.isdir(full_path) or os.path.isfile(full_path):
            valid_entries.append(e)

    count = len(valid_entries)

    for i, entry in enumerate(valid_entries):
        full_path = os.path.join(path, entry)
        is_last = (i == count - 1)

        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")

        if os.path.isdir(full_path):
            # === FOLDER LOGIC ===

            # RULE: If depth is 0 (we are in TOP), ALWAYS expand.
            # Otherwise, check if it's huge.
            should_expand = False

            f_count, d_size = get_dir_stats(full_path)

            if depth == 0:
                # Always show contents of top-level folders (ANTHROHEART, assets, etc)
                should_expand = True
            elif f_count <= HUGE_FILE_THRESHOLD:
                # Normal folder, not too big
                should_expand = True

            if should_expand:
                print(f"{prefix}{connector}{entry}/")
                total_dirs += 1
                tree(full_path, child_prefix, depth + 1)
            else:
                # It is deep and HUGE -> Collapse it
                print(f"{prefix}{connector}[{human(d_size)}] {entry}/   (Collapsed: {f_count} files)")
                total_dirs += 1
                total_files += f_count
                total_size += d_size

        else:
            # === FILE LOGIC ===
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            print(f"{prefix}{connector}[{human(size)}] {entry}")
            total_files += 1
            total_size += size

if __name__ == "__main__":
    if len(sys.argv) < 2:
        ROOT = os.getcwd()
    else:
        ROOT = sys.argv[1]

    if ROOT == ".": ROOT = os.getcwd()

    if not os.path.isdir(ROOT):
        print(f"Error: {ROOT} is not a directory")
        sys.exit(1)

    print(f"[{os.path.abspath(ROOT)}]")

    # Start tree with depth=0
    tree(ROOT, prefix="", depth=0)

    print()
    print("-" * 40)
    print(f"Total: {human(total_size)} used in {total_dirs} directories, {total_files} files")
