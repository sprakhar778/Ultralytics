import cv2
import numpy as np
from ultralytics import solutions

cap = cv2.VideoCapture("../data/conveyr-belt.mp4")
assert cap.isOpened(), "Error reading video file"

# Define a horizontal region (adjust Y as needed)
region_points = [(1075, 0), (1085, 0), (1085, 2000), (1075, 2000)]


# Video writer setup
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize object counter
counter = solutions.ObjectCounter(
    show=True,
    region=region_points,
    model="../models/yolo11n.pt",
    classes=[28],  # Specify class for counting, e.g., 'person'
    conf=0.5,  # Confidence threshold for counting
    show_in=True,
    show_out=True,
    tracker="bytetrack.yaml",
    line_width=3,
    verbose=True,
)

# Process video
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        break

    results = counter(im0)

    # Visualize region for debug
    cv2.polylines(im0, [np.array(region_points, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=2)
    

    # Optional debug logs
    print(f"In count: {results.in_count}")
    print(f"Out count: {results.out_count}")
    print(f"Total tracked: {results.total_tracks}")
    print(f"Classwise count: {results.classwise_count}")
    print(f"Region counts: {results.region_counts}")
    print(f"Queue count: {results.queue_count}")


    video_writer.write(results.plot_im)

cap.release()
video_writer.release()
cv2.destroyAllWindows()


# Convert saved .avi to .mp4
import os
import subprocess
avi_path = "object_counting_output.avi"
mp4_path = "object_counting_output.mp4"

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
