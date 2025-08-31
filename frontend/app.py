import streamlit as st
import logging
from datetime import datetime
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

# Initialize session state for chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_index" not in st.session_state:
    st.session_state.awaiting_index = None
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False


class AIAssistantApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        self.api_client = APIClient()
        self.ui = UIComponents()
    
    def check_backend_connection(self) -> bool:
        """Check if backend is available."""
        return self.api_client.health_check()
    
    def _process_pending_if_any(self):
        """If there's a pending chat message, call backend and update it."""
        idx = st.session_state.awaiting_index
        if idx is None or st.session_state.is_processing:
            return
        if idx < 0 or idx >= len(st.session_state.messages):
            # reset invalid state
            st.session_state.awaiting_index = None
            return

        st.session_state.is_processing = True
        item = st.session_state.messages[idx]
        try:
            response_data = self.api_client.generate_response(
                prompt=item.get("prompt", ""),
                model=item.get("model", "llama3.2:3b"),
                thinking=item.get("thinking", False),
            )
            response_text = response_data.get("response", "")

            # update the message
            st.session_state.messages[idx]["response"] = response_text
            st.session_state.messages[idx]["pending"] = False
            # optional: add/refresh timestamp for AI
            st.session_state.messages[idx]["timestamp"] = item.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            st.session_state.messages[idx]["response"] = f"❌ Error: {e}"
            st.session_state.messages[idx]["pending"] = False
        finally:
            st.session_state.awaiting_index = None
            st.session_state.is_processing = False
            st.rerun()
    
    def render_sidebar(self):
        """Render sidebar with app info and connection status."""
        with st.sidebar:
            st.markdown("## 📊 App Status")
            
            # Connection status
            is_connected = self.check_backend_connection()
            self.ui.render_connection_status(is_connected)
            
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
    
    def run(self):
        """Run the Streamlit application."""
        # Render sidebar
        self.render_sidebar()
        
        # Render main interface
        self.ui.render_header()
        
        # Model selection (kept)
        model, thinking = self.ui.render_model_selector()

        # Chat container
        self.ui.render_chat_container(st.session_state.messages)

        # Chat input (send button + textarea)
        text, submitted = self.ui.render_chat_input()
        if submitted:
            clean = (text or "").strip()
            if not clean:
                st.warning("Please enter a message.")
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

        # If there's a pending request, process it now (after UI renders the pending note)
        self._process_pending_if_any()


def main():
    """Main entry point for the Streamlit app."""
    # Initialize the app only when running under Streamlit
    app = AIAssistantApp()
    app.run()


# Run the app directly when the script is executed
main()
