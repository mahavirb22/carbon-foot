# System Architecture Guide

This document outlines the design architecture, directory structuring, and layer communications of the Carbon Footprint Awareness Platform.

---

## 🗺️ System Overview

The application functions as a single unified container deployed to **Google Cloud Run**, serving both dynamic REST API requests and static single-page application (SPA) assets.

```text
  +-------------------------------------------------------------+
  |                      Browser (SPA Web)                       |
  |     - React, TS, Vite                                       |
  |     - Local storage device hashes                           |
  +------------------------------+------------------------------+
                                 |
                            HTTP / JSON
                                 |
                                 v
  +-------------------------------------------------------------+
  |                   GCP Cloud Run Container                   |
  |                                                             |
  |   +-----------------------------------------------------+   |
  |   |                FastAPI App Backend                  |   |
  |   |  - Static mounts serve React bundles                |   |
  |   |  - Route schemas parse incoming inputs              |   |
  |   +-------+-------------------------------------+-------+   |
  |           |                                     |           |
  +-----------|-------------------------------------|-----------+
              |                                     |
              v (ADC)                               v (ADC)
  +-----------------------+             +-----------------------+
  |    Vertex AI Gemini   |             |    Cloud Firestore    |
  |   (Insights Engine)   |             | (Snapshot Database)   |
  +-----------------------+             +-----------------------+
```

---

## 🐍 Backend Core Structure

The backend application uses a layered design structure where dependency injections move strictly inward:

### 1. Calculation Domain (`app/carbon/`)
- Contains purely deterministic formulas without secondary side-effects or external network actions.
- Models emission constants directly (using published DEFRA, EPA, and IPCC metrics) with source links inline.

### 2. Suggestion & Insights Engine (`app/insights/`)
- Leverages the Vertex AI API client to construct structured prompts for Gemini.
- Uses a deterministic, rules-based calculation fallback (`rules.py`) to construct saving insights should the model be unavailable.

### 3. Storage Layer (`app/repository/`)
- Interfaces are abstracted behind protocols (`base.py`).
- Implementations include `firestore_repo.py` for live database saves and `memory_repo.py` for testing scenarios.

### 4. Transport Controllers (`app/routes/`)
- Mount endpoint functions (such as `/api/calculate`, `/api/insights`, and `/api/entries`).
- Validates request structures using bounded constraints defined in `app/models.py`.

---

## ⚛️ Frontend Architecture

The frontend application uses React and TypeScript:

- **State Sync Hook (`src/hooks/useFootprint.ts`):** Coordinates client requests, local state hooks, error responses, and local storage updates.
- **Component Views (`src/components/`):** Contains localized views such as form fields, graphs, visual savings breakdowns, and tables.
- **Helper Utilities (`src/lib/`):** Houses helper formatters and client api definitions.

---

## 🛠️ Security and Isolation Principles

- **No Shared Keys:** Avoid embedding static keys. All systems use Application Default Credentials (ADC) to authenticate.
- **Offline Reliability:** All features gracefully fallback to offline mechanisms (such as rule-based fallback generators and memory tables) when environment configurations disable AI and DB integrations.
- **Input Constraints:** Form values are verified against range limits on both the client (via input constraints) and server (via Pydantic schemas).
