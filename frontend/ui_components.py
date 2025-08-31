# ui_components.py
import streamlit as st
from typing import Dict, Any
import logging
from .api_client import APIClient
from datetime import datetime
from config import DEFAULT_MODEL, THINKING_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UIComponents:
    """UI components for the Streamlit interface."""

    @staticmethod
    def render_header():
        """Render the application header and inject global styles."""
        # Inject polished CSS for a professional look + light gray background
        st.markdown(
            """
            <style>
            /* Page background and centered content column */
            html, body, [data-testid="stAppViewContainer"] > div:first-child {
                background: #f2f4f7; /* light grayish background */
            }

            .block-container {
                max-width: 1100px;
                margin: 24px auto;
                padding: 1.25rem 2rem;
            }

            /* Header */
            .main-header {
                display: flex;
                align-items: center;
                gap: 14px;
                background: linear-gradient(90deg,#ffffff,#fafbfd);
                border: 1px solid rgba(20,20,20,0.04);
                padding: 14px 18px;
                border-radius: 12px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.03);
            }
            .main-header h3 {
                margin: 0;
                font-family: "Inter", "Segoe UI", Roboto, sans-serif;
                font-weight: 700;
                color: #0f1724;
                letter-spacing: -0.2px;
            }
            .main-header .sub {
                color: #475569;
                font-size: 13px;
                font-weight: 500;
            }

            /* Chat area */
            .chat-wrapper {
                background: transparent;
                margin-top: 12px;
            }

            .chat-container {
                background: #ffffff;
                border: 1px solid rgba(15, 23, 42, 0.05);
                border-radius: 12px;
                padding: 20px;
                max-height: 520px;
                overflow-y: auto;
                box-shadow: 0 6px 30px rgba(9, 30, 66, 0.04);
            }

            /* Message bubbles */
            .msg-row {
                display: flex;
                gap: 12px;
                margin: 12px 0;
                align-items: flex-end;
            }

            .msg-row.user {
                justify-content: flex-start;
            }

            .msg-row.ai {
                justify-content: flex-end;
            }

            .avatar {
                width: 44px;
                height: 44px;
                border-radius: 10px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                color: white;
                flex: 0 0 44px;
                box-shadow: 0 4px 14px rgba(2,6,23,0.06);
                font-family: "Inter", sans-serif;
            }

            .avatar.user {
                background: linear-gradient(135deg,#2d8fe6,#2879b9);
            }

            .avatar.ai {
                background: linear-gradient(135deg,#9aa7b2,#7d8b97);
            }

            .bubble {
                max-width: 78%;
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.45;
                color: #0f1724;
                box-shadow: 0 4px 18px rgba(16,24,40,0.03);
                border: 1px solid rgba(15, 23, 42, 0.03);
                background: #f8fafc;
                word-wrap: break-word;
            }

            .bubble.user {
                background: linear-gradient(180deg, #e8f3ff, #d7ecff);
                color: #04243a;
                border-radius: 12px 12px 12px 4px;
                border: 1px solid rgba(41, 132, 255, 0.12);
            }

            .bubble.ai {
                background: #ffffff;
                color: #0f1724;
                border-radius: 12px 12px 4px 12px;
            }

            .bubble .meta {
                display: flex;
                gap: 8px;
                align-items: center;
                margin-bottom: 8px;
            }

            .bubble .who {
                font-weight: 700;
                font-size: 12px;
                color: #334155;
            }

            .bubble .time {
                font-size: 11px;
                color: #64748b;
                opacity: 0.9;
            }

            /* Pending note under user bubble */
            .pending-note {
                margin-left: 56px; /* avatar (44) + gap (12) */
                max-width: 78%;
                text-align: right;
                font-size: 12px;
                color: #64748b;
                opacity: 0.9;
                margin-top: 6px;
            }

            /* Input area */
            .input-area {
                margin-top: 18px;
                display: flex;
                gap: 12px;
                align-items: flex-end;
            }

            .stTextArea > div > div > textarea {
                border-radius: 12px !important;
                border: 1px solid rgba(15, 23, 42, 0.06) !important;
                font-size: 14px !important;
                background: #0f172410 !important;
                padding: 14px !important;
                color: #0f1724 !important;
                min-height: 64px !important;
            }

            .send-btn {
                border-radius: 10px !important;
                height: 48px !important;
                font-weight: 700 !important;
                background: linear-gradient(135deg,#0ea5a4,#0891b2) !important;
                border: none !important;
                color: white !important;
                padding: 0 18px !important;
            }

            .send-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(2,6,23,0.08);
            }

            /* scrollbar */
            .chat-container::-webkit-scrollbar {
                width: 8px;
            }
            .chat-container::-webkit-scrollbar-track {
                background: #f1f5f9;
                border-radius: 6px;
            }
            .chat-container::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 6px;
            }

            /* footer spacing */
            .footer-space {
                height: 8px;
            }

            @media (max-width: 760px) {
                .block-container { padding-left: 12px; padding-right: 12px; }
                .bubble { max-width: 86%;}
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Render header content
        st.markdown(
            '<div class="main-header">'
            '<div style="display:flex;flex-direction:column;">'
            '<h3>💬 Conversation</h3>'
            '<div class="sub">Professional AI Assistant • Ollama + FastAPI</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_model_selector() -> tuple[str, bool]:
        """
        Render model selection dropdown.

        Returns:
            Tuple of (model_name, thinking_mode)
        """
        col1, col2 = st.columns([3, 1.2])

        with col1:
            model_option = st.selectbox(
                "Model Mode:",
                options=[
                    "Normal",
                    "Thinking"
                ],
                index=0
            )

        with col2:
            # concise model info
            if model_option and "Normal" in model_option:
                st.caption("🚀 Fast responses")
                model = DEFAULT_MODEL
                thinking = False
            else:
                st.caption("🧠 Detailed thinking")
                model = THINKING_MODEL
                thinking = True

        return model, thinking

    @staticmethod
    def render_prompt_input() -> str:
        """
        Render prompt input area.

        Returns:
            User prompt text
        """
        prompt = st.text_area(
            "Enter your prompt:",
            placeholder="Ask me anything...",
            height=100,
            max_chars=2000
        )
        return prompt

    @staticmethod
    def render_submit_button() -> bool:
        """
        Render submit button.

        Returns:
            True if button was clicked
        """
        return st.button("Generate Response", type="primary", use_container_width=True)

    @staticmethod
    def render_response(response: str):
        """
        Render the AI response.
        """
        st.markdown("### 🤖 AI Response:")
        st.markdown("---")
        st.markdown(response)

    @staticmethod
    def render_chat_message(message: str, is_user: bool = True, model: str | None = None, timestamp: str | None = None):
        """
        Render a single chat message with refined styling.
        If timestamp is None, nothing is shown — your messages can include 'timestamp' in the message dict.
        """
        import html

        escaped_message = html.escape(message).replace("\n", "<br>")

        # Build meta row (who + optional timestamp)
        who = "You" if is_user else "AI Assistant"
        ts_html = f'<span class="time">• {timestamp}</span>' if timestamp else ""

        if is_user:
            st.markdown(
                f"""
                <div class="msg-row user">
                  <div class="avatar user">YOU</div>
                  <div class="bubble user">
                    <div class="meta"><div class="who">👤 {who}</div>{ts_html}</div>
                    <div>{escaped_message}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            model_info = f' • {model}' if model else ""
            st.markdown(
                f"""
                <div class="msg-row ai">
                  <div class="bubble ai">
                    <div class="meta"><div class="who">🤖 AI Assistant{model_info}</div>{ts_html}</div>
                    <div>{escaped_message}</div>
                  </div>
                  <div class="avatar ai">AI</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    @staticmethod
    def render_chat_container(messages: list):
        """
        Render the chat container with all messages.
        Expects messages to be list of dicts with keys:
          - prompt (user text)
          - response (ai text)
          - thinking (optional bool)
          - timestamp (optional ISO string or formatted)
          - pending (optional bool) when waiting for AI response
        """
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        if messages:
            for msg in messages:
                # prefer provided timestamps; otherwise None
                user_ts = msg.get("timestamp") if msg.get("timestamp") else None
                ai_ts = msg.get("timestamp") if msg.get("timestamp") else None

                # render user entry (prompt)
                UIComponents.render_chat_message(msg["prompt"], is_user=True, timestamp=user_ts)

                # If pending, show small right-aligned note under user bubble
                if msg.get("pending") and not msg.get("response"):
                    st.markdown(
                        '<div class="pending-note">⏳ Waiting for the response…</div>',
                        unsafe_allow_html=True,
                    )

                # render ai response
                if msg.get("response"):
                    model_display = "Thinking Mode" if msg.get("thinking") else "Normal Mode"
                    UIComponents.render_chat_message(msg["response"], is_user=False, model=model_display, timestamp=ai_ts)

            # auto scroll to bottom
            st.markdown(
                """
                <script>
                (function(){
                    var chat = document.querySelector('.chat-container');
                    if (chat) { chat.scrollTop = chat.scrollHeight; }
                })();
                </script>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="color:#64748b;padding:26px 12px;font-size:14px;">No messages yet — start the conversation below.</div>',
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_chat_input(autofocus: bool = True):
        """
        Render the chat input area and return (prompt_str, submitted_bool).
        Uses an on_click callback to clear safely.
        """
        st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)  # spacing
        st.markdown('<div class="input-area">', unsafe_allow_html=True)

        # Ensure session keys exist before widgets are created
        if "chat_input" not in st.session_state:
            st.session_state["chat_input"] = ""

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        def _send_callback():
            text = st.session_state.get("chat_input", "")
            st.session_state["pending_message"] = (text or "").strip()
            st.session_state["chat_input"] = ""

        # Layout: large textarea + send button
        col1, col2 = st.columns([9, 1.6], gap="small")
        with col1:
            st.text_area(
                "Message",
                placeholder="Type your message here...",
                height=72,
                max_chars=2000,
                label_visibility="collapsed",
                key="chat_input"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button(
                "Send",
                key="send_btn",
                type="primary",
                use_container_width=True,
                on_click=_send_callback,
                args=(),
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # If pending_message set by callback, pop and return it
        pending = st.session_state.pop("pending_message", None)
        if pending is not None:
            return pending, True

        # No submission
        # Optionally autofocus the textarea using JS (best-effort)
        if autofocus:
            st.markdown(
                """
                <script>
                (function(){
                    // Focus the last textarea on the page (Streamlit creates the textarea)
                    const areas = document.getElementsByTagName('textarea');
                    if (areas.length) {
                        const ta = areas[areas.length - 1];
                        try { ta.focus(); } catch(e) {}
                    }
                })();
                </script>
                """,
                unsafe_allow_html=True,
            )

        return "", False

    @staticmethod
    def render_error(error_message: str):
        """
        Render error message.
        """
        st.error(f"❌ Error: {error_message}")

    @staticmethod
    def render_loading():
        """Render loading spinner."""
        # Keep for compatibility, but prefer inline pending note in chat.
        return st.spinner("🔄 Working…")

    @staticmethod
    def render_connection_status(is_connected: bool):
        """
        Render connection status indicator.
        """
        if is_connected:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Disconnected - Please start the FastAPI server")
