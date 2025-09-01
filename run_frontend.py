"""
Frontend runner for AI Assistant.

This script should be used with streamlit run command:
    streamlit run run_frontend.py
"""

import streamlit as st
import logging
from datetime import datetime
import sys
import os

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from frontend.api_client import APIClient
from frontend.ui_components import UIComponents
import html

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

    # Stream tokens and live-update a placeholder bubble
    st.session_state.is_processing = True
    item = st.session_state.messages[idx]
    model = item.get("model", "llama3.2:3b")
    thinking = item.get("thinking", False)
    ts = item.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M")

    placeholder = st.empty()
    accumulated = ""
    try:
        for chunk in api_client.stream_response(prompt=item.get("prompt", ""), model=model, thinking=thinking):
            if not chunk:
                continue
            accumulated += chunk
            safe = html.escape(accumulated).replace("\n", "<br>")
            model_display = "Thinking Mode" if thinking else "Normal Mode"
            placeholder.markdown(
                f"""
                <div class=\"msg-row ai\">
                  <div class=\"bubble ai\">
                    <div class=\"meta\"><div class=\"who\">🤖 AI Assistant • {model_display}</div><span class=\"time\">• {ts}</span></div>
                    <div>{safe}</div>
                  </div>
                  <div class=\"avatar ai\">AI</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        accumulated = accumulated or f"❌ Error: {e}"
    finally:
        # Persist final text into messages and clear pending
        st.session_state.messages[idx]["response"] = accumulated
        st.session_state.messages[idx]["pending"] = False
        st.session_state.awaiting_index = None
        st.session_state.is_processing = False
        # Force a final rerun to render as a normal bubble
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
            st.markdown("## 📈 Chat History")
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

    # Header and model selection
    ui.render_header()
    model, thinking = ui.render_model_selector()

    # Chat container
    ui.render_chat_container(st.session_state.messages)

    # Chat input
    text, submitted = ui.render_chat_input()
    if submitted:
        clean = (text or "").strip()
        if not clean:
            st.warning("⚠️ Please enter a message before sending.")
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

    # Process any pending call after rendering UI
    process_pending_if_any(api_client)

# Run the main function
main()
