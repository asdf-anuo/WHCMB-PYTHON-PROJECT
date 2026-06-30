# AGENTS.md

## Cursor Cloud specific instructions

This repo is a small Python project that scrapes the Wuhan city message board
(武汉城市留言板) public API, plus a single static HTML query/visualization page.
There is no build step and no automated test suite.

### Components
- **Scraper (Python):** `start.py` → `eur.py` (logic) + `config.py` (settings),
  with `keywords.txt`/`cookie.txt` as inputs. Saves results to a timestamped
  `wuhan_comments_*.xlsx`. Run/setup commands are in `README.md`.
- **Query page (static HTML):** `message_board_query.html` is a Vue 3 + Element
  Plus single file that calls the live API directly from the browser via `fetch`.
  Dependencies load from CDN; no bundler.
- `design/` holds static design-mockup HTML and docs (no runtime role).

### Environment / running
- Python deps (`pandas`, `requests`, `openpyxl`) are installed into a `.venv` by
  the startup update script. Run Python with `.venv/bin/python` (e.g.
  `.venv/bin/python start.py`, `.venv/bin/python test_api.py`).
- The scraper and the HTML page both hit the live API at
  `https://api1-liuyan.cjn.cn/...`. As of setup this API is reachable from the
  cloud VM, returns `code:0` with real data, and works **without a valid Cookie**
  (the bundled Cookie in `config.py`/`cookie.txt` may be expired but is not
  required for basic queries). The API also returns permissive CORS headers, so
  the browser page works from `localhost`.
- Serve the HTML page with a static server, then open it, e.g.
  `python3 -m http.server 8000` and visit
  `http://localhost:8000/message_board_query.html`. Opening it via `file://`
  also works for the fetch calls.

### Gotchas
- `config.py` defaults to `MAX_PAGES = 1000` with 2–5s random delays, so a full
  `start.py` run crawls the entire dataset and takes a very long time. For quick
  verification, override at runtime (set `config.MAX_PAGES`/`PAGE_SIZE` small and
  `MIN_DELAY=MAX_DELAY=0`) rather than editing `config.py`.
- There is no linter configured; `python -m py_compile` and `pyflakes` work for
  basic checks. Existing pyflakes warnings (unused `json` import, f-strings
  without placeholders in `eur.py`) are pre-existing and harmless.
