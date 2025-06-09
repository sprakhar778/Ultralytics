from ultralytics import YOLO
import subprocess
import os
# Load a model
model = YOLO("models/best.pt")  # load an official model
# model = YOLO("path/to/best.pt")  # load a custom model

# Predict with the modelt
results = model("data/drone-view.mp4",stream=True)  # predict on an image



# Convert saved .avi to .mp4
avi_path = "runs/obb/predict/drone-view.avi"
mp4_path = "runs/obb/predict/drone-view.mp4"

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


# Access the results
for result in results:
    xywhr = result.obb.xywhr  # center-x, center-y, width, height, angle (radians)
    xyxyxyxy = result.obb.xyxyxyxy  # polygon format with 4-points
    names = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
    confs = result.obb.conf  # confidence score of each box