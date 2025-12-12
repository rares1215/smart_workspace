# 🧠 Smart Workspace – AI Document Assistant (Backend)

Smart Workspace is a **production-ready backend API** built with **Django REST Framework**, designed to let users upload documents and interact with them through an AI-powered chat interface using **Retrieval-Augmented Generation (RAG)**.

The system ensures **secure authentication**, **email verification**, **high performance**, and **LLM-safe answers** strictly grounded in user-uploaded documents.

---

## ✨ Core Features

### 📄 Document Management
- Upload PDF documents
- Automatic text extraction
- Chunking & vector embedding generation
- Per-user document isolation

### 🔍 Retrieval-Augmented Generation (RAG)
- Semantic search using **pgVector**
- Cosine similarity over document chunks
- Context-aware answers generated **only from document content**
- Zero hallucinations enforced at prompt level

### 💬 Conversational AI Chat
- Per-document chat history
- Context preserved across messages
- Natural, conversational, yet professional tone
- Multi-turn follow-up questions supported

### ⚡ Performance & Scalability
- Redis caching for:
  - Document embeddings
  - Query embeddings
  - Document metadata
- Bulk database operations (no N+1 queries)
- Optimized similarity queries
- API-level throttling

### 🔐 Authentication & Security
- JWT authentication (SimpleJWT)
- Email verification with expiring numeric codes
- Account activation required before login
- Secure password validation
- Per-endpoint rate limiting

---

## 🛠 Tech Stack

- **Django 5**
- **Django REST Framework**
- **PostgreSQL + pgVector**
- **Redis (Dockerized)**
- **Sentence Transformers**
  - `all-MiniLM-L6-v2`
- **Groq LLaMA 3.1 API**
- **JWT Authentication (SimpleJWT)**
- **Mailtrap (Email Testing)**

---

## 🔐 Email Verification Flow

1. User registers
2. Account is created as **inactive**
3. A **6-digit numeric verification code** is sent via email
4. Code expires after **10 minutes**
5. User verifies the code
6. Account becomes active and login is enabled
7. Resend endpoint available with throttling

---

## 📡 API Endpoints (Overview)

### Auth
- `POST /api/register/`
- `POST /api/verify-email/{user_id}/`
- `POST /api/resend-email/{user_id}/`

### Documents
- `POST /api/documents/`
- `GET /api/documents/`
- `GET /api/documents/{id}/`
- `DELETE /api/documents/{id}/`

### RAG Chat
- `POST /api/rag/{document_id}/`
- `GET /api/chat/{document_id}/`
- `DELETE /api/chat/{document_id}/`

---

## 🚦 Rate Limiting (Throttling)

| Action | Limit |
|------|------|
| Document upload (burst) | 2 / minute |
| Document upload (daily) | 20 / day |
| RAG queries (burst) | 10 / minute |
| RAG queries (daily) | 100 / day |
| Resend verification email | 1 / minute, 5 / hour |

---

## 🧠 LLM Safety Guarantees

- Answers are generated **only from retrieved document context**
- If information is missing:
  > “The document does not contain enough information.”
- No hallucinated facts
- Context + chat history enforced in prompt

---

## 📈 Performance Optimizations

- Embeddings cached in Redis (24h TTL)
- Document data cached on retrieval
- Bulk creation of embeddings
- Database query monitoring with Django Silk

---

## 🔮 Future Improvements

- Async background processing (Celery)
- Streaming LLM responses
- Frontend integration (React + Tailwind)
- Role-based access
- Analytics & usage metrics

---

## 👨‍💻 Author

Built as a **portfolio-grade backend project** focused on:
- Clean architecture
- Real-world AI workflows
- Production-ready API design

---

## 📄 License

MIT License

