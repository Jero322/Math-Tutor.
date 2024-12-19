import streamlit as st
import google.generativeai as genai
import base64
from io import BytesIO

# Configure the API key
genai.configure(api_key="AIzaSyBQmBfA--Xy0UaXB1FxwLQ2Oh3bl4holtY")

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
- **About Álvaro Uribe**: Learn about his life and career **[here](https://www.alvarouribevelez.com.co/trabajo-2-1-2-14/)**.
""")

# Sidebar Customize Chat Section
st.sidebar.header("Customize Chat")
user_image_upload = st.sidebar.file_uploader("Upload Your Image", type=["jpg", "jpeg", "png"])

# Check if user uploaded an image
if user_image_upload:
    # Read the uploaded image content and base64 encode it
    image_bytes = user_image_upload.read()
    st.session_state.user_image = image_bytes  # Store the image content
else:
    st.session_state.user_image = DEFAULT_USER_IMAGE  # Use the default image if none uploaded

custom_input = st.sidebar.text_input("Add Custom Information to Base Prompt")
if custom_input:
    base_prompt += f"\n{custom_input}"
    st.session_state.messages[0]["content"] = base_prompt

# Main App Layout
st.title("Álvaro Uribe Vélez Chatbot")
st.markdown("""
This chatbot simulates the responses of Álvaro Uribe Vélez, former President of Colombia. 
Ask questions about his life, political career, and more!
""")

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
    """
    Build the context for the AI model:
    - Base prompt: Personality and background.
    - Conversation history: Condensed summary of the last few exchanges.
    - Latest user query.

    Args:
        messages (list): List of conversation messages (user and assistant messages).
        base_prompt (str): The base personality/background information for the AI.
        history_limit (int): Number of recent exchanges to include in the context.

    Returns:
        str: A formatted string containing the full context for the model.
    """
    # Initialize an empty list to store the summarized history
    conversation_history = []
    
    # Process the messages, excluding the latest user input
    for msg in messages[:-1]:  # Exclude the last message (latest user input)
        if msg["role"] == "user":
            conversation_history.append(f"User: {msg['content']}")
        elif msg["role"] == "assistant":
            conversation_history.append(f"Assistant: {msg['content']}")
    
    # Condense the conversation history to the last `history_limit` exchanges
    recent_history = "\n".join(conversation_history[-history_limit:])  # Include only the last few exchanges
    
    # Get the latest user query
    latest_message = messages[-1]["content"] if messages else ""
    
    # Assemble the full context
    context = (
        base_prompt +
        "\n\nConversation History (Recent):\n" +
        recent_history +
        f"\n\nUser: {latest_message}"  # Add the current user input
    )
    
    return context

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.container():
            # Encode user image if uploaded, else use the default image
            image_to_display = st.session_state.user_image
            if isinstance(image_to_display, bytes):
                image_b64 = base64.b64encode(image_to_display).decode()  # Convert image bytes to base64
            else:
                image_b64 = base64.b64encode(open(image_to_display, 'rb').read()).decode()  # For default image
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
                        <strong>Álvaro Uribe Bot:</strong> {message["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# User input prompt
if prompt := st.chat_input("Ask about Álvaro Uribe Vélez's achievements, family, or policies..."):
    # Display user message
    with st.container():
        # Encode user image if uploaded, else use the default image
        image_to_display = st.session_state.user_image
        if isinstance(image_to_display, bytes):
            image_b64 = base64.b64encode(image_to_display).decode()  # Convert image bytes to base64
        else:
            image_b64 = base64.b64encode(open(image_to_display, 'rb').read()).decode()  # For default image
        st.markdown(f"""
            <div class="chat-container">
                <img src="data:image/png;base64,{image_b64}" alt="User Image">
                <div class="user-text">
                    <strong>You:</strong> {prompt}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.container():
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Build context for the AI model
            context = build_context(st.session_state.messages, base_prompt)

            # Generate response
            response = model.generate_content(context)
            full_response = response.text.strip()
        except Exception as e:
            full_response = f"Error: Unable to generate a response. {str(e)}"

        # Display response
        st.markdown(f"""
            <div class="chat-container">
                <img src="data:image/png;base64,{base64.b64encode(open(ASSISTANT_IMAGE, 'rb').read()).decode()}" alt="Assistant Image">
                <div class="assistant-text">
                    <strong>Álvaro Uribe Bot:</strong> {full_response}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("""
---
Built by Jeronimo.
""")
