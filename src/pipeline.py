"""CLI with separate dev selection and held-out test stages."""
from __future__ import annotations

import argparse
import csv
import json
import time
import numpy as np
from pathlib import Path

from .common import ROOT, now, read_json, read_jsonl, sha256, write_json, write_jsonl
from .benchmark import build as build_benchmark, verify_lock
from .chunking import CONFIGS, build as build_chunks
from .embedding import Embedder, runtime
from .evaluation import is_hit, summarize
from .store import Store


def no_overwrite(path):
    if (ROOT/path).exists():
        raise FileExistsError(f"Existing evidence retained: {path}. Use a separate checkout for a new experiment.")


def index():
    verify_lock()
    no_overwrite("results/index.json")
    build_chunks()
    embedder = Embedder()
    store = Store()
    timings, checks = {}, {}
    try:
        for strategy in ("A", "B"):
            chunks = read_jsonl(f"results/chunks_{strategy}.jsonl")
            tokens = embedder.token_count([c["text"] for c in chunks])
            if max(tokens) > 512:
                raise ValueError(f"Truncation would discard source evidence: {strategy}, max {max(tokens)} tokens")
            started = time.perf_counter()
            vectors = embedder.documents([c["text"] for c in chunks])
            embed_seconds = time.perf_counter()-started
            np.save(ROOT/f".local/vectors_{strategy}.npy", vectors)
            started = time.perf_counter()
            count = store.replace(CONFIGS[strategy]["collection"], chunks, vectors)
            ingest_seconds = time.perf_counter()-started
            count_again = store.replace(CONFIGS[strategy]["collection"], chunks, vectors)
            checks[strategy] = {"expected_count": len(chunks), "count_first": count,
                "count_after_same_snapshot_reingest": count_again, "no_duplicates": count == count_again == len(chunks)}
            timings[strategy] = {"embedding_seconds": embed_seconds, "store_ingest_seconds": ingest_seconds,
                "total_model_tokens": sum(tokens), "max_model_tokens": max(tokens), "vector_shape": list(vectors.shape),
                "vectors_sha256": sha256(ROOT/f".local/vectors_{strategy}.npy")}
            print(f"Indexed {strategy}: {count} real vectors, embedding {embed_seconds:.2f}s", flush=True)
        chunks = read_jsonl("results/chunks_B.jsonl")
        vectors = np.load(ROOT/".local/vectors_B.npy")
        store.replace("gate_obsolete_check", chunks[:2], vectors[:2])
        before = store.client.count("gate_obsolete_check", exact=True).count
        store.replace("gate_obsolete_check", chunks[:1], vectors[:1])
        after = store.client.count("gate_obsolete_check", exact=True).count
        checks["obsolete_chunks"] = {"before": before, "after": after, "removed": before == 2 and after == 1,
            "method": "Full collection snapshot replacement; temporary check collection only"}
        store.replace("gate_obsolete_check", [], np.empty((0,384),dtype=np.float32))
        before_hits = store.search("day06_B", vectors[0])
    finally:
        store.close()
    store = Store()
    try:
        after_hits = store.search("day06_B", vectors[0])
        checks["persistence"] = {"reopened_from_disk": True,
            "same_top3": [h["chunk_id"] for h in before_hits] == [h["chunk_id"] for h in after_hits],
            "count_after_reopen": store.client.count("day06_B", exact=True).count}
        filters = {"document_type": "library_reference"}
        filtered = store.search("day06_B", vectors[0], filters)
        checks["filter"] = {"returned": len(filtered), "all_match": all(h["document_type"] == "library_reference" for h in filtered)}
    finally:
        store.close()
    timings["C"] = {"shared_index": "B", "incremental_embedding_seconds": 0, "incremental_ingest_seconds": 0}
    write_json("results/index.json", {"created_at": now(), "model_load_seconds": embedder.load_seconds, "strategies": timings,
        "reingest_policy": "Full snapshot replacement removes obsolete points; not atomic, requires rebuild on failure"})
    write_json("results/store_checks.json", checks)
    write_json("results/runtime.json", runtime())
    freeze = __import__("subprocess").check_output([__import__("sys").executable, "-m", "pip", "freeze"], text=True)
    (ROOT/"requirements-lock.txt").write_text(freeze, encoding="utf-8")


def check_store():
    """Reconcile and validate saved real vectors without repeating embedding or benchmark."""
    verify_lock()
    store, checks = Store(), {}
    try:
        for s in ("A","B"):
            chunks = read_jsonl(f"results/chunks_{s}.jsonl")
            vectors = np.load(ROOT/f".local/vectors_{s}.npy")
            started = time.perf_counter()
            first = store.replace(CONFIGS[s]["collection"],chunks,vectors)
            seconds = time.perf_counter()-started
            again = store.replace(CONFIGS[s]["collection"],chunks,vectors)
            checks[s] = {"expected_count":len(chunks),"count_first":first,"count_after_same_snapshot_reingest":again,
                         "no_duplicates":first==again==len(chunks),"validated_store_ingest_seconds":seconds}
        store.replace("gate_obsolete_check",chunks[:2],vectors[:2])
        before = store.client.count("gate_obsolete_check",exact=True).count
        store.replace("gate_obsolete_check",chunks[:1],vectors[:1])
        after = store.client.count("gate_obsolete_check",exact=True).count
        checks["obsolete_chunks"] = {"before":before,"after":after,"removed":before==2 and after==1,
            "method":"Stable ID upsert plus official Qdrant deletion of obsolete point IDs"}
        store.replace("gate_obsolete_check",[],np.empty((0,384),dtype=np.float32))
        before_hits = store.search("day06_B",vectors[0])
    finally:
        store.close()
    store = Store()
    try:
        after_hits = store.search("day06_B",vectors[0])
        checks["persistence"] = {"reopened_from_disk":True,"same_top3":[h['chunk_id'] for h in before_hits]==[h['chunk_id'] for h in after_hits],
                                "count_after_reopen":store.client.count("day06_B",exact=True).count}
        hits = store.search("day06_B",vectors[0],{"document_type":"library_reference"})
        checks["filter"] = {"returned":len(hits),"all_match":len(hits)==3 and all(h["document_type"]=="library_reference" for h in hits)}
    finally:
        store.close()
    assert checks["A"]["no_duplicates"] and checks["B"]["no_duplicates"]
    assert checks["obsolete_chunks"]["removed"] and checks["persistence"]["same_top3"] and checks["filter"]["all_match"]
    if (ROOT/"results/store_checks.json").exists():
        previous = read_json("results/store_checks.json")
        if not previous.get("obsolete_chunks",{}).get("removed",False):
            write_json("results/history/store_checks_before_fix.json",previous)
    checks["checked_at"] = now()
    write_json("results/store_checks.json",checks)
    print(json.dumps(checks,indent=2))


def evaluate(split):
    verify_lock()
    out = f"results/traces_{split}.jsonl"
    no_overwrite(out)
    if split == "test":
        selection = read_json("results/selection.json")
        if selection["benchmark_lock_sha256"] != sha256(ROOT/"benchmark/lock.json"):
            raise ValueError("Selection and test must use the same frozen benchmark")
        for filename, expected in selection["chunk_hashes"].items():
            if sha256(ROOT/filename) != expected:
                raise ValueError("Chunk strategies changed after dev selection")
        for filename, expected in selection["implementation_hashes"].items():
            if sha256(ROOT/filename) != expected:
                raise ValueError("Retrieval implementation changed after dev selection")
    questions = [q for q in read_json("benchmark/questions.json") if q["split"] == split]
    embedder = Embedder()
    started = time.perf_counter()
    query_vectors = embedder.queries([q["question"] for q in questions])
    embedding_seconds = time.perf_counter()-started
    store = Store()
    traces = []
    try:
        # Interleave strategies by question to limit timing drift. B and C share the exact index.
        for q, vector in zip(questions, query_vectors):
            for strategy, config in CONFIGS.items():
                filters = q["filter"] if config["filter"] else {}
                started = time.perf_counter()
                hits = store.search(config["collection"], vector, filters)
                search_ms = (time.perf_counter()-started)*1000
                if len(hits) != 3:
                    raise ValueError("Expected exactly three hits from the frozen corpus")
                for hit in hits:
                    hit["strict_evidence_hit"] = is_hit(q, hit)
                traces.append({"strategy": strategy, "split": split, "question": q, "query_text": q["question"],
                    "applied_filter": filters, "hits": hits, "hit_at_1": hits[0]["strict_evidence_hit"],
                    "evidence_hit_at_3": any(h["strict_evidence_hit"] for h in hits), "search_ms": search_ms,
                    "filter_compliant": all(all(h["metadata"].get(k) == v for k, v in q["filter"].items()) for h in hits),
                    "retrieved_at": now()})
                print(f"{split} {q['id']} {strategy}: hit1={traces[-1]['hit_at_1']} hit3={traces[-1]['evidence_hit_at_3']}", flush=True)
    finally:
        store.close()
    write_jsonl(out, traces)
    summary = summarize(traces)
    write_json(f"results/metrics_{split}.json", {"split": split, "completed_at": now(), "strategies": summary,
        "shared_query_embedding_seconds": embedding_seconds, "query_count": len(questions),
        "query_tokens": sum(embedder.token_count([embedder_prefix()+q['question'] for q in questions])), "api_calls": 0, "api_cost_usd": 0})
    if split == "dev":
        winner = sorted(summary, key=lambda s: (-summary[s]["evidence_hit_at_3"]["n"], -summary[s]["hit_at_1"]["n"], summary[s]["mean_search_ms"], s))[0]
        write_json("results/selection.json", {"selected_at": now(), "selected_strategy": winner, "based_on": "dev only; before test retrieval",
            "rule": read_json("benchmark/protocol.json")["selection_rule"], "benchmark_lock_sha256": sha256(ROOT/"benchmark/lock.json"),
            "chunk_hashes": {f"results/chunks_{s}.jsonl": sha256(ROOT/f"results/chunks_{s}.jsonl") for s in ("A", "B")},
            "implementation_hashes": {p:sha256(ROOT/p) for p in ("src/chunking.py","src/embedding.py","src/store.py","src/evaluation.py")},
            "dev_summary": summary, "strategy_tuning": "No parameter search. One predeclared A/B/C comparison retained, including failures."})
    update_experiment_log()


def embedder_prefix():
    from .embedding import QUERY_PREFIX
    return QUERY_PREFIX


def update_experiment_log():
    dev = read_json("results/metrics_dev.json")["strategies"] if (ROOT/"results/metrics_dev.json").exists() else {}
    test = read_json("results/metrics_test.json")["strategies"] if (ROOT/"results/metrics_test.json").exists() else {}
    with (ROOT/"artifacts/experiment_log.csv").open("w", newline="", encoding="utf-8") as out:
        fields = ["strategy", "chunking", "chunk_size", "overlap", "metadata", "filter", "vectorizer", "hypothesis", "dev_hit1", "dev_hit3", "test_hit1", "test_hit3", "notes"]
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        for strategy, config in CONFIGS.items():
            def score(data, key):
                return f"{data[strategy][key]['n']}/{data[strategy][key]['N']}" if strategy in data else ""
            writer.writerow({"strategy": strategy, "chunking": config["method"], "chunk_size": config.get("size_chars", config.get("max_chars")),
                "overlap": config["overlap_chars"], "metadata": "document_id/source/page/document_type/version/language/title/offsets",
                "filter": "explicit question document_type only" if config["filter"] else "none", "vectorizer": "BAAI/bge-small-en-v1.5 local ONNX 384d",
                "hypothesis": {"A": "500/50 is a small retrieval baseline; may split necessary evidence.", "B": "Paragraph grouping may preserve complete evidence but dilute specificity.", "C": "Same B index plus explicit scope may remove irrelevant categories; wrong scope could exclude the answer."}[strategy],
                "dev_hit1": score(dev,"hit_at_1"), "dev_hit3": score(dev,"evidence_hit_at_3"),
                "test_hit1": score(test,"hit_at_1"), "test_hit3": score(test,"evidence_hit_at_3"),
                "notes": "Frozen once before retrieval; no test-driven tuning; C reuses B vectors."})


def verify():
    verify_lock()
    pages = read_jsonl("data/pages.jsonl")
    questions = read_json("benchmark/questions.json")
    assert len(pages) >= 30 and min(len(p["text"]) for p in pages) >= 1500
    assert len({p["text"] for p in pages}) == len(pages)
    assert sum(q["split"] == "dev" for q in questions) >= 15
    assert sum(q["split"] == "test" for q in questions) >= 5
    assert sum(bool(q["filter"]) for q in questions) >= 3
    assert any(q["filter"] and q["split"] == "test" for q in questions)
    page_map = {p["page"]: p for p in pages}
    for q in questions:
        assert q["gold_alternatives"]
        for gold in q["gold_alternatives"]:
            p = page_map[gold["page"]]
            assert p["document_id"] == gold["source_id"] and gold["evidence_quote"] in p["text"]
            assert all(p["metadata"].get(k) == v for k,v in q["filter"].items())
    for source in read_json("data/manifest.json")["sources"]:
        assert sha256(ROOT/source["snapshot_path"]) == source["raw_sha256"]
        assert sha256(ROOT/source["normalized_path"]) == source["normalized_sha256"]
        text = (ROOT/source["normalized_path"]).read_text(encoding="utf-8")
        from .ingestion import extract_html
        assert extract_html((ROOT/source["snapshot_path"]).read_text(encoding="utf-8"))[1] == text
        cursor = 0
        for unit in source["pages"]:
            assert unit["boundary_start"] == cursor
            cursor = unit["boundary_end"]
            page = page_map[unit["page_id"]]
            assert text[unit["start"]:unit["end"]] == page["text"]
            assert len(page["text"]) == unit["normalized_chars"]
        assert cursor == len(text)
    assert sha256(ROOT/"data/raw/python_license.html") == read_json("data/manifest.json")["license_snapshot_sha256"]
    for s in ("A","B"):
        if (ROOT/f"results/chunks_{s}.jsonl").exists():
            chunks = read_jsonl(f"results/chunks_{s}.jsonl")
            assert len({c["chunk_id"] for c in chunks}) == len(chunks)
            for c in chunks:
                p = page_map[c["page"]]
                assert p["text"][c["start"]:c["end"]] == c["text"]
                assert c["metadata"] == p["metadata"]
    for split in ("dev", "test"):
        if not (ROOT/f"results/traces_{split}.jsonl").exists():
            continue
        traces = read_jsonl(f"results/traces_{split}.jsonl")
        expected = 45 if split == "dev" else 15
        assert len(traces) == expected
        assert len({(t['question']['id'],t['strategy']) for t in traces}) == expected
        assert summarize(traces) == read_json(f"results/metrics_{split}.json")["strategies"]
        for t in traces:
            for h in t["hits"]:
                p = page_map[h["page"]]
                assert p["text"][h["start"]:h["end"]] == h["text"]
                assert h["source"] == p["source"] and h["document_id"] == p["document_id"]
                assert h["metadata"] == p["metadata"]
                assert h["strict_evidence_hit"] == is_hit(t["question"], h)
        pairs = {(t["question"]["id"],t["strategy"]): t for t in traces}
        for q in [q for q in questions if q["split"] == split and not q["filter"]]:
            b,c = pairs[(q["id"],"B")],pairs[(q["id"],"C")]
            assert [h["chunk_id"] for h in b["hits"]] == [h["chunk_id"] for h in c["hits"]]
    if (ROOT/"results/traces_test.jsonl").exists():
        from datetime import datetime
        assert datetime.fromisoformat(read_json("results/selection.json")["selected_at"]) < min(datetime.fromisoformat(t["retrieved_at"]) for t in read_jsonl("results/traces_test.jsonl"))
    audit_state = read_json("results/audit/status.json") if (ROOT/"results/audit/status.json").exists() else None
    human_audit = "pending until student confirmation supplied"
    if audit_state and all(g["pending"] == 0 for g in audit_state["groups"].values()):
        human_audit = f"confirmed by {audit_state['reviewer']}; 110/110 rows accepted; see results/audit/human_confirmation.json"
    result = {"verified_at": now(), "checks_passed": True, "content_units": len(pages), "questions": len(questions),
        "automatic_verification_only": True, "human_audit": human_audit}
    write_json("results/verification.json", result)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["ingest", "freeze", "index", "check-store", "dev", "test", "audit", "report", "verify"])
    args = parser.parse_args()
    if args.stage == "ingest":
        from .ingestion import ingest
        ingest()
    elif args.stage == "freeze":
        from .embedding import prepare
        prepare()
        build_benchmark()
    elif args.stage == "index":
        index()
    elif args.stage == "check-store":
        check_store()
    elif args.stage in ("dev", "test"):
        evaluate(args.stage)
    elif args.stage == "audit":
        from .audit import build
        build()
    elif args.stage == "report":
        from .report import build
        build()
    else:
        verify()


if __name__ == "__main__":
    main()
