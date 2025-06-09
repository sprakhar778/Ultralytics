# from ultralytics import YOLO

# # Load a model
# model = YOLO("models/yolo11n-seg.pt")  # load an official model
# # model = YOLO("path/to/best.pt")  # load a custom model

# # Predict with the model
# results = model("data/bus.jpg",show=True,save=True,stream=True,show_boxes=False,show_labels=True)  # predict on an image

# # Access the results
# for result in results:
#     xy = result.masks.xy  # mask in polygon format
#     xyn = result.masks.xyn  # normalized
#     masks = result.masks.data  # mask in matrix format (num_objects x H x W)


from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load YOLO segmentation model
model = YOLO("models/best (1).pt")

# Generate colors
def generate_bright_colors(n):
    """
    Generate n vibrant, visually distinct colors in BGR format
    using HSV color space.
    """
    colors = []
    for i in range(n):
        hue = int(180 * i / n)  # OpenCV Hue range: 0-179
        saturation = 230        # Max 255, high saturation for vibrancy
        value = 242             # Max 255, high brightness
        hsv_pixel = np.uint8([[[hue, saturation, value]]])
        bgr_pixel = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)[0][0]
        colors.append((int(bgr_pixel[0]), int(bgr_pixel[1]), int(bgr_pixel[2])))
    return colors

# Create color map
num_classes = len(model.names)
class_colors = {
    i: color for i, color in enumerate(generate_bright_colors(num_classes))
}

# Predict
results = model("data/bus.jpg", stream=True, conf=0.5)

for result in results:
    img = result.orig_img.copy()

    if result.masks is None:
        print("No masks found.")
        continue

    masks = result.masks.data.cpu().numpy()
    classes = result.boxes.cls.cpu().numpy().astype(int)

    for i, mask in enumerate(masks):
        class_id = classes[i]
        color = class_colors[class_id]

        # Resize mask to image size
        mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))
        mask_img = (mask_resized * 255).astype(np.uint8)
        mask_bool = mask_img > 127

        # Create color mask and overlay
        colored_mask = np.zeros_like(img, dtype=np.uint8)
        colored_mask[mask_bool] = color
        overlay = cv2.addWeighted(img, 0.5, colored_mask, 0.5, 0)
        img = np.where(mask_bool[..., None], overlay, img)

        # Put class label
        ys, xs = np.nonzero(mask_bool)
        if len(xs) and len(ys):
            cx, cy = int(xs.mean()), int(ys.mean())
            label = model.names[class_id]
            cv2.putText(img, label, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)

    # Save and Show
    cv2.imwrite("output_segmentation.png", img)
    print("Saved to output_segmentation.png")
    cv2.imshow("Segmentation", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
