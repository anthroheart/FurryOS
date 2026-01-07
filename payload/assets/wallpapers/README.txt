═══════════════════════════════════════════════════════════════════════════════
                           📁 WALLPAPERS FOLDER
═══════════════════════════════════════════════════════════════════════════════

PUT YOUR DESKTOP WALLPAPERS HERE

REQUIRED FILE:
  • default.jpg          ← Main desktop wallpaper (MUST EXIST!)

SPECIFICATIONS:
  • Format: JPEG (.jpg)
  • Size: 1920×1080 pixels MINIMUM (higher is better: 2560×1440, 3840×2160)
  • Filename: EXACTLY "default.jpg" (lowercase!)

OPTIONAL:
  You can add additional wallpapers with any names. The build script will only
  use default.jpg as the main wallpaper, but you can include extras for users
  to select later.

EXAMPLES:
  ✅ default.jpg          (REQUIRED - will be the desktop background)
  ✅ wallpaper2.jpg       (Optional alternative)
  ✅ dark-theme.jpg       (Optional)

❌ WRONG:
  ❌ Default.jpg          (Capital D - Linux is case-sensitive!)
  ❌ wallpaper.jpg        (Wrong name - must be "default.jpg")
  ❌ desktop.png          (Wrong format - must be .jpg)

HOW TO CONVERT:
  convert your_image.png default.jpg
  convert -resize 1920x1080! your_image.jpg default.jpg
