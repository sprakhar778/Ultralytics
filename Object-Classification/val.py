from ultralytics import YOLO

# # Load a model
# model = YOLO("yolo11n-cls.pt")  # load an official model
model = YOLO("models/best (2).pt")
# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.top1  # top1 accuracy
metrics.top5  # top5 accuracy