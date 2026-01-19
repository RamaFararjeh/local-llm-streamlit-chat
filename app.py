import streamlit as st
import requests
import json
from pathlib import Path
from datetime import date

# -----------------------
# Settings
# -----------------------
st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.2:latest"

TODAY = date.today().isoformat()
CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)
DEFAULT_CHAT_FILE = CHATS_DIR / f"chat_{TODAY}.json"

# -----------------------
# Helpers: Save / Load (for selected file)
# -----------------------
def load_chat(file_path: Path) -> list:
    if file_path.exists():
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_chat(file_path: Path, messages: list) -> None:
    file_path.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def ask_ollama(messages: list, model_name: str) -> str:
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"].strip()

# -----------------------
# Sidebar: Select chat file
# -----------------------
with st.sidebar:
    st.header("⚙️ Settings")
    model_name = st.text_input("Model", value=DEFAULT_MODEL)

    st.divider()
    st.subheader("📂 Chats (by day)")

    # list all chat files; if none, create today's by default
    chat_files = sorted(CHATS_DIR.glob("chat_*.json"))
    if not chat_files:
        # ensure today's file exists (empty list)
        DEFAULT_CHAT_FILE.touch(exist_ok=True)
        chat_files = [DEFAULT_CHAT_FILE]

    file_names = [f.name for f in chat_files]

    # keep selected file in session_state so it won't reset on rerun
    if "selected_chat" not in st.session_state:
        st.session_state.selected_chat = DEFAULT_CHAT_FILE.name if DEFAULT_CHAT_FILE.name in file_names else file_names[-1]

    selected_name = st.selectbox(
        "Select a chat file",
        options=file_names,
        index=file_names.index(st.session_state.selected_chat) if st.session_state.selected_chat in file_names else 0
    )

    st.session_state.selected_chat = selected_name
    CHAT_FILE = CHATS_DIR / selected_name

    st.write(f"**Selected file:** `{CHAT_FILE}`")

    colA, colB = st.columns(2)
    with colA:
        if st.button("💾 Save now"):
            if "messages" in st.session_state:
                save_chat(CHAT_FILE, st.session_state.messages)
            st.success("Saved")

    with colB:
        if st.button("🧹 Clear file"):
            save_chat(CHAT_FILE, [])
            st.session_state.messages = []
            st.success("Cleared")
            st.rerun()

    st.divider()
    if st.button("🧹 Reset chat (delete file)"):
        if CHAT_FILE.exists():
            CHAT_FILE.unlink()
        st.session_state.messages = []
        st.success("Deleted")
        st.rerun()

# -----------------------
# UI: Header
# -----------------------
st.title("🤖 Local LLM Chat (Ollama)")
st.caption("Chat UI + Sidebar + Multi-day JSON Chats")

# -----------------------
# Initialize messages (load selected file)
# -----------------------
# reload when file changes
if "loaded_file" not in st.session_state or st.session_state.loaded_file != str(CHAT_FILE):
    st.session_state.messages = load_chat(CHAT_FILE)
    st.session_state.loaded_file = str(CHAT_FILE)

# -----------------------
# Display chat (bubbles)
# -----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# Chat input
# -----------------------
user_input = st.chat_input("اكتب رسالتك هنا...")

if user_input:
    # 1) add user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_chat(CHAT_FILE, st.session_state.messages)

    # 2) show user immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # 3) get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                bot_reply = ask_ollama(st.session_state.messages, model_name)
            except requests.exceptions.RequestException as e:
                bot_reply = f"Error talking to Ollama: {e}"
        st.markdown(bot_reply)

    # 4) save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_chat(CHAT_FILE, st.session_state.messages)

    st.rerun()
