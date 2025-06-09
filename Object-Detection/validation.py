from ultralytics import YOLO
model= YOLO("models/best.pt")  # load a pretrained model (recommended for training)
metrics = model.val(data="path_of_dataset", imgsz=640, batch=16, conf=0.25, iou=0.6)