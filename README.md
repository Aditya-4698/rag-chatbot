# 🤖 RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** built with Django REST Framework.

The application allows authenticated users to upload PDF documents and ask questions about their documents. The system retrieves relevant document chunks using semantic search and generates answers using a local LLM through Ollama.

---

## 🚀 Features

- 🔐 User authentication
- 👤 User-specific document isolation
- 📄 PDF document upload
- 📑 PDF text extraction
- ✂️ Text cleaning and chunking
- 🧠 Local text embeddings using Ollama
- 🔎 Semantic search using ChromaDB
- 🤖 RAG-based question answering
- 🦙 Local LLM inference using Ollama
- 📚 Source document and page information
- 💬 Chat history
- 🗑️ Chat message deletion
- 🔒 User-isolated retrieval
- ⚡ Celery background processing
- 🗄️ PostgreSQL database
- 🔴 Redis message broker
- 🐳 Docker and Docker Compose
- ❤️ Health monitoring endpoint
- 🧪 Automated Django tests
- 🔄 GitHub Actions CI
- 🎨 Futuristic AI/RAG frontend

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      Frontend    │
                         │ HTML / CSS / JS   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Django REST    │
                         │       API        │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          Authentication     PDF Upload        Chat API
                 │                │                │
                 │                ▼                │
                 │        PDF Extraction          │
                 │                │                │
                 │                ▼                │
                 │        Text Chunking           │
                 │                │                │
                 │                ▼                │
                 │       Ollama Embeddings        │
                 │                │                │
                 │                ▼                │
                 │           ChromaDB              │
                 │                │                │
                 │                │                ▼
                 │                │        Semantic Retrieval
                 │                │                │
                 │                │                ▼
                 │                │          RAG Context
                 │                │                │
                 │                │                ▼
                 │                │          Ollama LLM
                 │                │                │
                 └────────────────┴────────────────┘
                                  │
                                  ▼
                              Answer
