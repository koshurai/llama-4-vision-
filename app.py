import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time

# Set page config for futuristic theme
st.set_page_config(
    page_title="NeuraVision AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic aesthetic
def set_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary-color: #00f2ff;
            --secondary-color: #ff00e6;
            --dark-bg: #0a0a1a;
            --darker-bg: #050510;
            --card-bg: rgba(15, 15, 35, 0.7);
        }
        
        body {
            background-color: var(--dark-bg);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);
        }
        
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: rgba(20, 20, 40, 0.8) !important;
            color: white !important;
            border: 1px solid var(--primary-color) !important;
        }
        
        .stButton>button {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            color: black !important;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px var(--primary-color);
        }
        
        .stMarkdown {
            color: white;
        }
        
        .sidebar .sidebar-content {
            background-color: var(--darker-bg);
            border-right: 1px solid rgba(0, 242, 255, 0.2);
        }
        
        h1, h2, h3 {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .card {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 3px solid var(--primary-color);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .glow {
            animation: glow 2s infinite alternate;
        }
        
        @keyframes glow {
            from {
                box-shadow: 0 0 5px var(--primary-color);
            }
            to {
                box-shadow: 0 0 20px var(--primary-color);
            }
        }
    </style>
    """, unsafe_allow_html=True)

set_custom_css()

# Encode image to base64
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Prediction function
def analyze_image(api_key, image, prompt):
    if not api_key:
        return "❌ Please provide your Groq API key."
    
    try:
        client = Groq(api_key=api_key)
        base64_image = encode_image_to_base64(image)

        with st.spinner('🌀 Processing image with quantum neural networks...'):
            time.sleep(1)  # For dramatic effect
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=1024,
            )
            return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# App layout
def main():
    st.title("🔮 NeuraVision AI")
    st.markdown("### Quantum-Powered Image Analysis with Groq & LLaMA 4 Scout")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container():
            st.markdown("### ⚙️ Configuration Panel")
            api_key = st.text_input("🔑 Groq API Key", type="password", help="Enter your Groq API key")
            
            uploaded_file = st.file_uploader("📸 Upload Image", type=["png", "jpg", "jpeg"], 
                                           help="Upload an image for analysis")
            
            prompt = st.text_area("💬 Analysis Prompt", 
                                 value="Describe this image in detail, including all important elements and their relationships.",
                                 height=150)
            
            if st.button("🚀 Analyze Image", use_container_width=True):
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    with col2:
                        with st.container():
                            st.markdown("### 🔍 Analysis Results")
                            st.image(image, caption="Uploaded Image", width=300)
                            
                            result = analyze_image(api_key, image, prompt)
                            st.markdown("### 📝 Insights")
                            st.markdown(f"<div class='card glow'>{result}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Please upload an image first.")
    
    with col2:
        if 'result' not in st.session_state:
            st.markdown("### 🔍 Analysis Results")
            st.markdown("""
            <div class='card'>
                <h4>Welcome to NeuraVision AI</h4>
                <p>Upload an image and provide a prompt to get started with quantum-powered analysis.</p>
                <p>Try prompts like:</p>
                <ul>
                    <li>"Describe this image in detail"</li>
                    <li>"What emotions does this image convey?"</li>
                    <li>"Analyze the composition and artistic elements"</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.image("https://via.placeholder.com/600x400/0a0a1a/00f2ff?text=Upload+an+Image", 
                    caption="Your analysis will appear here", width=400)

# Sidebar
with st.sidebar:
    st.markdown("## 🌌 Quantum Console")
    st.markdown("""
    <div class='card'>
        <p>System Status: <span style='color: var(--primary-color)'>Online</span></p>
        <p>Model: LLaMA 4 Scout 17B</p>
        <p>Processor: Quantum Core</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick Prompts")
    if st.button("Describe technically"):
        st.session_state.prompt = "Provide a detailed technical description of this image, including objects, colors, composition, and any notable features."
    
    if st.button("Analyze emotions"):
        st.session_state.prompt = "What emotions does this image convey? Describe the mood, atmosphere, and any emotional elements present."
    
    if st.button("Artistic critique"):
        st.session_state.prompt = "Provide an artistic critique of this image, discussing composition, color theory, lighting, and artistic merit."

if __name__ == "__main__":
    main()
