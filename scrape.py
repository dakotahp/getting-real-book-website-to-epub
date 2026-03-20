#!/usr/bin/env python3
"""
Scrape Getting Real (https://basecamp.com/gettingreal) and compile into
a single clean HTML file suitable for conversion to EPUB via Calibre.
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://basecamp.com"
INDEX_URL = f"{BASE_URL}/gettingreal"
OUT_DIR = Path(__file__).parent / "chapters"
EPUB_HTML = Path(__file__).parent / "getting-real.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

def get_chapter_urls():
    resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
    seen = set()
    urls = []
    for a in soup.find_all("a", href=re.compile(r"^/gettingreal/\d")):
        href = a["href"]
        if href not in seen:
            seen.add(href)
            urls.append(BASE_URL + href)
    return urls

def scrape_chapter(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    # Force UTF-8 decode from raw bytes to avoid requests mis-detecting charset
    soup = BeautifulSoup(resp.content.decode("utf-8"), "html.parser")

    # --- Title / chapter heading ---
    masthead = soup.select_one(".intro__masthead")
    title_tag = soup.select_one(".intro__title")
    chapter_label = masthead.get_text(strip=True) if masthead else ""
    chapter_title = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1]

    # --- Prose content ---
    content_div = soup.select_one("div.content")
    if not content_div:
        return None, chapter_label, chapter_title

    # Remove Stimulus template elements, nav/button noise, and footer copyright
    for tag in content_div.find_all(["template", "button", "nav"]):
        tag.decompose()
    for tag in content_div.find_all(class_="footer__copyright"):
        tag.decompose()

    # Remove anchor icon links injected by JS (they render as empty <a> tags)
    for a in content_div.find_all("a", class_="anchor"):
        a.decompose()

    # Grab inner HTML as a string
    inner_html = content_div.decode_contents().strip()
    return inner_html, chapter_label, chapter_title

def build_epub_html(chapters):
    parts = ["""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Getting Real — Basecamp</title>
</head>
<body>
  <h1>Getting Real</h1>
  <p><em>by Basecamp (37signals)</em></p>
  <p><em>Copyright &#169;1999-2025 37signals LLC. All rights reserved.</em></p>
"""]

    for slug, chapter_label, chapter_title, html in chapters:
        anchor = slug.replace("/gettingreal/", "").replace("-", "_")
        header = f'<h2 id="{anchor}">'
        if chapter_label:
            header += f'<small>{chapter_label}</small><br/>'
        header += f'{chapter_title}</h2>'
        parts.append(header)
        parts.append(html)
        parts.append("")

    parts.append("</body>\n</html>")
    return "\n".join(parts)

def main():
    OUT_DIR.mkdir(exist_ok=True)

    print("Fetching chapter list...")
    urls = get_chapter_urls()
    print(f"Found {len(urls)} chapters.")

    chapters = []
    for i, url in enumerate(urls, 1):
        slug = url.replace(BASE_URL, "")
        cache_file = OUT_DIR / (slug.replace("/gettingreal/", "") + ".html")

        if cache_file.exists():
            print(f"[{i:2}/{len(urls)}] (cached) {slug}")
            raw = cache_file.read_text()
            # Re-parse cached file to extract label/title
            soup = BeautifulSoup(f"<div>{raw}</div>", "html.parser")
            h2 = soup.find("h2")
            label = ""
            title = slug.split("/")[-1]
            if h2:
                small = h2.find("small")
                label = small.get_text(strip=True) if small else ""
                if small:
                    small.decompose()
                title = h2.get_text(strip=True)
            # Read the content after the h2
            content_html = cache_file.read_text()
            chapters.append((slug, label, title, content_html))
            continue

        print(f"[{i:2}/{len(urls)}] Scraping {slug}")
        try:
            html, label, title = scrape_chapter(url)
            if html:
                cache_file.write_text(html)
                chapters.append((slug, label, title, html))
            else:
                print(f"  WARNING: no content found for {url}")
        except Exception as e:
            print(f"  ERROR: {e}")

        time.sleep(0.5)  # polite delay

    print(f"\nBuilding combined HTML → {EPUB_HTML}")
    epub_html = build_epub_html(chapters)
    EPUB_HTML.write_text(epub_html)
    print(f"Written: {EPUB_HTML} ({EPUB_HTML.stat().st_size // 1024} KB)")

    print("\nTo convert to EPUB with Calibre:")
    print(f"  ebook-convert '{EPUB_HTML}' getting-real.epub \\")
    print(f"    --title 'Getting Real' \\")
    print(f"    --authors 'Basecamp (37signals)' \\")
    print(f"    --language en \\")
    print(f"    --level1-toc '//h:h2' \\")
    print(f"    --no-default-epub-cover")

if __name__ == "__main__":
    main()
