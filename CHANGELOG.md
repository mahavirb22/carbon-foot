# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

## [1.3.0] - 2026-06-12

### Added
- **Stream Guard Middleware:** Read actual body content bytes rather than depending on raw headers to enforce maximum size limits securely.
- **SHA-256 Response Cache:** Implemented a TTLCache for duplicate API inputs to lower model costs.
- **Typed Metadata:** Added type-safe attributes to specify whether calculations were derived from caches, smart rules, or Gemini models.
- **Accessibility Improvements:** Added detailed ARIA labels on visual layout bars and comparison indicators.
- **CI Gates:** Extended CI tasks with API schema matching checks and automated E2E Playwright test execution.

---

## [1.2.0] - 2026-06-12

### Added
- **Rate Limiting:** Enforced API limits of 10 requests per minute on insights requests to prevent service abuse.
- **Input Validation Bounding:** Safeguarded system calculations using strict min/max thresholds.
- **Structured JSON Logging:** Shifted application logs to structured JSON formatting containing queryable transaction fields.
- **Dark Mode Support:** Added accessible styling choices obeying CSS prefers-color-scheme queries.

---

## [1.1.0] - 2026-06-11

### Added
- **Strict Quality Checks:** Standardized pre-commit hooks and coverage rules in CI (backend coverage > 90% and frontend coverage > 85%).
- **Component Tests:** Extended frontend tests to cover key panels with automated accessibility (axe-core) validation.
- **Refactoring:** Form inputs isolated to dedicated form controls and hooks.

---

## [1.0.0] - 2026-06-08

### Added
- **Carbon Math Engine:** Established initial calculation logic based on EPA/DEFRA datasets.
- **Rule Engine & Fallback:** Created smart rule fallbacks if Gemini queries fail.
- **State Saving:** Configured basic Firestore saving for anonymous histories.
- **App Layout:** Developed basic SPA shell and FastAPI integration.
