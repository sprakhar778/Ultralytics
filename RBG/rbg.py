from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

# Load model once
pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

def load_image(uploaded_file_or_url):
    if isinstance(uploaded_file_or_url, str):  # URL
        response = requests.get(uploaded_file_or_url)
        return Image.open(BytesIO(response.content)).convert("RGB")
    else:  # FileUpload from Streamlit
        return Image.open(uploaded_file_or_url).convert("RGB")

def get_result_image(image):
    result = pipe(image)  # Returns a PIL image directly
    return result

def save_image(img, filename):
    img.save(filename)
    return filename
