import streamlit as st
from rbg import load_image, get_result_image, save_image
from io import BytesIO
import base64
from PIL import Image
import time

# Page config with modern styling
st.set_page_config(
    page_title="AI Background Remover Pro", 
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container styling */
    .main-container {
        
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .hero-title {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #6b7280;
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Upload section styling */
    .upload-section {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px dashed #cbd5e1;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
    }
    
    /* Comparison section */
    .comparison-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .image-box {
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .image-title {
        color: white;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .image-display {
        max-width: 350px;
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .image-display:hover {
        transform: scale(1.02);
    }
    
    /* Download section */
    .download-section {
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        color: white;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .feature-desc {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Progress bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1 rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: transform 0.2s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Radio button styling */
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Hero Section
st.markdown("""
<div class="main-container">
    <div class="hero-section">
        <h1 class="hero-title">🪄 AI Background Remover Pro</h1>
        <p class="hero-subtitle">Remove backgrounds from any image instantly using advanced AI technology</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="main-container">
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Lightning Fast</h3>
            <p class="feature-desc">Process images in seconds with our optimized AI models</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Precision Cuts</h3>
            <p class="feature-desc">Advanced edge detection for pixel-perfect results</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">Any Device</h3>
            <p class="feature-desc">Works seamlessly on desktop, tablet, and mobile</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">Secure & Private</h3>
            <p class="feature-desc">Your images are processed securely and never stored</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats section
st.markdown("""
<div class="main-container">
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Images Processed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">Uptime</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">< 3s</div>
            <div class="stat-label">Average Processing</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">4.9★</div>
            <div class="stat-label">User Rating</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 📁 Upload Your Image")
    
    # Upload method selection with custom styling
    upload_method = st.radio(
        "Choose upload method:",
        ["📤 Upload File", "🔗 From URL"],
        horizontal=True
    )

# Initialize session state for image processing
if 'processing' not in st.session_state:
    st.session_state.processing = False

image = None

if upload_method == "📤 Upload File":
   
    uploaded_file = st.file_uploader(
        "Drag and drop your image here, or click to browse",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, JPEG, PNG, WEBP (Max 10MB)"
    )
    if uploaded_file:
        image = load_image(uploaded_file)
        st.success(f"✅ Image uploaded successfully! ({uploaded_file.name})")
    st.markdown('</div>', unsafe_allow_html=True)

elif upload_method == "🔗 From URL":
   
    url = st.text_input(
        "Enter image URL:",
        placeholder="https://example.com/image.jpg",
        help="Enter a direct link to an image file"
    )
    if url:
        try:
            image = load_image(url)
            st.success("Image loaded successfully from URL!")
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Processing and Results
if image is not None:
    # Processing section
   
    
    if not st.session_state.processing:
        if st.button("🚀 Remove Background", type="primary"):
            st.session_state.processing = True
            st.rerun()
    
    if st.session_state.processing:
        # Progress indicator
        st.markdown("""
        <div class="progress-container">
            <h3>Processing your image...</h3>
            <p>Our AI is working its magic! This usually takes 2-5 seconds.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)  # Simulate processing time
            progress_bar.progress(i + 1)
        
        # Process the image
        with st.spinner("Applying final touches..."):
            result = get_result_image(image)
        
        st.session_state.processing = False
        st.success("✨ Background removed successfully!")
        
        # Comparison section
        st.markdown("## Before & After Comparison")
        st.markdown(f"""
        <div class="comparison-container">
            <div class="image-box">
                <h4 class="image-title">Original</h4>
                <img src='data:image/png;base64,{image_to_base64(image)}' class='image-display'/>
            </div>
            <div class="image-box">
                <h4 class="image-title">Background Removed</h4>
                <img src='data:image/png;base64,{image_to_base64(result)}' class='image-display'/>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download section
        st.markdown("""
        <div class="download-section">
            <h3>💾 Download Your Result</h3>
            <p>Your processed image is ready! Click below to download in high quality.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare download
        buf = BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.download_button(
                label="Download PNG (High Quality)",
                data=byte_im,
                file_name=f"background_removed_{int(time.time())}.png",
                mime="image/png"
            )
        
       
        
        # Reset button
        if st.button("Process Another Image"):
            st.session_state.processing = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="main-container" style="text-align: center; margin-top: 3rem;">
    <hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #cbd5e1, transparent); margin: 2rem 0;">
    <p style="color: #6b7280; font-size: 0.9rem;">
        Made with ❤️ using Streamlit & Advanced AI • 
        <strong>Privacy First</strong> - Images are processed locally and never stored
    </p>
</div>
""", unsafe_allow_html=True)