# CLAUDE.md

## What This Is

A Python script that scrapes the Getting Real book website (https://basecamp.com/gettingreal) and compiles all 91 chapters into a single HTML file, then converts it to EPUB using Calibre.

## Key Files

- `scrape.py` — the scraper and HTML builder
- `chapters/` — cached per-chapter HTML (gitignored)
- `getting-real.html` — compiled output (gitignored)
- `getting-real.epub` — final EPUB (gitignored)

## Running

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install beautifulsoup4 requests
python3 scrape.py
ebook-convert getting-real.html getting-real.epub \
  --title 'Getting Real' --authors 'Basecamp (37signals)' \
  --language en --level1-toc '//h:h2' --no-default-epub-cover
```

## Architecture

`scrape.py` has three responsibilities:
1. `get_chapter_urls()` — fetches the index page and extracts all `/gettingreal/NN.N-slug` hrefs in order
2. `scrape_chapter(url)` — fetches a chapter, extracts `div.content`, strips Stimulus `<template>` tags, buttons, nav elements, and the `footer__copyright` element
3. `build_epub_html(chapters)` — assembles a single valid HTML document with the copyright notice on the title page and all chapters as `<h2>`-headed sections

Chapters are cached to `chapters/<slug>.html` so re-runs skip already-fetched pages.

## Known Details

- `resp.content.decode("utf-8")` is used instead of `resp.text` to avoid requests misdetecting the charset and double-encoding smart quotes
- Copyright appears once on the opening page and is stripped from each chapter's footer
- Calibre auto-generates a 217-entry navigation TOC from the heading hierarchy
