import os
import io
import streamlit as st
# pyrefly: ignore [missing-import]
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
# pyrefly: ignore [missing-import]
from rembg import remove, new_session

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="🇮🇳 Independence Day Photo Studio",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN LIGHT THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Elegant Light Canvas Background */
    .stApp {
        background: linear-gradient(135deg, #FAF8F5 0%, #FFF9F2 40%, #F2FAF5 100%);
        color: #0F172A;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(255, 247, 237, 0.95) 0%, #FFFFFF 50%, rgba(240, 253, 244, 0.95) 100%);
        border: 2px solid rgba(255, 103, 31, 0.25);
        border-radius: 20px;
        padding: 2rem 1.8rem;
        text-align: center;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 30px -5px rgba(255, 103, 31, 0.08), 0 8px 16px -4px rgba(22, 163, 74, 0.05);
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #E65100 0%, #06038D 50%, #15803D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #475569;
        font-size: 1.12rem;
        font-weight: 500;
        max-width: 680px;
        margin: 0 auto 1.2rem auto;
        line-height: 1.5;
    }

    .badge-pill-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    .badge-saffron {
        background: #FFF7ED;
        color: #C2410C;
        border: 1px solid #FDBA74;
    }

    .badge-blue {
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #93C5FD;
    }

    .badge-green {
        background: #F0FDF4;
        color: #15803D;
        border: 1px solid #86EFAC;
    }

    /* Clean Card Container */
    .studio-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
    }

    .section-heading {
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Primary Generate Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF671F 0%, #EA580C 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.8rem;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 8px 22px rgba(234, 88, 12, 0.3);
        transition: all 0.25s ease;
        width: 100%;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #FF7722 0%, #C2410C 100%);
        box-shadow: 0 12px 30px rgba(234, 88, 12, 0.45);
        transform: translateY(-2px);
        color: #FFFFFF !important;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #16A34A 0%, #15803D 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.25);
        transition: all 0.25s ease;
        width: 100%;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #22C55E 0%, #166534 100%);
        box-shadow: 0 10px 24px rgba(22, 163, 74, 0.35);
        transform: translateY(-2px);
        color: #FFFFFF !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #FAFAFA;
        border: 2px dashed #CBD5E1;
        border-radius: 14px;
        padding: 10px;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #FF671F;
        background: #FFF7ED;
    }

    /* Clean labels and typography */
    label, p, span {
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🇮🇳 Independence Day Photo Studio</div>
    <div class="hero-subtitle">
        Create beautiful, high-definition 15th August portraits in seconds with AI cutout and patriotic flag themes.
    </div>
    <div class="badge-pill-container">
        <span class="badge-pill badge-saffron">✨ Instant AI Cutout</span>
        <span class="badge-pill badge-blue">🏛️ HD National Flag Themes</span>
        <span class="badge-pill badge-green">👈 Move Left/Right & Fine-Tune</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CACHED MODEL SESSION ---
@st.cache_resource
def get_rembg_session():
    return new_session("u2net")

# --- BACKGROUND ASSETS LOADER ---
ASSETS_DIR = "assets"

def get_available_backgrounds():
    presets = {}
    preset_labels = {
        "independence.png": "🏛️ Heritage & Tricolor Sky",
        "indepedenceday.png": "🇮🇳 Independence Day Pride",
        "independece1.png": "🕊️ Freedom & National Flag",
        "happyindependence.png": "🎉 Festive Tiranga Poster"
    }
    
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                full_path = os.path.join(ASSETS_DIR, f)
                label = preset_labels.get(f, f"🎨 {f}")
                presets[label] = full_path
                
    return presets

preset_backgrounds = get_available_backgrounds()

# --- HIGH QUALITY COMPOSITOR ENGINE ---
def compose_photo(
    upload_file, 
    bg_image_source, 
    scale_pct=80, 
    x_pct=50, 
    y_pct=100, 
    flip_horizontal=False,
    brightness=1.0,
    contrast=1.0,
    saturation=1.0
):
    # 1. Open User Upload
    input_image = Image.open(upload_file)
    
    # 2. Extract Subject with AI
    session = get_rembg_session()
    subject_image = remove(input_image, session=session)
    
    # 3. Horizontal Flip (Mirror) if selected
    if flip_horizontal:
        subject_image = subject_image.transpose(Image.FLIP_LEFT_RIGHT)
        
    # 4. Lighting & Color Adjustments (Brightness, Contrast, Saturation)
    if brightness != 1.0 or contrast != 1.0 or saturation != 1.0:
        # Split RGB and Alpha
        if subject_image.mode == "RGBA":
            r, g, b, a = subject_image.split()
            rgb_img = Image.merge("RGB", (r, g, b))
            
            if brightness != 1.0:
                rgb_img = ImageEnhance.Brightness(rgb_img).enhance(brightness)
            if contrast != 1.0:
                rgb_img = ImageEnhance.Contrast(rgb_img).enhance(contrast)
            if saturation != 1.0:
                rgb_img = ImageEnhance.Color(rgb_img).enhance(saturation)
                
            r2, g2, b2 = rgb_img.split()
            subject_image = Image.merge("RGBA", (r2, g2, b2, a))
            
    # 5. Load Background Image
    if isinstance(bg_image_source, str):
        background = Image.open(bg_image_source).convert("RGBA")
    else:
        background = Image.open(bg_image_source).convert("RGBA")
        
    bg_width, bg_height = background.size
    subj_orig_width, subj_orig_height = subject_image.size
    
    # 6. Proportional Subject Scaling
    target_height = int(bg_height * (scale_pct / 100.0))
    scale_factor = target_height / max(subj_orig_height, 1)
    target_width = max(int(subj_orig_width * scale_factor), 1)
    
    subject_resized = subject_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 7. Smooth Placement Coordinates
    max_x = bg_width - target_width
    x_position = int(max_x * (x_pct / 100.0))
    
    max_y = bg_height - target_height
    y_position = int(max_y * (y_pct / 100.0))
    
    # 8. Composite Paste onto Background
    background.paste(subject_resized, (x_position, y_position), subject_resized)
    
    final_image = background.convert("RGB")
    return final_image

# --- STUDIO TWO-COLUMN WORKSPACE ---
col_controls, col_preview = st.columns([1.15, 1], gap="large")

with col_controls:
    # 1. STUDIO CONTROLS CONTAINER
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    
    # STEP 1: Upload Photo
    st.markdown('<div class="section-heading">📸 1. Upload Your Photo</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a portrait, selfie, or full-body photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="Clear photos with good lighting work best for clean AI cutouts."
    )
    
    st.markdown("---")
    
    # STEP 2: Background Selection
    st.markdown('<div class="section-heading">🇮🇳 2. Select Patriotic Background</div>', unsafe_allow_html=True)
    
    bg_mode = st.radio(
        "Background Source:",
        ["HD Presets Gallery", "Upload Custom Background"],
        horizontal=True
    )
    
    selected_bg_path = None
    custom_bg_file = None
    
    if bg_mode == "HD Presets Gallery":
        if preset_backgrounds:
            preset_labels_list = list(preset_backgrounds.keys())
            chosen_preset = st.selectbox("Choose Background Theme:", preset_labels_list, index=0)
            selected_bg_path = preset_backgrounds[chosen_preset]
            st.image(selected_bg_path, use_container_width=True)
        else:
            st.warning("No background presets found in `assets/` folder.")
    else:
        custom_bg_file = st.file_uploader(
            "Upload your custom flag or background image",
            type=["jpg", "jpeg", "png", "webp"],
            key="custom_bg_uploader"
        )
        if custom_bg_file:
            st.image(custom_bg_file, caption="Custom Background Preview", use_container_width=True)
            
    st.markdown("---")
    
    # STEP 3: Move & Position Photo
    st.markdown('<div class="section-heading">⚙️ 3. Move & Adjust Position</div>', unsafe_allow_html=True)
    
    # Left / Center / Right Quick Preset Buttons
    pos_btn_col1, pos_btn_col2, pos_btn_col3 = st.columns(3)
    if 'h_pos_val' not in st.session_state:
        st.session_state['h_pos_val'] = 50
        
    with pos_btn_col1:
        if st.button("👈 Left (20%)", key="btn_left"):
            st.session_state['h_pos_val'] = 20
    with pos_btn_col2:
        if st.button("🎯 Center (50%)", key="btn_center"):
            st.session_state['h_pos_val'] = 50
    with pos_btn_col3:
        if st.button("👉 Right (80%)", key="btn_right"):
            st.session_state['h_pos_val'] = 80
            
    # Continuous Horizontal Slider
    h_pos_pct = st.slider(
        "Move Photo Left ↔ Right (0% = Far Left, 50% = Center, 100% = Far Right)",
        min_value=0,
        max_value=100,
        value=st.session_state['h_pos_val'],
        step=1
    )
    st.session_state['h_pos_val'] = h_pos_pct
    
    # Vertical Placement & Size
    pos_row1, pos_row2 = st.columns(2)
    with pos_row1:
        v_align_choice = st.selectbox(
            "Vertical Position:",
            ["⬇️ Bottom (Standing on ground)", "🎯 Center (Floating)", "⬆️ Top"],
            index=0
        )
        v_pos_pct = 100 if "Bottom" in v_align_choice else (50 if "Center" in v_align_choice else 10)
    with pos_row2:
        scale_val = st.slider("🔍 Subject Size (%)", min_value=35, max_value=115, value=80, step=5)
        
    flip_photo = st.checkbox("🔄 Flip / Mirror Photo Horizontally", value=False, help="Makes your photo face the opposite direction.")
    
    # STEP 4: Optional Lighting & Tuning (Collapsible)
    with st.expander("🎨 Studio Lighting & Color Blend (Optional)", expanded=False):
        b_col, c_col, s_col = st.columns(3)
        with b_col:
            bright_val = st.slider("Brightness", 0.7, 1.3, 1.0, 0.05)
        with c_col:
            contrast_val = st.slider("Contrast", 0.7, 1.3, 1.0, 0.05)
        with s_col:
            satur_val = st.slider("Vibrance", 0.7, 1.4, 1.0, 0.05)
            
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    # 2. OUTPUT & PREVIEW CONTAINER
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">✨ Studio Canvas & Generation</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown("**Uploaded Photo:**")
        st.image(uploaded_file, width=200)
        
        ready_to_generate = (bg_mode == "HD Presets Gallery" and selected_bg_path is not None) or (bg_mode == "Upload Custom Background" and custom_bg_file is not None)
        
        if ready_to_generate:
            if st.button("🚀 Generate Independence Day Photo", use_container_width=True):
                with st.spinner("🇮🇳 Removing background and composing with Indian Flag..."):
                    bg_source = selected_bg_path if bg_mode == "HD Presets Gallery" else custom_bg_file
                    
                    try:
                        result_image = compose_photo(
                            uploaded_file,
                            bg_source,
                            scale_pct=scale_val,
                            x_pct=h_pos_pct,
                            y_pct=v_pos_pct,
                            flip_horizontal=flip_photo,
                            brightness=bright_val if 'bright_val' in locals() else 1.0,
                            contrast=contrast_val if 'contrast_val' in locals() else 1.0,
                            saturation=satur_val if 'satur_val' in locals() else 1.0
                        )
                        
                        st.session_state['generated_image'] = result_image
                        st.balloons()
                        st.success("🎉 Photo generated successfully!")
                    except Exception as err:
                        st.error(f"Error during photo generation: {err}")
        else:
            st.info("ℹ️ Please select or upload a background image on the left.")
    else:
        st.info("👋 Upload your photo in Step 1 to begin.")
        
    # Result & Download
    if 'generated_image' in st.session_state and st.session_state['generated_image'] is not None:
        st.markdown("---")
        st.markdown("### 🏆 Your Finished Portrait")
        st.image(st.session_state['generated_image'], caption="Happy Independence Day 🇮🇳", use_container_width=True)
        
        dl_col1, dl_col2 = st.columns(2)
        
        # High Quality JPEG
        jpeg_buf = io.BytesIO()
        st.session_state['generated_image'].save(jpeg_buf, format='JPEG', quality=95)
        
        with dl_col1:
            st.download_button(
                label="📥 Download HD JPEG",
                data=jpeg_buf.getvalue(),
                file_name="Independence_Day_Portrait.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
            
        # Lossless PNG
        png_buf = io.BytesIO()
        st.session_state['generated_image'].save(png_buf, format='PNG')
        
        with dl_col2:
            st.download_button(
                label="📥 Download HD PNG",
                data=png_buf.getvalue(),
                file_name="Independence_Day_Portrait.png",
                mime="image/png",
                use_container_width=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)