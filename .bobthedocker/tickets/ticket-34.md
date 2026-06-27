# Ticket #34: Wipe codebase and create static monkey index page

| Field | Value |
|---|---|
| Issue | #34 |
| Started | 2026-06-27T10:51:07Z |
| Agent | deepseek / deepseek-v4-pro |

## Issue Description

## 🎯 Goals & Context
Completely remove all Python backend code (FastAPI, SQLAlchemy, tests, models, schemas) and the existing static folder. Keep only `.gitignore`, `README.md`, and `requirements.txt` as project boilerplate. Then create a simple static `index.html` page about monkeys inside a `static/` directory.

## 🛠️ Technical Plan & Affected Files
### Files to Delete
- `main.py`
- `models.py`
- `schemas.py`
- `hello.py`
- `test_main.py`
- `test_hello.py`
- `grocery_store.db`
- `static/css/styles.css`
- `static/js/app.js`
- `static/index.html`

### Files to Create
- `static/index.html` – A self-contained HTML page about monkeys (facts, maybe an image placeholder, styling inline or in a `<style>` tag).

### Files to Keep Unchanged
- `.gitignore`
- `README.md` (consider updating description later, but not required for this ticket)
- `requirements.txt` (will become irrelevant but keep)

### Architecture
- No server, no Python. The page is pure HTML/CSS, served as a static file.
- Content: at least a headline, a paragraph about monkeys, and a list of monkey species or behaviors.

## ✅ Acceptance Criteria
1. All listed files are deleted from the repository.
2. `static/index.html` exists and is valid HTML5.
3. Opening `static/index.html` in a browser displays a page about monkeys.
4. No Python files or database remain.

## 🧪 Testing & Verification
- Run `ls` to confirm only `static/`, `.gitignore`, `README.md`, `requirements.txt` remain.
- Open `static/index.html` in a browser or validate with `python -m http.server 8000` and navigate to `/static/index.html`.
- No Python modules should be importable.

---

## Changes Made

| File | Action | Reason |
|---|---|---|
| `main.py` | Deleted | Remove FastAPI backend entry point |
| `models.py` | Deleted | Remove SQLAlchemy ORM models |
| `schemas.py` | Deleted | Remove Pydantic schemas |
| `hello.py` | Deleted | Remove auxiliary module |
| `test_main.py` | Deleted | Remove integration tests |
| `test_hello.py` | Deleted | Remove unit tests |
| `grocery_store.db` | Deleted | Remove SQLite database file |
| `static/css/styles.css` | Deleted | Remove old grocery store styles |
| `static/js/app.js` | Deleted | Remove old frontend JavaScript |
| `static/index.html` (old) | Deleted | Remove old grocery store landing page |
| `static/index.html` (new) | Created | New self-contained HTML5 page about monkeys with inline CSS |

## Architecture Decisions

- **No server runtime**: The entire Python backend (FastAPI + Uvicorn + SQLAlchemy) has been removed. The project is now a pure static site.
- **Self-contained HTML**: All styles are embedded in a `<style>` tag within the single `index.html` file. No external CSS or JS dependencies.
- **Content structure**: The page includes a header, an emoji-based image placeholder, sections on "What Are Monkeys?", "Famous Monkey Species" (7 species), "Fun Monkey Facts" (6 facts), and "Monkeys vs. Apes". A footer links to Wikipedia.
- **Kept boilerplate files**: `.gitignore`, `README.md`, and `requirements.txt` remain intact as project scaffolding, though `requirements.txt` is now vestigial.

## Test Results

- **File existence check**: Only `static/index.html`, `.gitignore`, `README.md`, and `requirements.txt` remain in the tracked file tree. No `.py` or `.db` files found.
- **HTML5 validation**: All 12 structural checks passed (DOCTYPE, html/head/body tags, lang attribute, charset, monkey content, parser success).
- **Acceptance criteria**: All 4 criteria met.
