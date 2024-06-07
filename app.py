from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini Pro Vision model
def get_cosmic_vision_response(input_text, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Function to get response from Gemini Pro model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Main content
st.sidebar.title("🌟 CosmicAI: Explore Infinite Possibilities")

model_option = st.sidebar.radio("", ("📝 Text Insights", "🖼️ Visual Explorer"))

# Create a session state to persist chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a section to display chat history
history_expander = st.sidebar.expander("Chat History", expanded=False)

if model_option == "📝 Text Insights":
    st.header("📝 Text Insights")
    input_text = st.text_input("💬 Enter your question or prompt:", key="input_gemini_pro")
    if st.button("🔬 Analyze"):
        if input_text:
            response = get_gemini_response(input_text)
            st.write("**You:**", input_text)
            st.write("**CosmicAI:**", response)
            st.session_state.chat_history.append(("You", input_text))
            st.session_state.chat_history.append(("CosmicAI", response))
        else:
            st.warning("⚠️ Please enter a question or prompt.")
elif model_option == "🖼️ Visual Explorer":
    st.header("🖼️ Visual Explorer")
    input_text = st.text_input("💬 Enter your prompt or question:", key="input_cosmic_vision")
    uploaded_file = st.file_uploader("📁 Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Uploaded Image.", use_column_width=True)
    else:
        image = None
    if st.button("🔬 Analyze"):
        if image:
            response = get_cosmic_vision_response(input_text, image)
            st.write("**You:**", input_text)
            st.write("**CosmicAI:**", response)
            st.session_state.chat_history.append(("You", input_text))
            st.session_state.chat_history.append(("CosmicAI", response))
        else:
            st.warning("⚠️ Please upload an image.")

# Display chat history
with history_expander:
    if len(st.session_state.chat_history) > 0:
        for sender, message in st.session_state.chat_history:
            st.write(f"**{sender}:** {message}")
    else:
        st.write("Chat history is empty.")
