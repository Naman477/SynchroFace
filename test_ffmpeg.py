import imageio_ffmpeg
import os
import subprocess

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print(f"FFmpeg exe: {ffmpeg_exe}")

# Test running ffmpeg
try:
    subprocess.check_call([ffmpeg_exe, "-version"])
    print("FFmpeg runs successfully.")
except Exception as e:
    print(f"FFmpeg failed: {e}")

# Test creating a dummy video
import cv2
import numpy as np
import uuid

# Create a dummy video file using imageio or cv2
dummy_video = "dummy_video.mp4"
if not os.path.exists(dummy_video):
    print("Creating dummy video...")
    writer = cv2.VideoWriter(dummy_video, cv2.VideoWriter_fourcc(*'mp4v'), 25, (64, 64))
    for i in range(25):
        frame = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        writer.write(frame)
    writer.release()

# Create dummy audio
dummy_audio = "dummy_audio.wav"
# We can just use an existing wav or create empty one?
# Let's assume we don't need audio for simple copy test or use a silent one.
# But let's try to just copy video.

temp_file = str(uuid.uuid4()) + ".mp4"
cmd = f'""{ffmpeg_exe}" -y -i "{dummy_video}" -c copy "{temp_file}""'
print(f"Running command: {cmd}")
ret = os.system(cmd)
print(f"Return code: {ret}")

if ret == 0 and os.path.exists(temp_file):
    print("FFmpeg copy successful.")
    os.remove(temp_file)
else:
    print("FFmpeg copy failed.")

if os.path.exists(dummy_video):
    os.remove(dummy_video)
