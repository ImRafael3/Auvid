# Auvid
A simple and ugly mp3 to mp4 script

This script was made by ImRafael.

TikTok: .imrafael1

# HOW TO USE

This script creates a watermark-free .mp4 video ready for YouTube
from any audio file, image/video file, and optional text file.

Text appears on the left side by default.
The cover image/video appears on the right by default.
You can change positions freely (see section 4).

----------------------------------------------------------------------
1. FOLDER STRUCTURE
----------------------------------------------------------------------

Your_Main_Folder/
    make_video.py
    install_dependencies.py
    install_dependencies.bat      (Windows)
    install_dependencies.sh       (macOS / Linux)
    resources/
        settings.txt
        your_text.txt             (optional)
        your_audio.mp3            (any audio format)
        foreground_cover.png      (or .jpg .gif .mp4 etc.)
        background_image.png      (optional)
        NotoSans-Regular.ttf      (or any .ttf font)

----------------------------------------------------------------------
2. INSTALL DEPENDENCIES (first time only)
----------------------------------------------------------------------

Run the installer. It only downloads what is missing.

  Windows:
    Double-click  install_dependencies.bat
    or run:  python install_dependencies.py

  macOS / Linux:
    ./install_dependencies.sh
    or run:  python3 install_dependencies.py

Required packages:
  - Pillow
  - FFmpeg  (via imageio-ffmpeg or system install)

If a package is already installed, it is skipped.

----------------------------------------------------------------------
3. PREPARE YOUR FILES
----------------------------------------------------------------------

Put these files inside the "resources" folder:

  - Audio: any .mp3 .wav .m4a .flac .ogg .aac
  - Cover: name it foreground_cover + extension
           (.png .jpg .webp .gif .mp4 .mov .avi)
  - Text:  your_text.txt  (optional, line breaks are kept)
  - Font:  any .ttf file (optional, falls back to system font)
  - Background (optional): background_image.png or background_video.mp4

----------------------------------------------------------------------
4. POSITION (text and cover)
----------------------------------------------------------------------

In settings.txt you can set:

  text_x_pos / foreground_x_pos
    left | center | right | or a pixel number

  text_y_pos / foreground_y_pos
    top | center | bottom | or a pixel number

  text_x_offset / text_y_offset
  foreground_x_offset / foreground_y_offset
    extra pixels (can be negative)

Examples:

  text_x_pos=left
  text_x_offset=50
  text_y_pos=center

  foreground_x_pos=right
  foreground_y_pos=center
  foreground_x_offset=-20

  foreground_x_pos=center
  foreground_y_pos=top
  foreground_y_offset=30

You can also write combined values like: right+20  or  left-10

----------------------------------------------------------------------
5. OTHER SETTINGS (settings.txt)
----------------------------------------------------------------------

  video_width / video_height   resolution (default 1280x720)
  fps / static_fps             frames per second
  font_size                    text size
  text_color                   text color (white, yellow, red...)
  max_characters_per_line      auto line wrap
  foreground_width             cover size
  background_opacity           0.0 to 1.0
  background_blur_strength     0 to 50
  background_scale_mode        stretch / fit / fill
  audio_codec / audio_bitrate  audio quality

----------------------------------------------------------------------
6. RUN THE SCRIPT
----------------------------------------------------------------------

  python make_video.py

Choose option 2 to render.
The output file is: youtube_ready.mp4

