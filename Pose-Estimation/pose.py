from ultralytics import YOLO
import subprocess
import os

# Load model
model = YOLO("models/best.pt")

# Run inference and auto-save video
results = model.predict(
    source="data/airport.mp4",
    save=True,
    show=False
)

# Convert saved .avi to .mp4
avi_path = "runs/pose/predict/airport.avi"
mp4_path = "runs/pose/predict/airport.mp4"

if os.path.exists(avi_path):
    subprocess.run([
        "ffmpeg", "-i", avi_path,
        "-vcodec", "libx264",
        "-crf", "23",
        mp4_path
    ])
    print(f"Converted to MP4: {mp4_path}")
else:
    print("AVI file not found! Conversion skipped.")
