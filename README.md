# 🤖 Local LLM Streamlit Chat (Ollama)

A simple and interactive **Streamlit-based chat interface** connected to a **locally hosted Large Language Model (LLM)** using **Ollama**.  
The application runs fully **offline**, supports **conversation history**, **multi-day chat storage**, and provides a clean chat UI similar to modern LLM applications.

---

## 🚀 Features

- 🧠 Connects to a **locally installed LLM** via Ollama  
- 💬 Real-time chat interface built with **Streamlit**
- 🗂️ **Conversation history** with full context awareness
- 📅 **Multi-day chat storage** (one JSON file per day)
- 🔄 Reset and clear chat functionality
- ⚙️ Model selection from the sidebar
- 🌐 Fully **local execution** (no external APIs required)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Frontend UI
- **Ollama** – Local LLM runtime
- **Requests** – API communication
- **JSON** – Persistent chat storage

---

## 📂 Project Structure

local-llm-streamlit-chat/
│
├── app.py # Main Streamlit application
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── chats/
└── .gitkeep # Chat history JSON files (created at runtime)


---

## ⚙️ Prerequisites

Before running the project, make sure you have:

- Python **3.9+**
- Ollama installed and running  
  👉 https://ollama.com
- At least one local model pulled, for example:
  ```bash
  ollama pull llama3.2
