"""Download licensed HTML snapshots; count contiguous >=1500-character units."""
from __future__ import annotations

import re
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from .common import ROOT, now, sha256, write_json, write_jsonl

SOURCES = [
    ("tutorial_controlflow", "tutorial/controlflow.html", "tutorial"),
    ("tutorial_datastructures", "tutorial/datastructures.html", "tutorial"),
    ("tutorial_modules", "tutorial/modules.html", "tutorial"),
    ("tutorial_inputoutput", "tutorial/inputoutput.html", "tutorial"),
    ("tutorial_errors", "tutorial/errors.html", "tutorial"),
    ("tutorial_classes", "tutorial/classes.html", "tutorial"),
    ("library_json", "library/json.html", "library_reference"),
    ("library_csv", "library/csv.html", "library_reference"),
    ("library_pathlib", "library/pathlib.html", "library_reference"),
]


def normalize_text(text):
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = text.replace("\u00a0", " ").expandtabs(4)
    lines = [line.rstrip() for line in text.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def extract_html(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.select_one('div.body[role="main"]') or soup.select_one("div.body")
    if body is None:
        raise ValueError("Missing document body; refusing to index navigation")
    for junk in body.select("script, style, nav, .headerlink, .viewcode-link, .toctree-wrapper"):
        junk.decompose()
    blocks = []
    for tag in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "dt", "li"]):
        if tag.find_parent(["pre", "dt", "p"]):
            continue
        if tag.name == "li" and tag.find(["p", "pre", "li"]):
            continue
        text = tag.get_text() if tag.name == "pre" else tag.get_text(" ", strip=True)
        text = normalize_text(text)
        if text:
            blocks.append(text)
    text = normalize_text("\n\n".join(blocks))
    title = body.find("h1").get_text(" ", strip=True)
    return title, text, blocks, soup.title.get_text() if soup.title else ""


def unit_bounds(text, target=3500, minimum=1500):
    """Partition without duplication; keep delimiters, merge a short final unit."""
    ends = [m.end() for m in re.finditer(r"\n\n", text)] + [len(text)]
    ranges, start = [], 0
    for end in ends:
        if len(text[start:end].strip()) >= target:
            ranges.append([start, end])
            start = end
    if start < len(text):
        if len(text[start:].strip()) < minimum and ranges:
            ranges[-1][1] = len(text)
        else:
            ranges.append([start, len(text)])
    if not ranges or any(len(text[a:b].strip()) < minimum for a, b in ranges):
        raise ValueError("Source too short for the declared unit counting rule")
    return ranges


def download(url, path):
    if path.exists():
        return "cached snapshot"
    response = requests.get(url, timeout=60, headers={"User-Agent": "Day06-Educational-Ingestion/1.0"})
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return response.url


def ingest():
    started = time.perf_counter()
    raw = ROOT / "data/raw"
    raw.mkdir(parents=True, exist_ok=True)
    manifest, pages, events = [], [], []
    for doc_id, relative, doc_type in SOURCES:
        url = "https://docs.python.org/3.13/" + relative
        path = raw / (doc_id + ".html")
        try:
            resolved = download(url, path)
            title, text, blocks, html_title = extract_html(path.read_text(encoding="utf-8"))
            normalized = ROOT / "data/normalized" / (doc_id + ".txt")
            normalized.parent.mkdir(parents=True, exist_ok=True)
            normalized.write_text(text, encoding="utf-8")
            units = []
            for number, (start, end) in enumerate(unit_bounds(text), 1):
                page_id = f"{doc_id}:u{number:03d}"
                unit = text[start:end].strip()
                leading = len(text[start:end]) - len(text[start:end].lstrip())
                offset = start + leading
                page = {"document_id": doc_id, "source": url, "page": page_id,
                        "text": unit, "start": offset, "end": offset + len(unit),
                        "boundary_start": start, "boundary_end": end,
                        "metadata": {"document_type": doc_type, "version": "3.13", "language": "en", "title": title}}
                pages.append(page)
                units.append({"page_id": page_id, "start": offset, "end": offset + len(unit),
                              "boundary_start": start, "boundary_end": end, "normalized_chars": len(unit)})
            manifest.append({"source_id": doc_id, "title": title, "html_title": html_title,
                "source_path_or_url": url, "snapshot_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "normalized_path": str(normalized.relative_to(ROOT)).replace("\\", "/"),
                "license_or_permission": "PSF-2.0; example code additionally available under 0BSD",
                "license_url": "https://docs.python.org/3.13/license.html", "accessed_at": now(),
                "raw_sha256": sha256(path), "normalized_sha256": sha256(normalized),
                "document_type": doc_type, "version": "3.13", "normalized_chars": len(text),
                "page_count": len(units), "pages": units})
            events.append({"source_id": doc_id, "status": "ok", "resolved_url": resolved,
                           "units": len(units), "blocks": len(blocks), "chars": len(text)})
            print(f"Ingested {doc_id}: {len(units)} units / {len(text)} chars", flush=True)
        except Exception as error:
            events.append({"source_id": doc_id, "status": "error", "error": str(error)})
            write_json("results/ingestion_log.json", {"events": events, "completed": False})
            raise
    license_path = raw / "python_license.html"
    download("https://docs.python.org/3.13/license.html", license_path)
    write_json("data/manifest.json", {"created_at": now(), "counting_rule":
        "HTML body only; contiguous ordered paragraph-boundary units target 3500, minimum 1500 normalized characters; merge short tail. No duplicates. Units are not physical PDF pages.",
        "excluded": ["navigation", "sidebar", "footer", "table of contents wrapper", "scripts/styles", "license page (retained as legal notice, not counted)"],
        "normalization": "NFC, NBSP to space, LF, tabs to four spaces, trailing-space removal, max one empty line; code indentation preserved.",
        "modifications": "HTML content extracted and reformatted as plain text; partitioned and chunked. Original snapshots and license retained.",
        "license_snapshot_sha256": sha256(license_path), "total_content_units": len(pages), "sources": manifest})
    write_jsonl("data/pages.jsonl", pages)
    write_json("results/ingestion_log.json", {"events": events, "completed": True,
        "empty_units": 0, "ocr": "not applicable: born-digital HTML", "elapsed_seconds": time.perf_counter()-started})


if __name__ == "__main__":
    ingest()
