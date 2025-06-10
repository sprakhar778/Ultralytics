# from ultralytics import solutions

# solutions.ParkingPtsSelection()



import cv2

from ultralytics import solutions

# Video capture
cap = cv2.VideoCapture("../data/parking.mp4")
assert cap.isOpened(), "Error reading video file"

# Video writer
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("parking management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize parking management object
parkingmanager = solutions.ParkingManagement(
    show=True,  # display the output
    model="../models/yolo11n.pt",  # path to model file
    json_file="bounding_boxes.json",  # path to parking annotations file
    tracker="botsort.yaml",  # path to tracker configuration file
    classes=None
   
)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break

    results = parkingmanager(im0)

    # print(results)  # access the output

    video_writer.write(results.plot_im)  # write the processed frame.

cap.release()
video_writer.release()
cv2.destroyAllWindows()  # destroy all opened windows



# Convert to .mp4 (optional)
import os
import subprocess
avi_path = "parking management.avi"
mp4_path = "parking management.mp4"

if os.path.exists(avi_path):
    subprocess.run([
        "ffmpeg", "-i", avi_path,
        "-vcodec", "libx264", "-crf", "23", mp4_path
    ])
    print(f"Converted to MP4: {mp4_path}")
else:
    print("AVI file not found. Conversion skipped.")
