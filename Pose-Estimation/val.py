from ultralytics import YOLO

# Load a model
model = YOLO("models/yolo11n-pose.pt")  # load an official model
# model = YOLO("path/to/best.pt")  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps  # a list contains map50-95 of each category
metrics.pose.map  # map50-95(P)
metrics.pose.map50  # map50(P)
metrics.pose.map75  # map75(P)
metrics.pse.maps  # a list contains map50-95(P) of each category