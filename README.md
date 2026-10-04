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

```
Your_Main_Folder/
├── make_video.py
├── dependencies/
│   ├── install_dependencies.py
│   └── install_python.url
└── resources/
    ├── settings.txt
    ├── your_text.txt             (optional)
    ├── your_audio.mp3            (any audio format)
    ├── foreground_cover.png      (or .jpg .gif .mp4 etc.)
    ├── background_image.png      (optional)
    ├── background_video.mp4      (optional)
    └── NotoSans-Regular.ttf      (or any .ttf font)
```

----------------------------------------------------------------------
2. INSTALL DEPENDENCIES (first time only)
----------------------------------------------------------------------

Run the installer. It only downloads what is missing.

```
Windows:
  python dependencies/install_dependencies.py

macOS / Linux:
  python3 dependencies/install_dependencies.py
```

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
    (if both exist, background_video is used)

----------------------------------------------------------------------
4. POSITION (text and cover)
----------------------------------------------------------------------

In settings.txt you can set:

```
text_x_pos / foreground_x_pos
  left | center | right | or a pixel number

text_y_pos / foreground_y_pos
  top | center | bottom | or a pixel number

text_x_offset / text_y_offset
foreground_x_offset / foreground_y_offset
  extra pixels (can be negative)
```

Examples:

```
text_x_pos=left
text_x_offset=50
text_y_pos=center

foreground_x_pos=right
foreground_y_pos=center
foreground_x_offset=-20

foreground_x_pos=center
foreground_y_pos=top
foreground_y_offset=30
```

You can also write combined values like: right+20  or  left-10

----------------------------------------------------------------------
5. OTHER SETTINGS (settings.txt)
----------------------------------------------------------------------

```
video_width / video_height   resolution (default 1280x720)
fps / static_fps             frames per second
fit_video_to_image_size      1 = video size matches the cover image
                             and the cover fills the whole frame
                             (works with background image or video)
                             0 = use video_width / video_height
font_size                    text size
text_color                   text color (white, yellow, red...)
max_characters_per_line      auto line wrap
text_shadow                  0 = off, 1 = on
text_shadow_color            shadow color (example: black)
text_shadow_offset           shadow distance in pixels
foreground_width             cover size (ignored if fit_video_to_image_size=1)
background_opacity           0.0 to 1.0
background_blur_strength     0 to 50
background_scale_mode        stretch / fit / fill
background_loop              1 = loop background video, 0 = play once
background_freeze_last       1 = freeze last frame when done
audio_codec / audio_bitrate  audio quality
video_crf                    quality 0-51 (lower = better, typical 18-28)
video_bitrate                optional, examples: 2M, 5M (overrides CRF)
video_tune                   stillimage / film / animation / grain / empty
video_pix_fmt                usually yuv420p
video_profile / video_level  optional H.264 options
```

----------------------------------------------------------------------
6. RUN THE SCRIPT
----------------------------------------------------------------------

```
python make_video.py
```

Choose option 2 to render.
The output file is: youtube_ready.mp4

Video Output Example:

https://github.com/user-attachments/assets/26446d6b-a430-4a9b-9166-ab6cf597de8f

https://github.com/user-attachments/assets/5b1b21d1-7596-4cec-9aae-23e2540514d2
