═══════════════════════════════════════════════════════════════════════════════
                            📁 SPLASH FOLDER
═══════════════════════════════════════════════════════════════════════════════

PUT YOUR BOOT SPLASH SCREEN HERE

REQUIRED FILE:
  • splash.png           ← Boot screen image (MUST EXIST!)

SPECIFICATIONS:
  • Format: PNG (.png)
  • Size: 1024×768 OR 1920×1080 pixels
  • Filename: EXACTLY "splash.png" (lowercase!)
  • Background: Dark backgrounds work best for readability

PURPOSE:
  This image is shown during system boot via Plymouth, before the login screen.
  It should contain your FurryOS branding/logo.

EXAMPLES:
  ✅ splash.png           (REQUIRED - boot screen)

❌ WRONG:
  ❌ Splash.png           (Capital S - Linux is case-sensitive!)
  ❌ splash.PNG           (Capital extension)
  ❌ boot.png             (Wrong name - must be "splash.png")
  ❌ splash.jpg           (Wrong format - must be .png)

HOW TO CREATE:
  convert -size 1024x768 xc:background splash.png
  convert your_image.jpg splash.png
  convert -resize 1024x768! your_image.png splash.png
