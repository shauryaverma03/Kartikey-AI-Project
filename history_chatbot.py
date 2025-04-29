import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def get_gemini_response(prompt):
    # Add context to ensure the response is history-focused
    history_context = "You are a history expert. Please provide accurate and detailed historical information. "
    full_prompt = history_context + prompt
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Set up the Streamlit interface
st.title("History Expert Chatbot")
st.write("Ask me anything about history!")

# Chat input
user_input = st.text_input("Your question:", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get bot response
    bot_response = get_gemini_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"History Expert: {message['content']}")
        st.write("---") 