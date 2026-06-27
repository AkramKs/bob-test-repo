# Static Frontend Blog

A static single-page frontend blog, served directly from `static/index.html`.

## Project Structure

```
.
├── static/
│   ├── index.html       # Single-page application shell
│   ├── js/
│   │   └── app.js       # Frontend logic
│   └── css/
│       └── styles.css   # Stylesheet
├── .gitignore
└── README.md
```

## Local Development

Serve the static site with Python's built-in HTTP server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/static/index.html` in your browser.
