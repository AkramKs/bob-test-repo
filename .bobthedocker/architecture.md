# Architecture Reference

## Tech Stack & Dependencies
- **Runtime**: None required; static HTML/CSS/JS files only
- **Serving**: Any static file server (e.g., `python -m http.server`, nginx, Apache)
- **Frontend**: Static HTML/CSS/JS single-page application
- **Database**: None
- **Testing**: Manual browser testing

## Directory Structure
```
.
├── static/
│   ├── index.html       # Single-page application shell
│   ├── js/
│   │   └── app.js       # Frontend logic (API calls, UI updates)
│   └── css/
│       └── styles.css   # Stylesheet
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## Entry Points
- **Frontend**: Served from `/static/index.html` by any static file server.

## Build & Run Commands
```bash
# Serve static site locally
python -m http.server 8000

# Open in browser: http://localhost:8000/static/index.html
```

## Notable Patterns & Conventions
- **Static Single Page Application**: The frontend is a static SPA with no backend dependencies.
- **Zero Dependencies**: No package manager, no build step, no runtime required beyond a static file server.
