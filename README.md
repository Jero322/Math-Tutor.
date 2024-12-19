# Álvaro Uribe Vélez Chatbot

This project is a **Streamlit-based chatbot** that simulates the responses of Álvaro Uribe Vélez, former President of Colombia. Users can ask questions about his life, political career, policies, and more. The chatbot uses a generative AI model to provide detailed and context-aware answers.

---

## Features

- **Customizable Chat Experience:**
  - Upload your profile picture to personalize the chat.
  - Add custom information to the chatbot's base prompt.
- **Responsive AI Model:**
  - Simulates Álvaro Uribe Vélez's responses.
  - Handles context-aware conversations with recent history.
- **Dynamic Layout:**
  - Interactive chat interface with user-friendly design.
  - Circular profile images for both user and assistant.

---

## Installation

To run the chatbot locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Alvaro-Uribe-Chatbot.git
   cd Alvaro-Uribe-Chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run chatbot.py
   ```

4. Open your browser and interact with the chatbot at `http://localhost:8501`.

---

## Usage

1. Ask the chatbot about Álvaro Uribe Vélez's life, career, or policies.
2. Customize the chatbot's base prompt by adding additional context in the sidebar.
3. Upload a profile picture to enhance your chat experience.

---

## Preview

![Chatbot Screenshot](images/preview.png)

---

## File Structure

```
Alvaro-Uribe-Chatbot/
├── chatbot.py            # Main Streamlit app
├── requirements.txt      # Python dependencies
├── images/
│   ├── white.png         # Default user image
│   ├── download.jpeg     # Assistant image
│   └── preview.png       # Screenshot for README
├── base_prompt.txt       # Default prompt for the chatbot
└── README.md             # Documentation file
```

---

