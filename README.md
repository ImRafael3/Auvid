# Auvid
A simple and ugly mp3 to mp4 script

This script was made by ImRafael.

TikTok: .imrafael1

HOW TO USE THE SCRIPT
----------------------------------------------------------------------

This script creates a watermark free .mp4 video ready for YouTube from 
any audio file, image file, and text file. The text will appear on the 
left side of the screen over a pure black background, and the image 
will be placed on the right side.

----------------------------------------------------------------------
1. FOLDER LAYOUT
----------------------------------------------------------------------

Your project folder can be named anything you want. Inside this main 
folder, you must have the main script file and a subfolder named 
"resources".

----------------------------------------------------------------------
2. HOW TO PREPARE YOUR FILES
----------------------------------------------------------------------
Inside the "resources" subfolder, you need to prepare the following 
files:

- Image file: Place any standard image file (JPG, PNG, WEBP, or BMP).
- Audio file: Place any standard audio file (MP3, WAV, M4A, or AAC).
- Text file: Create a file named "your_text.txt". Write the text that 
  you want to show on the left side of the video. The script will 
  keep your manual line breaks.
- Font file: Place one custom font file ending in ".ttf". The script 
  will automatically read and apply it. If no font is found, it will 
  use system Arial.

----------------------------------------------------------------------
3. HOW TO EDIT SETTINGS (settings.txt)
----------------------------------------------------------------------
The file "settings.txt" inside the "resources" folder allows you to 
change the properties of the video without editing the Python code. 

Open it with any text editor to modify these variables:
- font_size: Changes the size of the text.
- text_color: Sets the color of the text (example: white, yellow, red).
- image_width: Changes how big the image looks on the right side.
- max_characters_per_line: Sets the maximum character width before a 
  word automatically jumps to the next line.
- video_width and video_height: Changes the final video resolution 
  (default is 1280x720).
- fps: Frames per second of the video output (default is 24).
- fit_video_to_image_size: Fits video to image size

Once all your files are inside the "resources" folder, you can simply double-click the 
"make_video.py" file to run it.

