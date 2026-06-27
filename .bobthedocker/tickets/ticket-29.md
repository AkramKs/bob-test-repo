# Ticket #29: Rewrite static/js/app.js to inject funny dummy blog posts about dogs & cats

| Field | Value |
|---|---|
| Issue | #29 |
| Started | 2026-06-27T10:40:53Z |
| Agent | deepseek / deepseek-v4-pro |

## Issue Description

### 🎯 Goals & Context
The blog needs dummy content that is joky and funny. We'll replace the existing JavaScript (which likely fetched products) with a hardcoded array of 6-8 hilarious posts about dogs and cats, then render them into the `#blog-posts` container.

### 🛠️ Technical Plan & Affected Files
- **File to modify:** `static/js/app.js`
- **Changes:**
  - Remove any fetch/XHR calls.
  - Create an array `posts` with objects: `{ title, body }`.
  - Example titles: "Why My Dog Thinks He's a Cat", "Top 10 Ways Cats Plot World Domination", "The Secret Life of Socks (According to My Cat)".
  - Example body: short funny paragraphs.
  - Write a function `renderPosts()` that loops over the array, creates HTML elements (cards), and appends them to `#blog-posts`.
  - Call `renderPosts()` on DOMContentLoaded.

### ✅ Acceptance Criteria
- [x] No network requests are made; all data is hardcoded.
- [x] 6-8 funny blog posts appear on page load.
- [x] Each post has a title and a short, humorous body.
- [x] Posts are rendered inside the styled card layout.

### 🧪 Testing & Verification
- Open the page; posts should appear immediately without any errors in the browser console.
- Verify the content is dog/cat themed and funny.

---

## Changes Made

- **`static/js/app.js`** — Complete rewrite: removed empty file and replaced with a hardcoded `posts` array of 8 funny dog/cat blog posts, a `renderPosts()` function that creates DOM elements (`.blog-card` > `h2.blog-title` + `p.blog-body`), and a `DOMContentLoaded` listener that calls `renderPosts()`. No network/fetch/XHR code exists.
- **`static/index.html`** — Added `<div id="blog-posts"></div>` container beneath the existing `<h1>Loading...</h1>` (preserved for test compatibility) so `renderPosts()` has a target to append cards into.
- **`static/css/styles.css`** — Added card layout styles: flexbox column layout for `#blog-posts`, `.blog-card` with white background, rounded corners, shadow and hover effect, styled `.blog-title` and `.blog-body`.

## Architecture Decisions

- **No external dependencies or network calls**: All 8 blog posts are hardcoded in the `posts` array, satisfying the "no network requests" requirement.
- **Plain DOM manipulation**: Used `document.createElement`, `appendChild`, and `textContent` (no innerHTML) for safe, fast rendering.
- **Minimal HTML change**: Kept the existing `<h1>Loading...</h1>` tag intact because `test_root_endpoint` asserts its presence. Added `#blog-posts` div alongside it.
- **Card-based layout**: Each post renders as an `<article class="blog-card">` with `h2` title and `p` body, styled via the existing `styles.css` file.

## Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-7.4.3, pluggy-1.6.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /workspace/bob-test-repo
plugins: anyio-3.7.1
collecting ... collected 18 items

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

======================== 18 passed, 2 warnings in 0.45s ========================
```

All 18 tests pass with 0 failures.
