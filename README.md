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
  --level2-toc '//h:h3' \
  --no-default-epub-cover
```

When complete, `getting-real.epub` will be in the current directory — open it with your e-reader or import it into Calibre.

The script caches each chapter as an individual HTML file under `chapters/` so re-runs are fast and don't re-fetch pages that already exist.

## Output

- `chapters/` — one HTML file per chapter (91 total)
- `getting-real.html` — single combined HTML file
- `getting-real.epub` — final EPUB with full navigation TOC

## Troubleshooting

**`python3: command not found`**
Python 3 isn't installed or isn't on your PATH. On macOS, install it via [Homebrew](https://brew.sh): `brew install python`. On Linux, use your package manager: `sudo apt install python3` (Debian/Ubuntu) or `sudo pacman -S python` (Arch).

**`python3 -m venv` fails or `venv` module not found`**
Some Linux distributions ship Python without the venv module. Install it separately: `sudo apt install python3-venv` (Debian/Ubuntu).

**`ebook-convert: command not found`**
Calibre is installed but its CLI tools aren't on your PATH. On macOS, add this to your shell config (`~/.zshrc` or `~/.bashrc`):
```sh
export PATH="/Applications/Calibre.app/Contents/MacOS:$PATH"
```
Then open a new terminal and try again. On Linux, installing Calibre via your package manager usually puts `ebook-convert` on PATH automatically.

**`ModuleNotFoundError: No module named 'bs4'` or `requests`**
The dependencies weren't installed, or you're running the script outside the virtual environment. Make sure you activated the venv first (`source .venv/bin/activate`) before running `pip install` and `python3 scrape.py`.

**Python version errors or unexpected behavior**
This script requires Python 3.8 or newer. Check your version with `python3 --version`. If it's older, install a newer version via Homebrew (macOS) or your package manager (Linux).

## Notes

The book is copyright ©1999-2025 37signals LLC. This script is provided for personal use only — to let you read a freely available book in a format that works better for you.
