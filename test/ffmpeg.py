import shutil

ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path:
    print("good")
else:
    print("ffmpeg.exe not found.")