# 🧠 Smart Workspace – AI Document Assistant (Backend)

Smart Workspace is a backend system built with **Django REST Framework**, **pgVector**, **Sentence Transformers**, **Redis**, and **Groq LLaMA**, providing:

- 📄 Intelligent document upload & processing  
- 🔍 RAG (Retrieval-Augmented Generation) using vector similarity search  
- 💬 Per-document conversational chat  
- ⚡ High-performance embedding caching via Redis  
- 🔐 JWT authentication + request throttling  

Users can upload PDFs, ask questions about their content, and the system answers using only the information found in the uploaded documents.

---

## 🚀 Tech Stack

- **Django 5 + Django REST Framework**
- **PostgreSQL + pgVector extension**
- **Redis caching**
- **Sentence Transformers: `all-MiniLM-L6-v2`**
- **Groq LLaMA 3.1 LLM API**
- **JWT (SimpleJWT)**

---