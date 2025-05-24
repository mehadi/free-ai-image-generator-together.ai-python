import streamlit as st
from api_client import TogetherAIClient
from image_handler import ImageHandler
import os
import random

# List of creative placeholder prompts
PLACEHOLDER_PROMPTS = [
    "A serene landscape with a magical forest at sunset, ethereal lighting, digital art style",
    "A futuristic cityscape with flying cars and neon lights, cyberpunk aesthetic",
    "A cute robot playing with a cat in a cozy living room, warm lighting",
    "An underwater scene with bioluminescent creatures, mystical atmosphere",
    "A steampunk-inspired airship floating through clouds, detailed mechanical parts",
    "A peaceful Japanese garden with cherry blossoms, traditional art style",
    "A fantasy castle floating in the sky, surrounded by clouds and rainbows",
    "A cozy cafe interior with steam rising from coffee cups, soft lighting",
    "A space station orbiting a colorful nebula, sci-fi style",
    "A magical library with floating books and glowing orbs, fantasy atmosphere"
]

# Initialize session state
if 'api_client' not in st.session_state:
    st.session_state.api_client = TogetherAIClient()
if 'image_handler' not in st.session_state:
    st.session_state.image_handler = ImageHandler()
if 'placeholder_prompt' not in st.session_state:
    st.session_state.placeholder_prompt = random.choice(PLACEHOLDER_PROMPTS)

# Set page config with custom theme
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    /* Main background and container styles */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Button styles */
    .stButton>button {
        background-color: #6366f1;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
    }
    .stButton>button:hover {
        background-color: #4f46e5;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
    }
    
    /* Input field styles */
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        background-color: white;
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Select box styles */
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        background-color: white;
    }
    
    /* Text styles */
    .stMarkdown {
        color: #1e293b;
    }
    .stHeader {
        color: #0f172a;
    }
    
    /* Card styles */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* Success message styles */
    .stSuccess {
        background-color: #dcfce7;
        color: #166534;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Error message styles */
    .stError {
        background-color: #fee2e2;
        color: #991b1b;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Info message styles */
    .stInfo {
        background-color: #dbeafe;
        color: #1e40af;
        border-radius: 8px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description with modern styling
st.markdown("""
    <div style='text-align: center; padding: 30px; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 30px;'>
        <h1 style='color: #0f172a; font-size: 2.5em; margin-bottom: 15px; font-weight: 700;'>🎨 AI Image Generator</h1>
        <p style='color: #475569; font-size: 1.2em;'>Create stunning images using Together.ai's Stable Diffusion model</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for settings with improved organization
with st.sidebar:
    st.markdown("""
        <div style='padding: 20px; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px;'>
            <h2 style='color: #0f172a; margin-bottom: 20px; font-weight: 600;'>⚙️ Settings</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Model selection
    st.markdown("### 🎯 Model")
    model = st.selectbox(
        "Select Model",
        ["black-forest-labs/FLUX.1-schnell-Free"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Image parameters in collapsible sections
    with st.expander("📐 Image Size", expanded=True):
        width = st.slider("Width", min_value=512, max_value=1024, value=576, step=64)
        height = st.slider("Height", min_value=512, max_value=1024, value=1024, step=64)
    
    with st.expander("⚡ Generation Settings", expanded=True):
        steps = st.slider("Steps", min_value=1, max_value=50, value=4, step=1)
        seed = st.number_input("Seed", min_value=-1, max_value=2147483647, value=42)
    
    with st.expander("🔧 Advanced Settings", expanded=False):
        negative_prompt = st.text_area(
            "Negative Prompt",
            height=100,
            help="Specify what you don't want in the image",
            placeholder="Enter elements to exclude from the image..."
        )

# Main content area with modern layout
st.markdown("""
    <div style='background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);'>
""", unsafe_allow_html=True)

# Prompt input with improved styling
st.markdown("### ✍️ Enter your prompt")
prompt = st.text_area(
    "Enter your prompt",
    height=100,
    placeholder=st.session_state.placeholder_prompt,
    label_visibility="collapsed"
)

# Generate button with loading state
generate_button = st.button("🎨 Generate Image", use_container_width=True)

if generate_button and prompt:
    with st.spinner("🎨 Creating your masterpiece..."):
        try:
            # Generate image with parameters
            image = st.session_state.api_client.generate_image(
                prompt=prompt,
                model=model,
                width=width,
                height=height,
                steps=steps,
                seed=seed,
                negative_prompt=negative_prompt if negative_prompt else None
            )
            
            # Save image
            filepath = st.session_state.image_handler.save_image(image, prompt)
            
            # Display image with modern styling
            st.markdown("### 🖼️ Generated Image")
            st.image(image, caption=prompt, use_column_width=True)
            
            # Success message with modern styling
            st.success("✨ Image generated successfully!")
            st.info(f"💾 Saved at: {filepath}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# Gallery section with modern styling
st.markdown("""
    <div style='margin-top: 40px;'>
        <h2 style='color: #0f172a; margin-bottom: 25px; font-weight: 600;'>🖼️ Generated Images</h2>
    </div>
""", unsafe_allow_html=True)

saved_images = st.session_state.image_handler.get_saved_images()

if saved_images:
    # Create a grid layout for the gallery
    num_cols = 3
    cols = st.columns(num_cols)
    
    # Sort images by creation time (newest first)
    saved_images.sort(reverse=True)
    
    for idx, image_name in enumerate(saved_images):
        image_path = os.path.join(st.session_state.image_handler.save_dir, image_name)
        with cols[idx % num_cols]:
            # Create a container for each image with modern styling
            st.markdown("""
                <div style='background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 25px; border: 1px solid #e2e8f0;'>
            """, unsafe_allow_html=True)
            
            # Display image with controlled size
            st.image(
                image_path,
                caption=image_name,
                use_column_width=True
            )
            
            # Add a download button with modern styling
            with open(image_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download",
                    data=file,
                    file_name=image_name,
                    mime="image/png",
                    key=f"download_{idx}",
                    use_container_width=True
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("🎨 No images generated yet. Start by entering a prompt above!") 