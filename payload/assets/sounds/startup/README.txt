═══════════════════════════════════════════════════════════════════════════════
                          📁 SOUNDS/STARTUP FOLDER
═══════════════════════════════════════════════════════════════════════════════

PUT YOUR LOGIN SOUND HERE

REQUIRED FILE:
  • startup.ogg          ← Login sound (MUST EXIST!)

SPECIFICATIONS:
  • Format: OGG Vorbis (.ogg)
  • Duration: 2-5 seconds recommended
  • Bitrate: 128 kbps or higher
  • Filename: EXACTLY "startup.ogg" (lowercase!)

PURPOSE:
  This sound plays when users log in to the desktop.

EXAMPLES:
  ✅ startup.ogg          (REQUIRED - login sound)

❌ WRONG:
  ❌ StartUp.ogg          (Capital letters - Linux is case-sensitive!)
  ❌ startup.mp3          (Wrong format - must be .ogg)
  ❌ startup.wav          (Wrong format - must be .ogg)
  ❌ login.ogg            (Wrong name - must be "startup.ogg")

HOW TO CONVERT:
  ffmpeg -i your_sound.mp3 -codec:a libvorbis -q:a 5 startup.ogg
  ffmpeg -i your_sound.wav -codec:a libvorbis -q:a 5 startup.ogg
  ffmpeg -i your_sound.mp3 -t 5 -codec:a libvorbis -q:a 5 startup.ogg
