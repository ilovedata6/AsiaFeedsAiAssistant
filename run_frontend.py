"""
Frontend runner for AI Assistant.

This script should be used with streamlit run command:
    streamlit run run_frontend.py
"""

import streamlit as st
import logging
import sys
import os

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from frontend.api_client import APIClient
from frontend.ui_components import UIComponents

# Configure page
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Initialize services
@st.cache_resource
def get_api_client():
    """Get API client instance."""
    return APIClient()

@st.cache_resource
def get_ui_components():
    """Get UI components instance."""
    return UIComponents()

def check_backend_connection(api_client: APIClient) -> bool:
    """Check if backend is available."""
    return api_client.health_check()

def handle_generate_request(api_client: APIClient, ui: UIComponents, prompt: str, model: str, thinking: bool):
    """
    Handle generation request.
    
    Args:
        api_client: API client instance
        ui: UI components instance
        prompt: User prompt
        model: Selected model
        thinking: Thinking mode flag
    """
    try:
        with ui.render_loading():
            response_data = api_client.generate_response(
                prompt=prompt,
                model=model,
                thinking=thinking
            )
            
            response_text = response_data.get("response", "No response received")
            
            # Store response in session state
            st.session_state.responses.append({
                "prompt": prompt,
                "response": response_text,
                "model": model,
                "thinking": thinking
            })
            
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        ui.render_error(str(e))

def render_sidebar(api_client: APIClient, ui: UIComponents):
    """Render sidebar with app info and connection status."""
    with st.sidebar:
        st.markdown("## 📊 App Status")
        
        # Connection status
        is_connected = check_backend_connection(api_client)
        ui.render_connection_status(is_connected)
        
        st.markdown("---")
        st.markdown("## ℹ️ About")
        st.markdown("""
        **AI Assistant** is a minimal chat interface powered by:
        - **Backend**: FastAPI (Port 8000)
        - **Frontend**: Streamlit (Port 8501)
        - **AI Models**: Ollama (Local)
        
        **Models Available:**
        - Llama3.2:3b (Normal mode)
        - Qwen3:4b (Thinking mode)
        """)
        
        if st.session_state.responses:
            st.markdown("---")
            st.markdown("## 📈 Chat History")
            st.markdown(f"Total responses: {len(st.session_state.responses)}")
            
            if st.button("Clear History"):
                st.session_state.responses = []
                st.rerun()

def main():
    """Main application function."""
    # Get service instances
    api_client = get_api_client()
    ui = get_ui_components()
    
    # Render sidebar
    render_sidebar(api_client, ui)
    
    # Render main interface
    ui.render_header()
    
    # Model selection
    model, thinking = ui.render_model_selector()
    
    # Render chat container with existing messages
    st.write(f"Debug: Messages in session state: {len(st.session_state.responses)}")
    if st.session_state.responses:
        st.write(f"Last message: {st.session_state.responses[-1]['prompt'][:50]}...")
    ui.render_chat_container(st.session_state.responses)
    
    # Render chat input at the bottom
    prompt, submit_clicked = ui.render_chat_input()
    
    # Handle submit
    if submit_clicked:
        if prompt.strip():
            # Store the message before clearing
            user_message = prompt.strip()
            # Clear the input by deleting the widget's value from session state
            if "chat_input" in st.session_state:
                del st.session_state["chat_input"]
            handle_generate_request(api_client, ui, user_message, model, thinking)
            st.rerun()  # Rerun to clear input and show new message
        else:
            st.warning("⚠️ Please enter a message before sending.")

# Run the main function
main()
