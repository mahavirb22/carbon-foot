# 🌱 Carbon Footprint Awareness Platform

An accessible, user-centric web application designed to help individuals **understand, track, and reduce** their personal carbon footprints. The platform estimates emissions across transportation, home energy, diet, and general consumption, delivering personalized, AI-generated reduction strategies and historical tracking.

Built with a **Python (FastAPI)** backend and a **React (TypeScript)** frontend, it integrates **Google Gemini (Vertex AI)** for intelligent insights, uses **Cloud Firestore** for anonymous history retention, and is packaged for easy deployment to **Google Cloud Run**.

---

## 🔗 Project Overview

The application is structured around three key user journeys:
1. **Understand:** Enter detailed daily life metrics and get an immediate, itemized breakdown of your annual carbon footprint.
2. **Track:** Save calculations anonymously (using a localized device ID) to build a personal history and monitor trends over time.
3. **Reduce:** Receive tailored, quantified suggestions to lower your emissions, focused on your highest-impact categories first.

---

## 🏗️ Architecture

```text
               +-------------------------------------------------+
               |             React + TypeScript SPA              |
               |  - Accessible HTML & semantic ARIA structures   |
               |  - Localized device ID tracking (localStorage)  |
               +-----------------------+-------------------------+
                                       |
                                  HTTP (JSON)
                                       |
                                       v
               +-------------------------------------------------+
               |              FastAPI Backend App                |
               |  - Pydantic models with schema validation       |
               |  - Rate limiting & size-constrained middleware  |
               +----------+---------------------------+----------+
                          |                           |
                          v                           v
             +-------------------------+ +-------------------------+
             |    Vertex AI Gemini     | |     Cloud Firestore     |
             |   (Personalized Advice) | |   (Snapshot Persistence) |
             |   [Rules-based Fallback]| |    [Memory Repository]  |
             +-------------------------+ +-------------------------+
```

### Layout
- `backend/`: API services, calculations engine, fallback rules, database repositories, and test files.
- `frontend/`: React components, state hooks, styling sheets, type definitions, and Vitest/Playwright tests.
- `docs/`: In-depth documentation regarding internal structures and design choices.

---

## 🚀 Local Development Setup

### Prerequisite Environment
- Python 3.10 or newer
- Node.js 20 or newer

### 1. Running the Backend
From the repository root:
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements-dev.txt
```

Start the local server with Gemini and Firestore mock integrations active:
```bash
USE_GEMINI=false USE_FIRESTORE=false uvicorn app.main:app --reload
```
The API documentation will be available at `http://localhost:8000/docs`.

### 2. Running the Frontend
From the repository root:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` (requests under `/api/*` are proxied to the backend at `http://localhost:8000`).

### 3. Containerized Execution
Build and run the entire application as a single Docker container locally:
```bash
docker build -t carbon-footprint-app .
docker run -p 8080:8080 -e USE_GEMINI=false -e USE_FIRESTORE=false carbon-footprint-app
```
Then visit `http://localhost:8080`.

---

## 🧪 Testing and Quality Control

All quality checks are enforced automatically on every commit and push:

| Test Suite | Execution | Targets |
|---|---|---|
| **Backend Tests** | `cd backend && pytest --cov=app --cov-fail-under=90` | Calculator formulas, Firestore integrations, routing schema validation, Gemini parsing, and fallback rules. |
| **Frontend Tests** | `cd frontend && npm run test` | React components, API integrations, hooks, and axe accessibility audits. |
| **End-to-End** | `cd frontend && npx playwright test` | Complete user interactions (filling forms, submitting, viewing results, saving entries). |
| **Linting** | `ruff check .` / `npm run lint` | Strict quality guidelines (including `jsx-a11y` constraints). |
| **Static Types** | `mypy app` / `npm run typecheck` | Strict compiler verification in Python and TypeScript. |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
