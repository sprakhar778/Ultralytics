from ultralytics import YOLO

# Load a pretrained YOLO11n model
def predict(model, source):
    model = YOLO(model)

    # Define source as YouTube video URL
  
    # Run inference on the source
    results = model(source, stream=True,show=True)  # generator of Results objects
    return results


source = "data/signature_example1.jpeg"
model="models/best.pt"
results =predict(model, source)

for result in results:
    result.show()  # display the results in a window

