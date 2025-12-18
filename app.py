"""
Streamlit Web UI for NCD Health RAG Assistant
"""

import streamlit as st
from src.chatbot import NCDChatbot
import os

# Page configuration
st.set_page_config(
    page_title="NCD Health Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS to match the design
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        padding: 1.5rem 2rem;
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Warning banner */
    .warning-banner {
        background-color: #FFF9E6;
        border-left: 4px solid #FFB020;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Chat container */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
        max-height: 500px;
        overflow-y: auto;
        background-color: #F5F7FA;
        border-radius: 8px;
    }
    
    /* User message (right side, blue) */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 0.5rem 0;
    }
    
    .user-bubble {
        background-color: #4A90E2;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    /* Bot message (left side, white) */
    .bot-message {
        display: flex;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .bot-avatar {
        width: 40px;
        height: 40px;
        background-color: #4A90E2;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    
    .bot-bubble {
        background-color: white;
        color: #2C3E50;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Source citations */
    .source-cite {
        display: inline-block;
        background-color: #4A90E2;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.75rem;
        margin: 0 2px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        border: 1px solid #E1E8ED;
    }
    
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #357ABD;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chatbot' not in st.session_state:
    try:
        st.session_state.chatbot = NCDChatbot()
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {str(e)}")
        st.stop()

# Header
st.markdown("""
<div class="main-header">
    🏥 NCD Health Assistant
</div>
""", unsafe_allow_html=True)

# Warning banner
st.markdown("""
<div class="warning-banner">
    ⚠️ Getting medical info from AI. This is not a substitute for professional medical advice.
</div>
""", unsafe_allow_html=True)

# Chat display area
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-bubble">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Format sources if available
            content = message["content"]
            if "sources" in message and message["sources"]:
                for i, source in enumerate(message["sources"], 1):
                    content = content.replace(f"[{i}]", f'<span class="source-cite">[{i}]</span>')
            
            st.markdown(f"""
            <div class="bot-message">
                <div class="bot-avatar">🤖</div>
                <div class="bot-bubble">{content}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show sources below the message
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**[{i}]** {source['source']}")
                        st.caption(source['content'][:200] + "...")

# Input area
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Enter your chatsen mee anapt answer here...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle send
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get bot response
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.chatbot.ask(user_input, return_sources=True)
            
            # Add bot message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"],
                "sources": response.get("sources", [])
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Sorry, I encountered an error: {str(e)}"
            })
    
    # Rerun to update chat
    st.rerun()

# Sidebar with info
with st.sidebar:
    st.markdown("### About")
    st.info("""
    This is an AI-powered assistant for information about 
    Non-Communicable Diseases (NCDs).
    
    **Topics covered:**
    - Diabetes
    - Cancer types
    - Heart disease
    - Obesity
    - High blood pressure
    - And more...
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by Google Gemini & LangChain")
