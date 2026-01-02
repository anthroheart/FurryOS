import os
import datetime

ROOT_DIR = os.getcwd()
OUTPUT_FILE = "manifest.txt"
IGNORE_DIRS = {'.git', '.build', 'chroot', 'binary', 'cache', '__pycache__', 'local'}
CRITICAL_EXTENSIONS = {'.sh', '.yaml', '.list', '.chroot', '.hook', '.py'}

def get_file_content(filepath):
    """Reads file content for debugging."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"

def scan_project():
    print(f"🕵️  Scanning FurryOS Project Root: {ROOT_DIR}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as report:
        report.write(f"FURRYOS PROJECT MANIFEST\n")
        report.write(f"Generated: {datetime.datetime.now()}\n")
        report.write("="*60 + "\n\n")

        # 1. CHECK FOR ISO FILES
        report.write("--- ISO SEARCH ---\n")
        iso_found = False
        for root, dirs, files in os.walk(ROOT_DIR):
            for file in files:
                if file.endswith(".iso"):
                    iso_path = os.path.join(root, file)
                    size_mb = os.path.getsize(iso_path) / (1024 * 1024)
                    report.write(f"[FOUND ISO] {iso_path} ({size_mb:.2f} MB)\n")
                    iso_found = True
        if not iso_found:
            report.write("NO ISO FILES FOUND.\n")
        report.write("\n")

        # 2. CHECK BUILD LOG TAIL
        report.write("--- BUILD LOG DIAGNOSIS (Last 20 lines) ---\n")
        log_file = os.path.join(ROOT_DIR, 'build.log')
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    tail = lines[-20:] if len(lines) > 20 else lines
                    report.write("".join(tail))
            except:
                report.write("Could not read build.log\n")
        else:
            report.write("build.log does not exist.\n")
        report.write("\n" + "="*60 + "\n\n")

        # 3. FULL FILE TREE & CONTENT
        report.write("--- FILE STRUCTURE & CRITICAL CONTENT ---\n")

        fastfetch_count = 0

        for root, dirs, files in os.walk(ROOT_DIR):
            # Filter directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            level = root.replace(ROOT_DIR, '').count(os.sep)
            indent = ' ' * 4 * level
            report.write(f"{indent}[DIR] {os.path.basename(root)}/\n")

            subindent = ' ' * 4 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                # Check for fastfetch ghost
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        if "fastfetch" in f.read():
                            report.write(f"{subindent}⚠️  WARNING: 'fastfetch' found in {file}\n")
                            fastfetch_count += 1
                except: pass

                report.write(f"{subindent}{file}\n")

                # If it's a critical config file, dump content
                _, ext = os.path.splitext(file)
                if ext in CRITICAL_EXTENSIONS or file == 'build.sh':
                    content = get_file_content(file_path)
                    report.write(f"{subindent}    --- CONTENT START ---\n")
                    # Indent content
                    for line in content.splitlines():
                        report.write(f"{subindent}    | {line}\n")
                    report.write(f"{subindent}    --- CONTENT END ---\n")

        report.write("\n" + "="*60 + "\n")
        report.write(f"DIAGNOSTIC SUMMARY:\n")
        if fastfetch_count > 0:
            report.write(f"❌ CRITICAL: Found {fastfetch_count} files still containing 'fastfetch'. This WILL break the build.\n")
        else:
            report.write(f"✅ CLEAN: No 'fastfetch' found.\n")

    print(f"✅ Manifest generated at: {os.path.join(ROOT_DIR, OUTPUT_FILE)}")

if __name__ == "__main__":
    scan_project()
