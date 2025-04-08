import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time

# Set page config for cyberpunk theme
st.set_page_config(
    page_title="NEURAVISION 2.0",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cyberpunk CSS styling
def set_custom_css():
    st.markdown("""
    <style>
        :root {
            --neon-blue: #0ff0fc;
            --neon-pink: #ff2a6d;
            --neon-purple: #d300c5;
            --dark-bg: #0a0a12;
            --darker-bg: #050508;
            --cyber-yellow: #f8f800;
        }
        
        body {
            background-color: var(--dark-bg);
            color: #e0e0e0;
            font-family: 'Courier New', monospace;
        }
        
        .stApp {
            background: radial-gradient(circle at center, var(--darker-bg) 0%, var(--dark-bg) 100%);
        }
        
        /* Input fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: rgba(10, 10, 20, 0.8) !important;
            color: var(--neon-blue) !important;
            border: 1px solid var(--neon-pink) !important;
            border-radius: 0 !important;
            font-family: 'Courier New', monospace;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, var(--neon-pink), var(--neon-purple));
            color: black !important;
            font-weight: bold;
            border: none;
            border-radius: 0;
            padding: 0.5rem 1rem;
            font-family: 'Courier New', monospace;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 15px var(--neon-pink);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--neon-blue);
            text-shadow: 0 0 10px rgba(15, 240, 252, 0.5);
            letter-spacing: 2px;
            border-bottom: 1px solid var(--neon-pink);
            padding-bottom: 5px;
        }
        
        /* Analysis result box */
        .analysis-result {
            background-color: rgba(15, 15, 35, 0.7);
            border-left: 3px solid var(--neon-blue);
            color: #ffffff;
            padding: 1.5rem;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            box-shadow: 0 0 20px rgba(15, 240, 252, 0.2);
            border-radius: 0;
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: var(--darker-bg);
            border-right: 1px solid var(--neon-purple);
        }
        
        /* Glowing effect */
        .glow {
            animation: glow 2s infinite alternate;
        }
        
        @keyframes glow {
            from {
                box-shadow: 0 0 5px var(--neon-blue);
            }
            to {
                box-shadow: 0 0 20px var(--neon-blue);
            }
        }
        
        /* Cyberpunk terminal effect */
        .terminal {
            background-color: black;
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            padding: 1rem;
            font-family: 'Courier New', monospace;
            position: relative;
        }
        
        .terminal::before {
            content: ">";
            position: absolute;
            left: 10px;
            color: var(--neon-pink);
        }
        
        /* Scanlines overlay */
        .scanlines {
            position: relative;
        }
        
        .scanlines::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                rgba(0, 255, 255, 0.03) 1px,
                transparent 1px
            );
            background-size: 100% 2px;
            pointer-events: none;
        }
    </style>
    """, unsafe_allow_html=True)

set_custom_css()

# Encode image to base64
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Prediction function with cyberpunk loading effect
def analyze_image(api_key, image, prompt):
    if not api_key:
        return "❌ ERROR: API KEY REQUIRED"
    
    try:
        client = Groq(api_key=api_key)
        base64_image = encode_image_to_base64(image)

        with st.empty():
            for i in range(3):
                st.markdown(f"<div class='terminal'>INITIALIZING NEURAL SCAN{'...'[:i+1]}</div>", unsafe_allow_html=True)
                time.sleep(0.5)
            
            st.markdown("<div class='terminal'>CONNECTING TO QUANTUM CORE...</div>", unsafe_allow_html=True)
            time.sleep(0.7)
            
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
            return f"▲▲ ANALYSIS COMPLETE ▲▲\n\n{response.choices[0].message.content}"
    
    except Exception as e:
        return f"⚠️ SYSTEM ERROR: {str(e)}"

# App layout
def main():
    st.title("〄 NEURAVISION 2.0")
    st.image('blob.png',width=300)
    st.markdown("### QUANTUM IMAGE DECODER // GROQ-LLaMA INTEGRATION")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container():
            st.markdown("### ⚡ CONTROL PANEL")
            api_key = st.text_input("〄 ENTER API KEY", type="password", help="Access token required for quantum neural network")
            
            uploaded_file = st.file_uploader("⇧ UPLOAD IMAGE DATA", type=["png", "jpg", "jpeg"])
            
            prompt = st.text_area("✎ ANALYSIS PROMPT", 
                                 value="Conduct full spectrum analysis of this image. Include technical, emotional, and compositional assessment.",
                                 height=150)
            
            if st.button("⟳ INITIATE SCAN", use_container_width=True):
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    with col2:
                        with st.container():
                            st.markdown("### ⟠ SCAN RESULTS")
                            st.image(image, caption="INPUT RECEIVED", width=350)
                            
                            result = analyze_image(api_key, image, prompt)
                            st.markdown("### ⚡ DECODED ANALYSIS")
                            st.markdown(f"<div class='analysis-result scanlines'>{result}</div>", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ NO IMAGE DATA DETECTED")

# Cyberpunk sidebar
with st.sidebar:
    st.markdown("## 〄 SYSTEM MONITOR")
    st.markdown("""
    <div class='terminal scanlines' style='margin-bottom: 20px;'>
        SYSTEM STATUS: ONLINE<br>
        MODEL: LLaMA-4 SCOUT 17B<br>
        PROCESSOR: QUANTUM CORE v2.3<br>
        TEMP: 34.7°C<br>
        MEM: 87% LOADED
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ QUICK SCAN PROTOCOLS")
    if st.button("TECHNICAL ANALYSIS"):
        st.session_state.prompt = "Provide detailed technical breakdown including objects, colors, composition, and metadata patterns."
    
    if st.button("EMOTIONAL PROFILE"):
        st.session_state.prompt = "Analyze emotional resonance. Describe mood, atmosphere, and psychological impact with confidence percentages."
    
    if st.button("ARTISTIC DECONSTRUCTION"):
        st.session_state.prompt = "Deconstruct artistic elements including composition theory, color harmonics, and creative execution quality."

if __name__ == "__main__":
    main()
