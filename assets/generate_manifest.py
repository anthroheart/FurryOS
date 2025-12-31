import os

# Configuration: Folders to scan relative to where the script is run
DIRS_TO_SCAN = [
    ".",              # Top level
    "assets",         # /TOP/assets
    "guides",         # /TOP/guides
]

# Configuration: File extensions and specific filenames to include
# We exclude binary files like .png to avoid encoding errors
VALID_EXTENSIONS = (
    ".py", ".sh", ".c", ".s", ".yaml", ".txt", ".md", ".json"
)
EXACT_FILES = [
    "Makefile_optimized",
    "requirements.txt",
    "Dockerfile" # Just in case
]

OUTPUT_FILE = "MANIFEST.txt"

def should_include(filename):
    """Checks if a file matches our extensions or exact name lists."""
    if filename in EXACT_FILES:
        return True
    return filename.endswith(VALID_EXTENSIONS) and not filename.startswith("MANIFEST")

def generate_manifest():
    print(f"Generating {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as manifest:
        # Write a header
        manifest.write("FurryOS Source Manifest\n")
        manifest.write("=======================\n\n")

        total_files = 0
        
        for directory in DIRS_TO_SCAN:
            if not os.path.exists(directory):
                print(f"Warning: Directory '{directory}' not found. Skipping.")
                continue

            # Walk through the directory
            for root, _, files in os.walk(directory):
                # Ensure we strictly follow the structure (don't go too deep if not needed)
                # This check ensures we don't scan sub-sub-folders if you only want the immediate children
                # Remove the following 2 lines if you want recursive scanning everywhere
                if directory == "." and root != ".": continue 
                if directory != "." and root != directory: continue

                for file in sorted(files):
                    if should_include(file):
                        filepath = os.path.join(root, file)
                        
                        # Normalize path for readability (remove ./ prefix)
                        clean_path = os.path.normpath(filepath)
                        
                        try:
                            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                                content = f.read()
                                
                            manifest.write(f"FILE_START: {clean_path}\n")
                            manifest.write("-" * 40 + "\n")
                            manifest.write(content)
                            if not content.endswith("\n"):
                                manifest.write("\n")
                            manifest.write("-" * 40 + "\n")
                            manifest.write(f"FILE_END: {clean_path}\n\n")
                            
                            print(f"Added: {clean_path}")
                            total_files += 1
                        except Exception as e:
                            print(f"Error reading {clean_path}: {e}")

    print(f"\nSuccess! Scanned {total_files} files into {OUTPUT_FILE}.")

if __name__ == "__main__":
    generate_manifest()
