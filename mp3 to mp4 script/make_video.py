import os
import glob
import sys
import re
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from moviepy import CompositeVideoClip, ColorClip, ImageClip

# Change the working directory to the script's folder automatically
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

RESOURCES_DIR = "resources"
SETTINGS_FILE = os.path.join(RESOURCES_DIR, "settings.txt")
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"  # Default backup system font

# Default configuration values
config = {
    "font_size": 40,
    "text_color": "white",
    "image_width": 540,
    "max_characters_per_line": 24,
    "video_width": 1280,
    "video_height": 720,
    "fps": 24,
    "fit_video_to_image_size": 0,
    "audio_codec": "copy",
    "audio_bitrate": "320k"
}

try:
    # 1. Load dynamic properties from settings.txt if available
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if key in config:
                        if key in ["text_color", "audio_codec", "audio_bitrate"]:
                            config[key] = value
                        else:
                            config[key] = int(value)

    # 2. Try to find your custom .ttf font file inside the resources folder
    ttf_files = glob.glob(os.path.join(RESOURCES_DIR, "*.ttf"))
    if ttf_files:
        FONT_PATH = ttf_files[0] # FIX: Extract first element string from list

    # 3. Scan for ANY common audio file format
    audio_extensions = ["*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg", "*.aac", "*.wma"]
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(RESOURCES_DIR, ext)))
    if not audio_files:
        raise FileNotFoundError("No supported audio file found inside the 'resources' folder.")
    AUDIO_FILE = audio_files[0] # FIX: Extract first element string from list

    # 4. Scan for ANY common image file format
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp", "*.tiff"]
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(RESOURCES_DIR, ext)))
    if not image_files:
        raise FileNotFoundError("No supported image file found inside the 'resources' folder.")
    IMAGE_FILE = image_files[0] # FIX: Extract first element string from list

    # --- ADJUST VIDEO SIZE TO IMAGE SIZE IF ENABLED ---
    if config["fit_video_to_image_size"] == 1:
        with Image.open(IMAGE_FILE) as img:
            config["video_width"], config["video_height"] = img.size
            config["image_width"] = config["video_width"]

    # 5. Check if the text file exists and has content (OPTIONAL TEXT SYSTEM)
    TEXT_FILE = os.path.join(RESOURCES_DIR, "your_text.txt")    
    has_text = False
    YOUR_TEXT = ""

    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding="utf-8") as file:
            raw_content = file.read().strip()
        if raw_content:
            has_text = True
            final_lines = []
            for line in raw_content.splitlines():
                words = line.strip().split()
                if not words:
                    final_lines.append("")
                    continue
                current_line = []
                for word in words:
                    if len(" ".join(current_line + [word])) > config["max_characters_per_line"]:
                        final_lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        current_line.append(word)
                if current_line:
                    final_lines.append(" ".join(current_line))
            YOUR_TEXT = "\n".join(final_lines)

    # --- GET AUDIO DURATION FOR PERCENTAGE CALCULATION ---
    FFMPEG_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
    probe_cmd = [FFMPEG_BINARY, "-i", AUDIO_FILE]
    probe_process = subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True, errors='ignore')
    duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", probe_process.stderr)
    
    if not duration_match:
        raise ValueError("Could not determine audio duration for the progress bar.")
        
    hours, minutes, seconds = map(float, duration_match.groups())
    total_duration_seconds = (hours * 3600) + (minutes * 60) + seconds
    total_frames = int(total_duration_seconds * config["fps"])

    print(f"Using Font: {os.path.basename(FONT_PATH)}")
    print(f"Detected Audio: {os.path.basename(AUDIO_FILE)}")
    print(f"Detected Image: {os.path.basename(IMAGE_FILE)}")
    print(f"Text Enabled: {has_text}")
    print(f"Audio Codec Mode: {config['audio_codec']} ({config['audio_bitrate'] if config['audio_codec'] != 'copy' else 'Uncompressed Stream'})")
    print("\nGenerating background frame image...")

    background_black = ColorClip(size=(config["video_width"], config["video_height"]), color=(0, 0, 0)).with_duration(1)
    clips_to_composite = [background_black]

    # 6. Build the visual layers conditionally
    if has_text:
        text_area_width = config["video_width"] // 2
        text_image = Image.new("RGBA", (text_area_width, config["video_height"]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_image)
        
        pil_font = ImageFont.truetype(FONT_PATH, config["font_size"])
        text_bbox = draw.textbbox((0, 0), YOUR_TEXT, font=pil_font)
        text_height = text_bbox[3] - text_bbox[1]
        
        x_pos = 10  
        y_pos = (config["video_height"] - text_height) // 2
        if y_pos < 10: y_pos = 10 
        
        draw.text((x_pos, y_pos), YOUR_TEXT, font=pil_font, fill=config["text_color"])
        
        temp_text_img_path = os.path.join(RESOURCES_DIR, "temp_text_layer.png")
        text_image.save(temp_text_img_path)
        
        text_clip = ImageClip(temp_text_img_path).with_duration(1).with_position((50, 0))
        clips_to_composite.append(text_clip)

        image_x = (config["video_width"] // 2) + 50
        image_clip = (ImageClip(IMAGE_FILE)
                      .with_duration(1)
                      .resized(width=config["image_width"])  
                      .with_position((image_x, "center")))
        clips_to_composite.append(image_clip)
    else:
        image_clip = (ImageClip(IMAGE_FILE)
                      .with_duration(1)
                      .resized(width=config["image_width"])  
                      .with_position(("center", "center")))
        clips_to_composite.append(image_clip)
        temp_text_img_path = None

    video_frame = CompositeVideoClip(clips_to_composite, size=(config["video_width"], config["video_height"])).with_fps(config["fps"])
    temp_frame_path = os.path.join(RESOURCES_DIR, "temp_frame.png")
    video_frame.save_frame(temp_frame_path, t=0.5)

    print("\nExecuting instant render via FFmpeg...")
    print("--- PROGRESS ---")

    # 7. Call FFmpeg
    ffmpeg_cmd = [
        FFMPEG_BINARY, "-y",
        "-progress", "pipe:1", 
        "-loop", "1", "-i", temp_frame_path,
        "-i", AUDIO_FILE,
        "-c:v", "libx264", "-tune", "stillimage",
        "-pix_fmt", "yuv420p", 
        "-c:a", config["audio_codec"],
        "-b:a", config["audio_bitrate"],
        "-shortest", "-preset", "ultrafast",
        "-r", str(config["fps"]),
        "youtube_ready.mp4"
    ]
    
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    for line in process.stdout:
        if "frame=" in line:
            try:
                current_frame = int(line.split("=")[1].strip())
                percentage = min(100, int((current_frame / total_frames) * 100))
                sys.stdout.write(f"\rRendering Video: {percentage}% [{current_frame}/{total_frames} frames]")
                sys.stdout.flush()
            except:
                pass

    process.wait()
    sys.stdout.write(f"\rRendering Video: 100% [{total_frames}/{total_frames} frames]\n")

    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)
    if temp_text_img_path and os.path.exists(temp_text_img_path):
        os.remove(temp_text_img_path)

    print("----------------")
    print("\n Success! Your video 'youtube_ready.mp4' is ready for upload.")

except Exception as error:
    print("\n--- AN ERROR OCCURRED ---")
    print(f"Error Details: {error}")
    print("-------------------------\n")

finally:
    input("Press Enter to close this window...")
