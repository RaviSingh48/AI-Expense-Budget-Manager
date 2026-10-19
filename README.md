# 💰 AI Expense & Budget Manager

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20SQLite-336791.svg)](https://www.postgresql.org/)
[![Vector DB](https://img.shields.io/badge/Vector%20Store-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack, AI-powered personal finance and expense management web application. Easily log daily transactions, monitor monthly budgets with real-time threshold alerts, analyze spending habits through interactive visualizations, and consult an intelligent AI financial advisor powered by **Retrieval-Augmented Generation (RAG)** using **Google Gemini 2.5 Flash** and **ChromaDB**.

---

## 🌟 Key Highlights

- **💳 Complete Expense Management**: Full CRUD operations with categories, payment methods, transaction dates, and custom notes.
- **🎯 Dynamic Budget Tracking**: Set monthly spending targets with automated warnings at 80% utilization and alerts when exceeding 100%.
- **📊 Interactive Visual Analytics**: Real-time spending charts (daily trends, category distributions, weekly breakdown) powered by Chart.js.
- **🤖 RAG-Powered AI Financial Assistant**: Natural language financial querying grounded strictly in your verified transaction data via ChromaDB vector embeddings and Google Gemini 2.5 Flash (`google-genai` SDK).
- **🔐 Multi-User Data Isolation**: Robust JWT authentication with Argon2id password hashing and user-level metadata filters in both relational queries and vector retrieval.
- **⚡ Dual Database Flexibility**: Seamless out-of-the-box support for both **SQLite** (instant local development with zero external dependencies) and **PostgreSQL** (production grade).

---

## 🏗️ System Architecture

```text
                             USER
                               │
                               ▼
                  ┌───────────────────────────┐
                  │    Frontend Client (UI)   │
                  │ Vanilla JS + CSS + HTML5  │
                  │    Chart.js Visuals       │
                  └─────────────┬─────────────┘
                                │
                             HTTP/REST
                                │
                                ▼
                  ┌───────────────────────────┐
                  │      FastAPI Backend      │
                  │   Uvicorn ASGI Server     │
                  │ JWT Auth & Request Router │
                  └─────────────┬─────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
┌──────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│ PostgreSQL/SQLite│  │ ChromaDB Vector   │  │  Gemini 2.5 Flash │
│ Relational Store │  │ Semantic Search   │  │   google.genai    │
│ Exact Financials │  │ User Vectors      │  │ Financial Advisor │
└──────────────────┘  └───────────────────┘  └───────────────────┘
```

---

## 🔄 RAG (Retrieval-Augmented Generation) Pipeline

```text
User Question: "How much did I spend on groceries this month?"
                        │
                        ▼
            POST /api/v1/chat (FastAPI)
                        │
                        ▼
                RAGService Pipeline
                        │
      ┌─────────────────┴─────────────────┐
      │                                   │
      ▼                                   ▼
[ChromaDB Vector Store]         [SQL Database Query]
Semantic similarity search       Exact SQL aggregations:
filtered by authenticated        Total spend, category sum,
user ID                          budget status & metrics
      │                                   │
      └─────────────────┬─────────────────┘
                        ▼
           Context Assembly & Guardrails
                        │
                        ▼
           Gemini 2.5 Flash (google.genai)
                        │
                        ▼
        Grounded, Factual Financial Advice
```

### Context Security & Isolation
Each user's vectors are stored with an immutable `user_id` metadata tag. Semantic searches are filtered using `where={"user_id": current_user.id}` to guarantee that no user's financial transactions can ever be accessed by or leaked to another user.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern, high-performance async Python web framework |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) | Lightning-fast ASGI web server |
| **ORM & Migrations** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) & [Alembic](https://alembic.sqlalchemy.org/) | Enterprise-grade ORM and database schema migration tool |
| **Relational Database** | [PostgreSQL](https://www.postgresql.org/) / [SQLite](https://www.sqlite.org/) | Reliable relational data storage with dialect auto-switching |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) | Embedding store for fast semantic similarity retrieval |
| **Embeddings & AI** | [Google Gemini 2.5 Flash](https://ai.google.dev/) | State-of-the-art LLM integrated via `google-genai` SDK |
| **Security & Auth** | [Argon2id](https://github.com/P-H-C/phc-winner-argon2) + [PyJWT](https://pyjwt.readthedocs.io/) | Next-gen cryptographic hashing and JSON Web Tokens |
| **Frontend UI** | Modern Vanilla JS, HTML5, CSS3 | Clean, responsive SPA interface with glassmorphism design |
| **Visualizations** | [Chart.js](https://www.chartjs.org/) | Interactive responsive charting library |

---

## 📁 Directory Structure

```text
AI-Expense-Budget-Manager/
├── backend/
│   ├── alembic/                  # Database migration scripts
│   │   └── versions/             # Migration version history
│   ├── app/
│   │   ├── core/                 # Config, database connection, security, exceptions
│   │   ├── middleware/           # Request logging, CORS, error handling
│   │   ├── models/               # SQLAlchemy ORM models (User, Expense, Budget)
│   │   ├── prompts/              # Financial advisor system prompts & guardrails
│   │   ├── repositories/         # Database query and CRUD abstraction layer
│   │   ├── routes/v1/            # API endpoints (auth, expenses, budgets, chat, analytics)
│   │   ├── schemas/              # Pydantic request/response validation schemas
│   │   ├── services/             # Business logic (RAG, Chroma, Gemini, Auth, Budget)
│   │   └── utils/                # Date formatting and text embedding helpers
│   ├── tests/                    # E2E test suites (test_api.py, test_auth_e2e.py)
│   ├── .env.example              # Environment variable template
│   ├── alembic.ini               # Alembic migration configuration
│   └── requirements.txt          # Python backend dependencies
├── frontend/
│   ├── css/                      # Stylesheets and custom variables
│   ├── js/                       # Modular ES6 JavaScript
│   │   ├── components/           # UI components (chatWidget, analytics, modals)
│   │   ├── services/             # API client, state store, notifications
│   │   ├── app.js                # Main application lifecycle coordinator
│   │   └── config.js             # API endpoint configuration
│   └── index.html                # Single-page application entry point
├── .gitignore                    # Git ignore file (safeguards secrets & DBs)
├── README.md                     # Project documentation
├── render.yaml                   # Infrastructure-as-code for Render deployment
└── run.bat                       # One-click Windows development launcher
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- **Python 3.10+** installed
- **Git** installed

### 1. Clone Repository
```bash
git clone https://github.com/RaviSingh48/AI-Expense-Budget-Manager.git
cd AI-Expense-Budget-Manager
```

---

### Option A: One-Click Startup (Windows)
Double-click `run.bat` or run:
```cmd
run.bat
```
The script will automatically detect or create the virtual environment, verify dependencies, start the FastAPI backend on port `8000`, start the frontend on port `5500`, and launch your browser!

---

### Option B: Manual Setup

#### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate

# Activate on Linux / macOS:
source .venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

#### 3. Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```bash
# Windows PowerShell:
Copy-Item backend\.env.example backend\.env

# Linux / macOS:
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your settings:
```env
APP_NAME="AI Expense & Budget Manager"
APP_ENV="development"
DEBUG=True
PORT=8000
HOST="127.0.0.1"

# Database: SQLite is ready to use immediately without setup
DATABASE_URL="sqlite:///./data/expense_tracker.db"

# Or configure PostgreSQL:
# DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/expense_tracker"

# Gemini API Key (get free from https://aistudio.google.com/)
GEMINI_API_KEY="your-gemini-api-key-here"
GEMINI_MODEL="gemini-2.5-flash"

SECRET_KEY="your-random-32-char-secret-key"
```

#### 4. Run the Backend Server
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Base: `http://localhost:8000`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Health Status: `http://localhost:8000/api/v1/health`

#### 5. Run the Frontend Server
In a separate terminal window:
```bash
python -m http.server 5500 --directory frontend
```
- Open [http://localhost:5500](http://localhost:5500) in your browser.

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate user and return JWT | No |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | Yes |
| `GET` | `/api/v1/expenses` | List user expenses with pagination & filters | Yes |
| `POST` | `/api/v1/expenses` | Add new expense & update vector store | Yes |
| `GET` | `/api/v1/expenses/{id}` | Retrieve specific expense details | Yes |
| `PUT` | `/api/v1/expenses/{id}` | Update an existing expense transaction | Yes |
| `DELETE`| `/api/v1/expenses/{id}` | Remove expense & purge from vector store | Yes |
| `GET` | `/api/v1/budgets/current` | Retrieve current active monthly budget | Yes |
| `POST` | `/api/v1/budgets` | Set or update monthly budget target | Yes |
| `GET` | `/api/v1/analytics/overview`| Summary metrics (spend, budget %, count) | Yes |
| `GET` | `/api/v1/analytics/trends` | Daily, weekly, and monthly trend data | Yes |
| `POST` | `/api/v1/chat` | Ask the RAG-assisted AI Financial Advisor | Yes |
| `GET` | `/api/v1/health` | Service diagnostic and database health check | No |

---

## 🧪 Running Tests

Comprehensive end-to-end and unit tests are included:

```bash
# Run API endpoint integration tests
python backend/test_api.py

# Run Authentication lifecycle tests
python backend/test_auth_e2e.py
```

---

## 🌐 Deployment Guide

### Deploy Backend (Render)
1. Fork or push this repository to GitHub.
2. Sign in to [Render](https://render.com/).
3. Create a **New Web Service** pointing to your repository, or use the included `render.yaml` Blueprint.
4. Set the Root Directory to `backend`.
5. Configure environment variables in the Render Dashboard:
   - `DATABASE_URL`: Your Render PostgreSQL Internal Database URL.
   - `SECRET_KEY`: A secure 32+ character random string.
   - `GEMINI_API_KEY`: Your Google AI Studio API key.

### Deploy Frontend (Vercel)
1. Sign in to [Vercel](https://vercel.com/).
2. Import the repository and select `frontend` as the Root Directory.
3. In `frontend/js/config.js`, update `API_BASE_URL` to point to your live Render backend URL.
4. Deploy!

---

## 👨‍💻 Author

**Ravi Singh**  
- GitHub: [@RaviSingh48](https://github.com/RaviSingh48)  
- Repository: [AI-Expense-Budget-Manager](https://github.com/RaviSingh48/AI-Expense-Budget-Manager)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
