# Ticket #27: Refactor static/index.html into a funny dog & cat blog layout

| Field | Value |
|---|---|
| Issue | #27 |
| Started | 2026-06-27T10:40:59Z |
| Agent | deepseek / deepseek-v4-pro |

## Issue Description

### 🎯 Goals & Context
Convert the current HTML page into a cartoonish blog about dogs and cats. The tone should be humorous and joky. The page will display a header and a container where JavaScript will inject blog posts (cards).

### 🛠️ Technical Plan & Affected Files
- **File to modify:** `static/index.html`
- **Changes:**
  - Replace the existing content with a simple HTML5 structure:
    - `<title>Paws & Jokes – Dog & Cat Blog</title>`
    - A header with a funny title (e.g., "Paws & Jokes") and a subtitle (e.g., "The furriest blog on the internet").
    - A `<div id="blog-posts"></div>` container for the posts.
    - A `<script src="js/app.js"></script>` at the bottom.
  - Remove any references to the grocery store API.

### ✅ Acceptance Criteria
- [x] Page has a playful header and a container for posts.
- [x] No references to products/grocery remain.
- [x] When the page loads, dummy posts appear (handled by JS).

### 🧪 Testing & Verification
- Open `static/index.html` in a browser (or serve via `python -m http.server`).
- Verify the page looks like a blog container with no backend errors.

---

## Changes Made

| File | Change |
|---|---|
| `static/index.html` | Replaced grocery store page with a playful dog & cat blog layout: header ("Paws & Jokes"), subtitle, `<div id="blog-posts">` container, and footer. All grocery/product references removed. |
| `static/js/app.js` | Populated with JS that injects 4 dummy blog post cards (funny dog/cat themed) into `#blog-posts` on DOM load. Uses vanilla JS (IIFE pattern) with no framework dependencies. |
| `static/css/styles.css` | Added cartoonish, playful styling: warm color palette, dashed borders, hover animations on cards, paw-print emoji accents. |
| `test_main.py` | Updated `test_root_endpoint` to assert new blog content (`"Paws &amp; Jokes"` and `id="blog-posts"`) instead of the old `<h1>Loading...</h1>`. All other tests unchanged. |

## Architecture Decisions

- **No new dependencies**: The blog posts are rendered client-side with vanilla JavaScript, keeping the server-side API (FastAPI) completely unchanged.
- **IIFE pattern in JS**: Wrapped all JS in an immediately-invoked function expression to avoid polluting the global namespace.
- **Static file serving**: `main.py` continues to serve `static/index.html` via `FileResponse` and mount `/static` — no changes needed to the backend.
- **Test update**: Only the assertion in `test_root_endpoint` was updated to match the new HTML content. No test was removed or skipped.

## Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-7.4.3, pluggy-1.6.0
rootdir: /workspace/bob-test-repo
plugins: anyio-3.7.1
collected 18 items

test_hello.py::test_get_hello PASSED                                     [  5%]
test_main.py::TestGroceryStoreAPI::test_root_endpoint PASSED             [ 11%]
test_main.py::TestGroceryStoreAPI::test_static_files_accessible PASSED   [ 16%]
test_main.py::TestGroceryStoreAPI::test_docs_endpoint PASSED             [ 22%]
test_main.py::TestGroceryStoreAPI::test_create_product PASSED            [ 27%]
test_main.py::TestGroceryStoreAPI::test_create_product_minimal_fields PASSED [ 33%]
test_main.py::TestGroceryStoreAPI::test_create_product_invalid_price PASSED [ 38%]
test_main.py::TestGroceryStoreAPI::test_create_product_empty_name PASSED [ 44%]
test_main.py::TestGroceryStoreAPI::test_list_products PASSED             [ 50%]
test_main.py::TestGroceryStoreAPI::test_list_products_with_category_filter PASSED [ 55%]
test_main.py::TestGroceryStoreAPI::test_list_products_available_only PASSED [ 61%]
test_main.py::TestGroceryStoreAPI::test_get_product_by_id PASSED         [ 66%]
test_main.py::TestGroceryStoreAPI::test_get_product_not_found PASSED     [ 72%]
test_main.py::TestGroceryStoreAPI::test_update_product PASSED            [ 77%]
test_main.py::TestGroceryStoreAPI::test_update_product_not_found PASSED  [ 83%]
test_main.py::TestGroceryStoreAPI::test_delete_product PASSED            [ 88%]
test_main.py::TestGroceryStoreAPI::test_delete_product_not_found PASSED  [ 94%]
test_main.py::TestGroceryStoreAPI::test_full_crud_flow PASSED            [100%]

======================== 18 passed, 2 warnings in 0.47s ========================
```
