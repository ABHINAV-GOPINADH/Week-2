import streamlit as st
import google.generativeai as genai

# Setup Gemini API
genai.configure(api_key="AIzaSyAtY7Pm8uXIYQez_Bt251_zYQg3OORsm2A")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-2.0-flash")  # Use the appropriate model from your account

# Set up the Streamlit page
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini Chatbot")

# Initialize session state to keep the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
def display_chat_history():
    for message in st.session_state.messages:
        st.markdown(f"**{message['sender']}:** {message['text']}")

# Collect user input and display chatbot's response
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input.strip():
        # Add user's message to the chat history
        st.session_state.messages.append({"sender": "You", "text": user_input})

        # Get the model's response
        try:
            response = model.generate_content(user_input)
            chatbot_response = response.text
        except Exception as e:
            chatbot_response = f"Error: {e}"

        # Add chatbot's response to the chat history
        st.session_state.messages.append({"sender": "Gemini", "text": chatbot_response})
    
    else:
        st.warning("Please enter a message.")

# Show the updated chat history
display_chat_history()
