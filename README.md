# Getting Real → EPUB

Scrapes the [Getting Real](https://basecamp.com/gettingreal) book website published by Basecamp (37signals) and compiles it into an EPUB file.

The scraped content and generated files are not included in this repo. Run the script yourself to generate them locally.

## Requirements

- Python 3
- [Calibre](https://calibre-ebook.com/) (for the `ebook-convert` CLI tool)

## Usage

```sh
# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4 requests

# Scrape all 91 chapters and build the combined HTML
python3 scrape.py

# Convert to EPUB (Calibre)
ebook-convert getting-real.html getting-real.epub \
  --title 'Getting Real' \
  --authors 'Basecamp (37signals)' \
  --language en \
  --level1-toc '//h:h2' \
  --no-default-epub-cover
```

The script caches each chapter as an individual HTML file under `chapters/` so re-runs are fast and don't re-fetch pages that already exist.

## Output

- `chapters/` — one HTML file per chapter (91 total)
- `getting-real.html` — single combined HTML file
- `getting-real.epub` — final EPUB with full navigation TOC

## Notes

The book is copyright ©1999-2025 37signals LLC. This script is provided for personal use only — to let you read a freely available book in a format that works better for you.
