from ultralytics import YOLO
import cv2
import numpy as np
import os
import subprocess
import shutil

# Load the segmentation model
model = YOLO("models/yolo11n-seg.pt")

# Set confidence threshold
CONF_THRESH = 0.7

# Get video properties from the source
input_path = "data/airport.mp4"
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"Error: Could not open video file {input_path}")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()

print(f"Video properties: {width}x{height} @ {fps:.2f}fps, Total frames: {total_frames}")

# Create output directory for frames
output_dir = os.path.join(os.getcwd(), "masked_frames")
os.makedirs(output_dir, exist_ok=True)
print(f"Frames will be saved in: {output_dir}")

# Perform tracking with segmentation
results = model.track(source=input_path, stream=True, show=False, persist=True)

frame_count = 0
cv2.namedWindow("High Confidence Person Segments", cv2.WINDOW_NORMAL)
cv2.resizeWindow("High Confidence Person Segments", 800, 600)

for result in results:
    frame_count += 1
    frame = result.orig_img.copy()
    masked_frame = np.zeros_like(frame)
    masks_applied = False

    if result.masks is not None and result.boxes is not None:
        masks = result.masks.data.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)
        confs = result.boxes.conf.cpu().numpy()
        names = model.names

        for i in range(len(masks)):
            cls_name = names[classes[i]]
            conf = confs[i]

            if cls_name == "person" and conf > CONF_THRESH:
                masks_applied = True
                binary_mask = masks[i]
                binary_mask = cv2.resize(binary_mask, (frame.shape[1], frame.shape[0]))
                binary_mask = (binary_mask > 0.5).astype(np.uint8)
                
                # Apply mask using bitwise operations
                person_roi = cv2.bitwise_and(frame, frame, mask=binary_mask)
                masked_frame = cv2.add(masked_frame, person_roi)

    # Save frame as image
    frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
    cv2.imwrite(frame_path, masked_frame)
    
    # Show final masked frame
    cv2.imshow("High Confidence Person Segments", masked_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Print progress
    if frame_count % 10 == 0:
        print(f"Processed frame {frame_count}/{total_frames}")

cv2.destroyAllWindows()

# Convert frames to video using FFmpeg
output_video_path = os.path.join(os.getcwd(), "output_masked.mp4")
ffmpeg_command = [
    'ffmpeg',
    '-y',  # Overwrite output file without asking
    '-framerate', str(fps),
    '-i', os.path.join(output_dir, 'frame_%06d.jpg'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '23',
    '-preset', 'fast',
    output_video_path
]

print("Converting frames to video using FFmpeg...")
print(" ".join(ffmpeg_command))
video_created = False
try:
    subprocess.run(ffmpeg_command, check=True)
    print(f"Successfully created video: {output_video_path}")
    video_created = True

except subprocess.CalledProcessError as e:
    print(f"FFmpeg conversion failed: {e}")
    print("You can manually convert the frames using:")
    print(f"ffmpeg -framerate {fps} -i {output_dir}/frame_%06d.jpg -c:v libx264 -pix_fmt yuv420p {output_video_path}")
except FileNotFoundError:
    print("FFmpeg not found. Please install FFmpeg to convert frames to video.")
    print("You can download it from: https://ffmpeg.org/download.html")

# Delete frames if video was successfully created
if video_created and os.path.exists(output_dir):
    try:
        shutil.rmtree(output_dir)
        print(f"Deleted temporary frames directory: {output_dir}")
    except Exception as e:
        print(f"Error deleting frames directory: {e}")

print("Processing complete")