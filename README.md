# Enterprise RAG Intelligence System

> Secure, context-aware RAG system with RBAC enforcement — built for enterprise data silos.

🔗 **Live Demo:** [Click here](https://enterprise-rag-system-abhi.streamlit.app/)

---

## Features

- **RBAC Enforcement** — 4 roles, each sees only permitted documents
- **Multi-format RAG** — PDF, CSV, JSON enterprise data sources
- **Zero Hallucination** — AI answers ONLY from retrieved context
- **Source Citations** — Every answer cites [Source N] with relevance score
- **Confidence Indicators** — High / Medium / Low per response
- **Free AI** — Powered by Google Gemini 1.5 Flash (no cost)

## 👥 User Roles

| User | Role | Access |
|------|------|--------|
| 👑 Arjun Sharma | Admin | All 9 docs |
| 👥 Priya Mehta | HR Manager | 5 docs |
| 💰 Rahul Gupta | Finance Analyst | 6 docs |
| 🎓 Sneha Patel | Intern | 3 docs |

##  Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-rag
cd enterprise-rag
pip install -r requirements.txt
streamlit run app.py
```

Get your **free** Gemini API key: [aistudio.google.com](https://aistudio.google.com/apikey)

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select this repo → Deploy
4. Add `GEMINI_API_KEY` in Secrets (optional)

## Architecture

```
User Query → RBAC Filter → Retrieval Engine → Gemini Flash → Grounded Response
                ↓               ↓                               ↓
         Accessible Docs   Top-3 Relevant              Citations + Confidence
```

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Google Gemini 1.5 Flash (Free)
- **RAG:** Custom keyword-scored retrieval
- **RBAC:** Role-based document access control
