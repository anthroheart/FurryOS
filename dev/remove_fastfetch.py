import os

ROOT_DIR = os.getcwd()
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

def remove_package_from_files(package_name):
    print(f"✂️  Removing '{package_name}' from configuration files...")
    count = 0

    # Walk through the config directory
    for root, dirs, files in os.walk(CONFIG_DIR):
        for file in files:
            # Look for package lists
            if file.endswith('.list.chroot') or file.endswith('.list'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Filter out the specific package
                    new_lines = [line for line in lines if package_name not in line.strip()]

                    # If lines were removed, write the file back
                    if len(lines) != len(new_lines):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f"   ✅ Removed '{package_name}' from: {file}")
                        count += 1

                except Exception as e:
                    print(f"   ⚠️  Error reading {file}: {e}")

    if count == 0:
        print(f"   ℹ️  '{package_name}' was not found in any active lists. You are already clean.")
    else:
        print(f"   🎉 Removed '{package_name}' from {count} files.")

if __name__ == "__main__":
    remove_package_from_files("fastfetch")
    # Also removing neofetch just to be absolutely double-sure
    remove_package_from_files("neofetch")
