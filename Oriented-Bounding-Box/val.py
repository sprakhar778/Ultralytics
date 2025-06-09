from ultralytics import YOLO

# Load a model
model = YOLO("models/yolo11n-obb.pt")  # load an official model

# Validate the model
metrics = model.val(data="dota8.yaml")  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95(B)
metrics.box.map50  # map50(B)
metrics.box.map75  # map75(B)
metrics.box.maps  # a list contains map50-95(B) of each category