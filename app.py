import streamlit as st
from groq import Groq
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Gen Z Chatbot",
    page_icon="💬",
    layout="centered"
)

# Custom CSS for improved UI
st.markdown("""
    <style>
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        font-size: 2.5em;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: #a8b2d1;
        font-size: 1.1em;
        font-weight: 400;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        margin: 1rem 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* User message specific */
    [data-testid="stChatMessageContent"] {
        color: #e6e6e6;
    }
    
    /* Input box styling */
    .stChatInputContainer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1rem;
    }
    
    .stChatInput input {
        border-radius: 25px !important;
        border: 2px solid rgba(168, 178, 209, 0.3) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput input:focus {
        border-color: #64b5f6 !important;
        box-shadow: 0 0 15px rgba(100, 181, 246, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #8892b0;
        padding: 2rem;
        font-size: 0.9em;
        margin-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Error message styling */
    .stAlert {
        background: rgba(244, 67, 54, 0.1) !important;
        border: 1px solid rgba(244, 67, 54, 0.3) !important;
        border-radius: 10px !important;
        color: #ff6b6b !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(168, 178, 209, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(168, 178, 209, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">💬 Gen Z Chatbot</div>
        <div class="subtitle">Your AI homie that speaks the language</div>
    </div>
""", unsafe_allow_html=True)

# Get API key from environment
api_key = os.getenv("api_key")

# Check API key
if not api_key:
    st.error("⚠️ API Key not found. Please add your Groq API key to the .env file as: api_key=YOUR_KEY")
    st.info("💡 Get your free API key from: https://console.groq.com")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message for first time users
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("Yo! I'm your Gen Z chatbot. Ask me anything and I'll hit you back with that Gen Z energy. No cap! 💯")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate Gen Z response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Configure Groq
            client = Groq(api_key=api_key)
           
            
            # Create Gen Z persona prompt
            genz_system_prompt = """You are a Gen Z chatbot that speaks in Gen Z slang and internet language. Use terms like: no cap, fr fr, bruh, bet, facts, lowkey, highkey, mid, fire, goated, based, cringe, W, L, ratio, cope, touch grass, it's giving, living rent free, understood the assignment, and other Gen Z expressions naturally.

Keep responses helpful and informative while using Gen Z language. Don't be over the top - keep it natural and authentic. Use emojis occasionally but don't overdo it."""
            
            # Generate response
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": genz_system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            
            full_response = chat_completion.choices[0].message.content
            
            # Simulate typing effect
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"Bruh, something went wrong 😅\n\nError: {str(e)}"
            message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("""
    <div class="footer">
        Powered by Groq AI 🚀 | Built by Ousman Bah<br>
        <small>Keep it real, keep it Gen Z 💯</small>
    </div>
""", unsafe_allow_html=True)