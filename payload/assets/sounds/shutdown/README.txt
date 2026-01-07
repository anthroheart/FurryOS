═══════════════════════════════════════════════════════════════════════════════
                         📁 SOUNDS/SHUTDOWN FOLDER
═══════════════════════════════════════════════════════════════════════════════

PUT YOUR LOGOUT SOUND HERE (OPTIONAL)

OPTIONAL FILE:
  • shutdown.ogg         ← Logout sound (OPTIONAL)

SPECIFICATIONS:
  • Format: OGG Vorbis (.ogg)
  • Duration: 2-5 seconds recommended
  • Bitrate: 128 kbps or higher
  • Filename: EXACTLY "shutdown.ogg" (lowercase!)

PURPOSE:
  This sound plays during system shutdown. This is OPTIONAL - if you don't
  want a shutdown sound, just leave this folder empty.

EXAMPLES:
  ✅ shutdown.ogg         (OPTIONAL - logout sound)
  ✅ (empty folder)       (Also OK - no shutdown sound)

❌ WRONG:
  ❌ Shutdown.ogg         (Capital S - Linux is case-sensitive!)
  ❌ shutdown.mp3         (Wrong format - must be .ogg)
  ❌ logout.ogg           (Wrong name - must be "shutdown.ogg")

HOW TO CONVERT:
  ffmpeg -i your_sound.mp3 -codec:a libvorbis -q:a 5 shutdown.ogg
  ffmpeg -i your_sound.wav -codec:a libvorbis -q:a 5 shutdown.ogg
