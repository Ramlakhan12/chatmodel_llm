# 🤖 LangGraph-Powered Streamlit Chatbot

## 🌟 Overview

This project implements a fully functional, stateful chatbot using **Streamlit** for the frontend interface and **LangGraph** for managing complex conversational logic and state. Conversation history is persistently stored and managed using the LangGraph checkpointing feature backed by an **SQLite database**.

This architecture allows users to start new chats, maintain separate conversations (called **threads**), and load previous chat histories seamlessly from the sidebar. 

---

## ✨ Key Features

* **Stateful Conversations:** Uses LangGraph's state management to maintain conversation context across turns within a unique `thread_id`.
* **Persistent Storage:** Conversation threads are saved and loaded from an **SQLite database**, ensuring continuity across sessions.
* **Multi-Threading:** Users can create new chat sessions (`thread_id`) and switch between any previously saved conversations listed in the sidebar.
* **Streaming UI:** Leverages Streamlit's `st.write_stream` for **real-time, token-by-token** display of the AI response, enhancing user experience.

<video controls src="62b07274-fca6-4da5-a9a5-3ec03d5f70d6-1.mp4" title="Title"></video>

## 🛠️ Project Dependencies

This application requires Python and relies on a few core files and libraries:

### Assumed Files
1.  **`streamlit_frontend_chat_hist`** (The Streamlit frontend code.)
2.  **`langgraph_backend_sqlite.py`** (The custom module that defines the LangGraph `workflow` and the necessary database connection/retrieval functions like `get_all_threads`.)

### Libraries
* `streamlit`
* `langchain`
* `langgraph`
* `langchain-core`
* `uuid` (Standard Python library)

---

## 🚀 Installation and Usage

### Prerequisites

* Python 3.8+
* The project directory must contain the `streamlit_frontend_chat_hist` and `langgraph_backend_sqlite.py` files.

### 1. Clone the repository

Open your terminal or command prompt and execute the following commands to clone the project:

```bash
git clone https://github.com/Ramlakhan12/chatmodel_llm.git
