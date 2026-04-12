# Changelog

All notable changes to this rewrite project are documented in this file.

## [0.8.1] - 2026-04-11

### Docs

- Prepared GitHub-facing publication docs and links.
- Added root `LICENSE` and this root `CHANGELOG.md` for repository-level visibility.
- Updated `README.md` documentation entry points and runtime verification notes.
- Updated `docs/NOTICE.md` from placeholder-heavy draft to a release checklist template.

### Verification

- Backend tests: `8 passed` (`backend_rewrite/.venv/Scripts/python.exe -m pytest -q`)
- Frontend build: `npm run build` passed
- Backend health endpoint: `/health` returns `{"status":"ok","service":"assistgen-rewrite"}`

## [0.8.0] - 2026-04-09

### Backend

- Switched conversation persistence from memory default to SQLite default.
- Added SQLite repository implementation and persistence regression tests.
- Kept memory repository as fallback strategy.

### Frontend

- Continued modularized rewrite with conversation context + stream chat integration.

### Notes

- Detailed historical entries are preserved in `docs/CHANGELOG_REWRITE.md`.

