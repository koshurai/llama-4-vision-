import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import time

# Set page config with clean layout
st.set_page_config(
    page_title="NeuraVision AI",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal CSS with dark theme for results
def set_custom_css():
    st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
        }
        .stButton>button {
            background-color: #000000;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #333333;
        }
        .analysis-result {
            background-color: #000000;
            color: white;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
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
        return "Please provide your Groq API key."
    
    try:
        client = Groq(api_key=api_key)
        base64_image = encode_image_to_base64(image)

        with st.spinner('Analyzing image...'):
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
        return f"Error: {str(e)}"

# App layout
def main():
    st.title("NeuraVision AI")
    st.caption("Image analysis with Groq & LLaMA")
    
    api_key = st.text_input("Groq API Key", type="password")
    
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    prompt = st.text_area("Analysis Prompt", 
                        value="Describe this image in detail",
                        height=100)
    
    if st.button("Analyze Image"):
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=300)
            
            result = analyze_image(api_key, image, prompt)
            st.markdown("### Analysis Results")
            st.markdown(f"<div class='analysis-result'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload an image first.")

if __name__ == "__main__":
    main()
