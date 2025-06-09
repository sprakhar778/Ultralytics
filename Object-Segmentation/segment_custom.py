from ultralytics import YOLO

# Load a model
model = YOLO("models/best (1).pt")  # load an official model
# model = YOLO("path/to/best.pt")  # load a custom model

# Predict with the model
result=model.predict(source=0,show=True)
# results = model("data/bus.jpg",show=True,save=True,stream=True)  # predict on an image

# # Access the results
# for result in results:
#     xy = result.masks.xy  # mask in polygon format
#     xyn = result.masks.xyn  # normalized
#     masks = result.masks.data  # mask in matrix format (num_objects x H x W)
