from ultralytics import YOLO
import torch
# Load a model
# model = YOLO("yolo11n-cls.pt")  # load an official model
model = YOLO("models/best (2).pt")


results= model.predict(source="data/digit9.jpg", save=False)  # save plotted images
# View results
for r in results:
    
    x=torch.argmax(r.probs.data)
    print("Predicted class:", x.item())
   