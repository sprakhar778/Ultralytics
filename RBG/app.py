import streamlit as st
from rbg import load_image, get_result_image, save_image
from io import BytesIO

st.set_page_config(page_title="Background Remover", layout="centered")
st.title("🪄 AI Background Remover")
# Helper function to convert image to base64 for HTML rendering
import base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Upload or provide URL
upload_method = st.radio("Upload Image via:", ["Upload", "URL"])
if upload_method == "Upload":
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = load_image(uploaded_file)
elif upload_method == "URL":
    url = st.text_input("Enter image URL")
    if url:
        image = load_image(url)

if "image" in locals():
    # Run model
    with st.spinner("Removing background..."):
        result = get_result_image(image)

    # Style container box for side-by-side display
    st.markdown("### 🎭 Comparison")
    st.markdown("""
    <div style='display: flex; justify-content: center; gap: 40px; padding: 20px; border: 2px solid #ccc; border-radius: 12px; background-color: #000000    '>
        <div>
            <h4 style='text-align: center'>Original</h4>
            <img src='data:image/png;base64,{}' style='max-width: 300px; border-radius: 10px;'/>
        </div>
        <div>
            <h4 style='text-align: center'>Background Removed</h4>
            <img src='data:image/png;base64,{}' style='max-width: 300px; border-radius: 10px;'/>
        </div>
    </div>
    """.format(
        image_to_base64(image),
        image_to_base64(result)
    ), unsafe_allow_html=True)

    # Download section
    st.markdown("### 💾 Download Output")
    buf = BytesIO()
    result.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Background Removed Image",
        data=byte_im,
        file_name="background_removed.png",
        mime="image/png"
    )


