# Ticket #36: Add static 'apples' information page

| Field | Value |
|---|---|
| Issue | #36 |
| Started | 2026-07-07 |
| Agent | BobTheDocker Realizer |

## Issue Description

### 🎯 Goals & Context
Create a new static HTML page about apples, served from the existing static files mount. This allows visitors to access informative content at `/apples.html`.

### 🛠️ Technical Plan & Affected Files
- **Files to Create**:
  - `static/apples.html` – full HTML page with heading, paragraphs about apples, varieties, fun facts, nutrition, and consistent styling with `index.html`
- **Files to Modify**:
  - `static/index.html` – add a navigation link to `apples.html` in the header

### ✅ Acceptance Criteria
1. `static/apples.html` exists and displays apple content
2. `static/index.html` has an "Apples" navigation link pointing to `apples.html`
3. `apples.html` has a "Home" link pointing back to `index.html`
4. Visual style is consistent with `index.html` (same card/header/footer pattern, inline CSS, matching color theme adapted for apples)

## Changes Made

| File | Action | Reason |
|---|---|---|
| `static/apples.html` | Created | New static page about apples with consistent styling |
| `static/index.html` | Modified | Added `<nav>` with "🍎 Apples" link in header |

## Architecture Decisions

- **No styles.css**: Per ticket #34, the project has no external CSS. Both pages use self-contained inline `<style>` blocks with identical structural patterns (card, header, footer, image-placeholder, fun-fact classes).
- **Color theme**: `apples.html` uses a red/warm gradient (`#6b1a1a → #d4784a`) distinct from `index.html`'s green gradient, while keeping identical layout and proportions.
- **Navigation**: Both pages use a `<nav>` element in the header with pill-shaped link buttons. `index.html` links to `apples.html`; `apples.html` links back to `index.html`.
- **Content**: `apples.html` covers what apples are, 7 popular varieties, 6 fun facts, and nutrition/health benefits. Footer links to Wikipedia.
- **Relative links**: Uses `href="apples.html"` and `href="index.html"` — works for both local file browsing and any static file server.

## Test Results

### HTML Validation
```
static/index.html: OK
  DOCTYPE: PASS, html tag: PASS, head tag: PASS, body tag: PASS, viewport meta: PASS, charset: PASS
static/apples.html: OK
  DOCTYPE: PASS, html tag: PASS, head tag: PASS, body tag: PASS, viewport meta: PASS, charset: PASS
```

### Content Verification
- `index.html` → Apples nav link: **PASS**
- `apples.html` → Home nav link: **PASS**
- `apples.html` → apple content sections: **PASS** (heading, varieties, fun facts, nutrition, Wikipedia link)
- No external stylesheet dependencies: **PASS** (styles.css already deleted in ticket #34)
- Self-contained: both pages have 1 external link each (Wikipedia footer), as expected

### Notes
- No Python backend exists (wiped in ticket #34). No `pytest` or `uvicorn` available to run. Verification done via HTML parser validation and content checks.
- The `architecture.md` still references FastAPI/SQLAlchemy (pre-ticket #34 state) but updating it is out of scope for this ticket.
