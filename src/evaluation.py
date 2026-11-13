"""Strict source/page plus full-quote scoring; no answer generation or LLM judge."""
from __future__ import annotations


def is_hit(question, chunk):
    return any(chunk["document_id"] == g["source_id"] and chunk["page"] == g["page"]
               and g["evidence_quote"] in chunk["text"] for g in question["gold_alternatives"])


def summarize(traces):
    result = {}
    for strategy in ("A", "B", "C"):
        subset = [t for t in traces if t["strategy"] == strategy]
        n = len(subset)
        if not n:
            continue
        filtered = [t for t in subset if t["question"]["filter"]]
        hit1 = sum(t["hit_at_1"] for t in subset)
        hit3 = sum(t["evidence_hit_at_3"] for t in subset)
        result[strategy] = {"questions": n, "hit_at_1": {"n": hit1, "N": n, "rate": hit1/n},
            "evidence_hit_at_3": {"n": hit3, "N": n, "rate": hit3/n},
            "filter_compliance": {"n": sum(t["filter_compliant"] for t in filtered), "N": len(filtered)} if filtered else None,
            "mean_search_ms": sum(t["search_ms"] for t in subset)/n,
            "filter_applied_count": sum(bool(t["applied_filter"]) for t in subset)}
    return result
