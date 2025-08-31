import streamlit as st
import logging
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


class AIAssistantApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        self.api_client = APIClient()
        self.ui = UIComponents()
    
    def check_backend_connection(self) -> bool:
        """Check if backend is available."""
        return self.api_client.health_check()
    
    def handle_generate_request(self, prompt: str, model: str, thinking: bool):
        """
        Handle generation request.
        
        Args:
            prompt: User prompt
            model: Selected model
            thinking: Thinking mode flag
        """
        try:
            with self.ui.render_loading():
                response_data = self.api_client.generate_response(
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
                
                # Display response
                self.ui.render_response(response_text)
                
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            self.ui.render_error(str(e))
    
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
            
            if st.session_state.responses:
                st.markdown("---")
                st.markdown(f"## 📈 Chat History")
                st.markdown(f"Total responses: {len(st.session_state.responses)}")
                
                if st.button("Clear History"):
                    st.session_state.responses = []
                    st.rerun()
    
    def run(self):
        """Run the Streamlit application."""
        # Render sidebar
        self.render_sidebar()
        
        # Render main interface
        self.ui.render_header()
        
        # Model selection
        model, thinking = self.ui.render_model_selector()
        
        # Prompt input
        prompt = self.ui.render_prompt_input()
        
        # Submit button
        if self.ui.render_submit_button():
            if prompt.strip():
                self.handle_generate_request(prompt, model, thinking)
            else:
                st.warning("Please enter a prompt before submitting.")
        
        # Display previous responses
        if st.session_state.responses:
            st.markdown("---")
            st.markdown("## 📝 Previous Responses")
            
            for i, response_data in enumerate(reversed(st.session_state.responses)):
                with st.expander(f"Response {len(st.session_state.responses) - i}: {response_data['prompt'][:50]}..."):
                    st.markdown(f"**Model**: {response_data['model']} {'(Thinking Mode)' if response_data['thinking'] else ''}")
                    st.markdown(f"**Prompt**: {response_data['prompt']}")
                    st.markdown(f"**Response**: {response_data['response']}")


def main():
    """Main entry point for the Streamlit app."""
    # Initialize the app only when running under Streamlit
    app = AIAssistantApp()
    app.run()


# Run the app directly when the script is executed
main()
