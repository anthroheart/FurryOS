═══════════════════════════════════════════════════════════════════════════════
                            📁 MUSIC FOLDER
═══════════════════════════════════════════════════════════════════════════════

PUT THEME MUSIC / BACKGROUND AUDIO HERE (OPTIONAL)

OPTIONAL FILES:
  • Theme songs
  • Background music for login screen
  • Ambient audio
  • System sounds (longer audio)

SPECIFICATIONS:
  • Formats: OGG Vorbis (.ogg), MP3, FLAC
  • OGG Vorbis recommended for best Linux compatibility
  • Any duration (typically 30 seconds to 5 minutes for theme songs)
  • Bitrate: 128-320 kbps

PURPOSE:
  Optional background music or theme songs for your custom FurryOS.
  These are OPTIONAL and can be used for:
  • Login screen background music
  • Welcome screen music
  • Theme songs
  • Ambient background audio

EXAMPLES:
  ✅ theme-song.ogg            (Main FurryOS theme song)
  ✅ login-ambient.ogg         (Calm music for login screen)
  ✅ welcome-music.ogg         (Welcome screen music)
  ✅ background-loop.ogg       (Looping background audio)

HOW TO CONVERT:
  ffmpeg -i your_music.mp3 -codec:a libvorbis -q:a 5 theme-song.ogg
  ffmpeg -i your_music.flac -codec:a libvorbis -q:a 5 theme-song.ogg

NOTES:
  • This folder is completely optional
  • Keep file sizes reasonable (< 10MB per file recommended)
  • OGG Vorbis format is preferred over MP3 for open-source compatibility
  • Consider looping audio for background music
