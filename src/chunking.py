from __future__ import annotations

import hashlib
import re
import numpy as np
from .common import read_jsonl, write_json, write_jsonl

CONFIGS = {
    "A": {"method": "fixed", "size_chars": 500, "overlap_chars": 50, "filter": False, "collection": "day06_A"},
    "B": {"method": "paragraph", "max_chars": 1000, "overlap_chars": 0, "filter": False, "collection": "day06_B"},
    "C": {"method": "paragraph", "max_chars": 1000, "overlap_chars": 0, "filter": True, "collection": "day06_B"},
}


def fixed_ranges(text, size=500, overlap=50):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Expected size > 0 and 0 <= overlap < size")
    result, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        result.append((start, end))
        if end == len(text):
            break
        start = end - overlap
    return result


def paragraph_ranges(text, maximum=1000):
    """Greedy paragraphs; split only overlong blocks at whitespace. No lost text."""
    if maximum < 2:
        raise ValueError("maximum must be >=2")
    ranges, start, end = [], 0, 0
    boundaries = [m.end() for m in re.finditer(r"\n\n", text)] + [len(text)]
    for boundary in boundaries:
        if boundary - start <= maximum:
            end = boundary
            continue
        if end > start:
            ranges.append((start, end))
            start = end
        while boundary - start > maximum:
            stop = text.rfind(" ", start + maximum // 2, start + maximum)
            stop = stop + 1 if stop != -1 else start + maximum
            ranges.append((start, stop))
            start = stop
        end = boundary
    if end > start:
        ranges.append((start, end))
    return ranges


def make_chunks(pages, strategy):
    chunks = []
    for page in pages:
        text = page["text"]
        ranges = fixed_ranges(text) if strategy == "A" else paragraph_ranges(text)
        for start, end in ranges:
            content = text[start:end]
            fingerprint = f"{strategy}|{page['page']}|{start}|{end}|{content}"
            chunks.append({"chunk_id": hashlib.sha256(fingerprint.encode()).hexdigest()[:32],
                "document_id": page["document_id"], "source": page["source"], "page": page["page"],
                "text": content, "start": start, "end": end, "source_start": page["start"]+start,
                "source_end": page["start"]+end, "metadata": page["metadata"]})
    return chunks


def build():
    pages = read_jsonl("data/pages.jsonl")
    stats = {}
    for strategy in ("A", "B"):
        chunks = make_chunks(pages, strategy)
        lengths = [len(c["text"]) for c in chunks]
        stats[strategy] = {"chunk_count": len(chunks), "characters_including_overlap": sum(lengths),
            "min_chars": min(lengths), "median_chars": float(np.median(lengths)),
            "p95_chars": float(np.percentile(lengths, 95)), "max_chars": max(lengths)}
        write_jsonl(f"results/chunks_{strategy}.jsonl", chunks)
    stats["C"] = {**stats["B"], "shared_index": "B; no duplicate storage or embedding"}
    write_json("results/chunk_stats.json", stats)
    return stats
