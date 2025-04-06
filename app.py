import streamlit as st
import google.generativeai as genai
import base64
from io import BytesIO
import datetime
from streamlit_autorefresh import st_autorefresh
import time

# Initialize timer if not already set
if "time_left" not in st.session_state:
    st.session_state.time_left = 60 * 60  # 60 minutes in seconds
if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()
if "test_mode" not in st.session_state:
    st.session_state.test_mode = False

# Test screen with timer and Exit button
if st.session_state.test_mode:
    # Refresh every 1 second (1000 milliseconds)
    st_autorefresh(interval=1000, key="timer_refresh")

    st.markdown("<style>body { background-color: white; }</style>", unsafe_allow_html=True)

    # Calculate time difference since last tick
    now = time.time()
    elapsed = now - st.session_state.last_tick
    st.session_state.last_tick = now
  st.session_state.time_left = max(0, st.session_state.time_left - round(elapsed))


    # Format and display timer
    mins, secs = divmod(st.session_state.time_left, 60)
    st.markdown(f"## ⏳ Time Left: {mins:02d}:{secs:02d}")

    # Exit button
    if st.button("Exit", key="exit_button"):
        st.session_state.test_mode = False
        st.session_state.time_left = 60 * 60  # Reset for next time
        st.session_state.last_tick = time.time()
        st.rerun()

    st.stop()

# Configure the API key
genai.configure(api_key="AIzaSyBlwWjOEN6daKjcUWj2Nh5AVE9ACOavLag")

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Read the base prompt from a file
try:
    with open("base_prompt.txt", "r", encoding="utf-8") as file:
        base_prompt = file.read()
except FileNotFoundError:
    base_prompt = """[Base prompt file not found. Please ensure 'base_prompt.txt' exists.]"""

# Paths to your custom images
DEFAULT_USER_IMAGE = "white.png"
ASSISTANT_IMAGE = "download.jpeg"

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": base_prompt}
    ]
if "user_image" not in st.session_state:
    st.session_state.user_image = DEFAULT_USER_IMAGE

# App Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- **practice extra math problems Here.**[here](https://www.mathsgenie.co.uk/)**.
""")

# Sidebar Customize Chat Section
st.sidebar.header("Customize Chat")
user_image_upload = st.sidebar.file_uploader("Upload Your Image", type=["jpg", "jpeg", "png"])

# Check if user uploaded an image
if user_image_upload:
    image_bytes = user_image_upload.read()
    st.session_state.user_image = image_bytes
else:
    st.session_state.user_image = DEFAULT_USER_IMAGE

custom_input = st.sidebar.text_input("Add Custom Information to Base Prompt")
if custom_input:
    base_prompt += f"\n{custom_input}"
    st.session_state.messages[0]["content"] = base_prompt

# Main App Layout
st.title("Math Tutor")
st.markdown("""
This chatbot is a profesional math tutor, and he will prepare you to any math you want to learn.
for only 20$ a month!!.
""")

# Start Test button
if not st.session_state.test_mode:
    if st.button("🚀 Start Test"):
        st.session_state.test_mode = True
        st.session_state.time_left = 60 * 60  # Reset timer
        st.session_state.last_tick = time.time()
        st.rerun()

# Add custom CSS for circular images and text alignment
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .chat-container img {
            border-radius: 50%; 
            width: 50px; 
            height: 50px; 
            object-fit: cover; 
            margin-right: 10px;
        }
        .chat-container .user-text, .chat-container .assistant-text {
            display: inline-block;
            vertical-align: top;
            max-width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

# Function to build context for AI
def build_context(messages, base_prompt, history_limit=5):
    conversation_history = []
    for msg in messages[:-1]:
        if msg["role"] == "user":
            conversation_history.append(f"User: {msg['content']}")
        elif msg["role"] == "assistant":
            conversation_history.append(f"Assistant: {msg['content']}")
    recent_history = "\n".join(conversation_history[-history_limit:])
    latest_message = messages[-1]["content"] if messages else ""
    context = (
        base_prompt +
        "\n\nConversation History (Recent):\n" +
        recent_history +
        f"\n\nUser: {latest_message}"
    )
    return context

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.container():
            image_to_display = st.session_state.user_image
            if isinstance(image_to_display, bytes):
                image_b64 = base64.b64encode(image_to_display).decode()
            else:
                image_b64 = base64.b64encode(open(image_to_display, 'rb').read()).decode()
            st.markdown(f"""
                <div class="chat-container">
                    <img src="data:image/png;base64,{image_b64}" alt="User Image">
                    <div class="user-text">
                        <strong>You:</strong> {message["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    elif message["role"] == "assistant":
        with st.container():
            st.markdown(f"""
                <div class="chat-container">
                    <img src="data:image/png;base64,{base64.b64encode(open(ASSISTANT_IMAGE, 'rb').read()).decode()}" alt="Assistant Image">
                    <div class="assistant-text">
                        <strong>Math Tutor:</strong> {message["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# User input prompt
if prompt := st.chat_input("ask any math problem and he will explain it and solve it with you."):
    with st.container():
        image_to_display = st.session_state.user_image
        if isinstance(image_to_display, bytes):
            image_b64 = base64.b64encode(image_to_display).decode()
        else:
            image_b64 = base64.b64encode(open(image_to_display, 'rb').read()).decode()
        st.markdown(f"""
            <div class="chat-container">
                <img src="data:image/png;base64,{image_b64}" alt="User Image">
                <div class="user-text">
                    <strong>You:</strong> {prompt}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.container():
        message_placeholder = st.empty()
        full_response = ""

        try:
            context = build_context(st.session_state.messages, base_prompt)
            response = model.generate_content(context)
            full_response = response.text.strip()
        except Exception as e:
            full_response = f"Error: Unable to generate a response. {str(e)}"

        st.markdown(f"""
            <div class="chat-container">
                <img src="data:image/png;base64,{base64.b64encode(open(ASSISTANT_IMAGE, 'rb').read()).decode()}" alt="Assistant Image">
                <div class="assistant-text">
                    <strong>Math Tutor:</strong> {full_response}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("""
---
Built by Jeronimo.
""")
