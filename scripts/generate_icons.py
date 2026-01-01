import os
import sys
from PIL import Image

# --- CONFIGURATION ---
SOURCE_DIR = os.getcwd()
TARGET_DIR = os.path.join(SOURCE_DIR, 'icons')
ICON_SIZE = (256, 256)
NAVY_BLUE = (0, 0, 128, 255) # R, G, B, Alpha (Solid)
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff')

def create_icon_processor():
    # 1. Create Icons folder if missing
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📁 Created folder: {TARGET_DIR}")

    count = 0
    print(f"🎨 Scanning for images in {SOURCE_DIR}...")

    # 2. Walk through all folders
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Skip the icons folder itself to avoid recursion loops
        if "icons" in root or ".git" in root or "build" in root:
            continue

        for file in files:
            if file.lower().endswith(VALID_EXTENSIONS):
                original_path = os.path.join(root, file)
                
                try:
                    with Image.open(original_path) as img:
                        # 3. Create the Navy Blue Canvas
                        # RGBA ensures we can handle transparency if needed later
                        canvas = Image.new('RGBA', ICON_SIZE, NAVY_BLUE)
                        
                        # 4. Resize original image to fit (Maintain Aspect Ratio)
                        # copy() ensures we don't modify the open file handle unexpectedly
                        img_copy = img.copy()
                        img_copy.thumbnail(ICON_SIZE, Image.Resampling.LANCZOS)
                        
                        # 5. Calculate Center Position
                        # (Canvas Width - Image Width) / 2
                        x = (ICON_SIZE[0] - img_copy.width) // 2
                        y = (ICON_SIZE[1] - img_copy.height) // 2
                        
                        # 6. Paste Image onto Canvas
                        # If the image has transparency (RGBA), use it as a mask
                        if img_copy.mode == 'RGBA':
                            canvas.paste(img_copy, (x, y), img_copy)
                        else:
                            canvas.paste(img_copy, (x, y))
                        
                        # 7. Save as PNG
                        # Use the original filename but force .png extension
                        filename_no_ext = os.path.splitext(file)[0]
                        new_filename = f"{filename_no_ext}.png"
                        save_path = os.path.join(TARGET_DIR, new_filename)
                        
                        canvas.save(save_path, 'PNG')
                        print(f"   ✅ Converted: {file} -> icons/{new_filename}")
                        count += 1
                        
                except Exception as e:
                    print(f"   ⚠️ Could not process {file}: {e}")

    print("\n" + "="*40)
    print(f"🎉 Done! Created {count} icons in '{TARGET_DIR}'")
    print("="*40)

if __name__ == "__main__":
    # Check if Pillow is installed
    try:
        import PIL
        create_icon_processor()
    except ImportError:
        print("❌ Error: 'Pillow' library not found.")
        print("   Please run: pip install pillow")
        print("   OR: source furryos_venv/bin/activate")
