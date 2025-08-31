import streamlit as st
import logging
from datetime import datetime
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_index" not in st.session_state:
    st.session_state.awaiting_index = None
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

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

def process_pending_if_any(api_client: APIClient):
    idx = st.session_state.awaiting_index
    if idx is None or st.session_state.is_processing:
        return
    if idx < 0 or idx >= len(st.session_state.messages):
        st.session_state.awaiting_index = None
        return
    st.session_state.is_processing = True
    item = st.session_state.messages[idx]
    try:
        response_data = api_client.generate_response(
            prompt=item.get("prompt", ""),
            model=item.get("model", "llama3.2:3b"),
            thinking=item.get("thinking", False),
        )
        response_text = response_data.get("response", "")
        st.session_state.messages[idx]["response"] = response_text
        st.session_state.messages[idx]["pending"] = False
        if not st.session_state.messages[idx].get("timestamp"):
            st.session_state.messages[idx]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        st.session_state.messages[idx]["response"] = f"❌ Error: {e}"
        st.session_state.messages[idx]["pending"] = False
    finally:
        st.session_state.awaiting_index = None
        st.session_state.is_processing = False
        st.rerun()

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
        
        if st.session_state.messages:
            st.markdown("---")
            st.markdown(f"## 📈 Chat History")
            st.markdown(f"Total messages: {len(st.session_state.messages)}")
            
            if st.button("Clear History"):
                st.session_state.messages = []
                st.session_state.awaiting_index = None
                st.session_state.is_processing = False
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

    # Chat container
    ui.render_chat_container(st.session_state.messages)

    # Chat input
    text, submitted = ui.render_chat_input()
    if submitted:
        clean = (text or "").strip()
        if not clean:
            st.warning("Please enter a message before submitting.")
        else:
            st.session_state.messages.append({
                "prompt": clean,
                "response": "",
                "model": model,
                "thinking": thinking,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "pending": True,
            })
            st.session_state.awaiting_index = len(st.session_state.messages) - 1
            st.rerun()

    # Process any pending request
    process_pending_if_any(api_client)

# Run the main function
if __name__ == "__main__":
    main()
else:
    # This runs when imported by Streamlit
    main()
