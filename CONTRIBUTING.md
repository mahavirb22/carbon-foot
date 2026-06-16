# Contributing Guide

We welcome contributions to the Carbon Footprint Awareness Platform! To maintain codebase consistency and security, all pull requests must satisfy specific quality gates before they are merged.

---

## 🛠️ Local Environment Setup

### 1. Backend Service (FastAPI)
Ensure you are using Python 3.10+:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Launch the hot-reloading development server in offline mode:
```bash
USE_GEMINI=false USE_FIRESTORE=false uvicorn app.main:app --reload
```

### 2. Frontend Application (React)
Ensure you are using Node.js 20+:
```bash
cd frontend
npm install
npm run dev
```
This runs the development build at `http://localhost:5173`.

### 3. Pre-commit Configuration
To check your changes before committing, install pre-commit:
```bash
pip install pre-commit
pre-commit install
```

---

## 📋 Quality and Validation Checkpoints

Your branch must pass all CI checks locally. Verify them with:

| Test Target | CLI Command (Backend) | CLI Command (Frontend) |
|---|---|---|
| **Linting** | `cd backend && ruff check .` | `cd frontend && npm run lint` |
| **Formatting** | `cd backend && ruff format --check .` | `cd frontend && npm run format:check` |
| **Types** | `cd backend && mypy app` | `cd frontend && npm run typecheck` |
| **Unit Tests** | `cd backend && pytest --cov=app` | `cd frontend && npm run test` |

---

## 💡 Contribution Guidelines

- **Explicit Schema Validation:** All backend models must employ bounded constraints to filter invalid entries early.
- **Accessibility (A11y):** Any newly created frontend component must pass `vitest-axe` validation. Verify that standard visual elements contain adequate label structures.
- **No Stored Credentials:** Do not store API credentials inside repository files. All connections to Google APIs must leverage Application Default Credentials (ADC).
