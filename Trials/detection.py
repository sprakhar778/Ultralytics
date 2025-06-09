import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolov8m.pt")


# from PIL
im1 = Image.open("test.png")
results = model.predict(source=im1, save=True)  # save plotted images

# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam

# results = model.predict(source=0 ,show=True)