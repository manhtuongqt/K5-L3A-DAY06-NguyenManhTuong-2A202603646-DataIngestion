"""Author source-backed gold before running retrieval; immutable checksummed lock."""
from __future__ import annotations

from .common import ROOT, now, read_json, read_jsonl, sha256, write_json
from .chunking import CONFIGS

# (document, question, answer, evidence paragraph selector, optional subquote start/end, filter)
SPECS = [
 ("tutorial_datastructures", "What happens if list.remove(value) cannot find that value?", "It raises ValueError.", "Remove the first item", None, None, None),
 ("tutorial_datastructures", "In the tutorial, which container supports a queue with fast appends and pops at either end?", "collections.deque.", "To implement a queue", None, None, "tutorial"),
 ("tutorial_datastructures", "Under what condition can a tuple be used as a dictionary key, and what disqualifies it?", "Its contents must be immutable; a mutable object directly or indirectly inside it disqualifies it.", "Tuples can be used", "Tuples can be used", "it cannot be used as a key.", None),
 ("tutorial_datastructures", "How can I test whether a single key is present in a dictionary?", "Use the in keyword.", "To check whether", "To check whether", "use the in keyword.", None),
 ("tutorial_datastructures", "How can I iterate over a sequence's distinct elements in sorted order?", "Combine sorted() with set().", "Using set()", None, None, None),
 ("tutorial_controlflow", "According to the tutorial, why can a list used as a default argument keep values between function calls?", "The default is evaluated only once, so the mutable default can accumulate arguments across calls.", "Important warning", None, None, "tutorial"),
 ("tutorial_controlflow", "Does range include its specified end point?", "No; the given end point is excluded.", "The given end point", "The given end point", "generated sequence;", None),
 ("tutorial_controlflow", "When does the else clause of a for or while loop execute in relation to break?", "When the loop finishes without executing break.", "If the loop finishes without", None, None, None),
 ("tutorial_modules", "When a module file is executed as a script, what value is assigned to __name__?", "__main__.", "the __name__ set", None, None, None),
 ("tutorial_modules", "What names does from module import * exclude, and why is this generally discouraged?", "It excludes names starting with underscore and may introduce unknown names that hide existing names.", "This imports all names except", None, None, None),
 ("tutorial_modules", "Where does Python cache a module's compiled code to speed loading?", "In the __pycache__ directory.", "To speed up loading modules", "To speed up loading modules", "in the __pycache__ directory", None),
 ("tutorial_inputoutput", "In the tutorial's file handling guidance, what encoding is recommended for text files unless another is needed?", "Explicit encoding='utf-8'.", "Because UTF-8", "Because UTF-8", "use a different encoding.", "tutorial"),
 ("tutorial_inputoutput", "Why should I use with when working with a file, even if the block may raise an exception?", "The file is properly closed when the suite finishes, even if an exception occurs.", "It is good practice", "It is good practice", "point.", None),
 ("tutorial_inputoutput", "What is the name for converting a Python data hierarchy into a JSON string, and the reverse operation?", "Serializing and deserializing, respectively.", "called serializing", "The standard module", "called deserializing .", None),
 ("tutorial_errors", "Why put success-only code in try/except's else clause rather than inside try?", "It avoids accidentally catching exceptions from code outside the intended protected operation.", "The use of the else clause is better", None, None, None),
 ("library_json", "In the library reference, what resource risk comes from parsing untrusted JSON, and what precaution is advised?", "A malicious JSON string may consume considerable CPU and memory; limit the size of input.", "Be cautious when parsing JSON", None, None, "library_reference"),
 ("library_json", "In the library reference, why do repeated json.dump calls on the same file produce invalid JSON?", "JSON is not a framed protocol; repeated serialization of multiple objects to the same file is invalid.", "JSON is not a framed protocol", None, None, "library_reference"),
 ("library_json", "What does the standard JSON decoder do by default when an object repeats the same property name?", "It does not raise an exception and retains only the last name-value pair.", "The RFC specifies that the names", None, None, None),
 ("library_csv", "How is Python None written by csv.writer, and is that conversion reversible?", "As an empty string; this is not reversible.", "value None is written", "To make it", "CSV files without preprocessing the data returned from a cursor.fetch* call.", None),
 ("library_pathlib", "In the library reference, does Path.mkdir(exist_ok=True) accept an existing path that is a regular file rather than a directory?", "No; FileExistsError is still raised if the path exists and is not a directory.", "If exist_ok is true", None, None, "library_reference"),
]


def build():
    if (ROOT / "benchmark/lock.json").exists():
        verify_lock()
        print("Existing benchmark lock retained; not regenerated")
        return
    pages = read_jsonl("data/pages.jsonl")
    questions = []
    for i, (doc, question, answer, selector, start_text, end_text, scope) in enumerate(SPECS):
        source_text = (ROOT / f"data/normalized/{doc}.txt").read_text(encoding="utf-8")
        matches = [p for p in source_text.split("\n\n") if selector in p]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous or missing source paragraph {doc}: {selector!r} ({len(matches)})")
        quote = matches[0]
        if start_text:
            quote = quote[quote.index(start_text):]
        if end_text:
            quote = quote[:quote.index(end_text)+len(end_text)]
        alternatives = [{"source_id": p["document_id"], "page": p["page"], "evidence_quote": quote,
                         "source": p["source"], "page_start": p["text"].index(quote)}
                        for p in pages if quote in p["text"]]
        if not alternatives:
            raise ValueError(f"Gold absent from any complete source unit: {doc}")
        split = "dev" if i < 15 else "test"
        qid = f"D{i+1:02d}" if split == "dev" else f"T{i-14:02d}"
        questions.append({"id": qid, "split": split, "question": question, "expected_answer": answer,
            "gold_source_id": alternatives[0]["source_id"], "gold_page": alternatives[0]["page"],
            "evidence_quote": quote, "gold_alternatives": alternatives,
            "filter": {"document_type": scope} if scope else {},
            "filter_origin": "Explicit tutorial/library-reference scope in the question, supplied before retrieval" if scope else "none",
            "gold_validation": "AI authored; exact substring verified in normalized snapshot; human semantic review pending"})
    anchors = [{"page": p["page"], "offset": min(200, len(p["text"])-1)} for p in sorted(pages, key=lambda p: p["page"])[:10]]
    write_json("benchmark/questions.json", questions)
    write_json("benchmark/protocol.json", {"frozen_at": now(), "configs": CONFIGS,
        "split_rule": "D01-D15: tutorial chapters; T01-T05: library reference (JSON/CSV/pathlib), source-disjoint from dev but same corpus. Authored together before retrieval.",
        "selection_rule": ["maximize dev Evidence Hit@3", "then maximize dev Hit@1", "then minimize average dev search latency", "then alphabetical strategy"],
        "audit_anchors": anchors, "anchor_rule": "First 10 lexically sorted page IDs; character offset 200; choose earliest containing chunk if overlap.",
        "metadata_audit": "All 5 test questions x top-3 for each A/B/C; compare with source pages and offsets.",
        "grounding_audit": "All 5 test questions x A/B/C. 0=no evidence; 1=partial/missing condition or context; 2=enough evidence and traceability. Human confirms.",
        "coherence_scale": "0=broken meaning/missing subject; 1=partly interpretable/context missing; 2=self-contained complete idea. Human confirms.",
        "hit_definition": "One top-ranked chunk must have a gold source AND page AND contain the complete recorded evidence. Not a union across chunks. Human-confirmed equivalent evidence may be recorded separately, without overwriting strict scores.",
        "holdout_policy": "Select on dev before opening test outputs; no test-based tuning. Refuse overwrite of runs. Bug fixes after exposure require disclosure and archived prior results.",
        "language": "English questions and English corpus; report in Vietnamese", "seed": None,
        "seed_reason": "No random split, random sampling or stochastic model sampling; deterministic anchors and exact retrieval.",
        "human_review_status": "pending; proposed labels never count as confirmed human audit"})
    paths = ["data/pages.jsonl", "data/manifest.json", "benchmark/questions.json", "benchmark/protocol.json", "benchmark/model.json"]
    write_json("benchmark/lock.json", {"locked_at": now(), "sha256": {p: sha256(ROOT/p) for p in paths}})
    print(f"Frozen {len(questions)} questions; {sum(bool(q['filter']) for q in questions)} filters", flush=True)


def verify_lock():
    lock = read_json("benchmark/lock.json")
    for path, expected in lock["sha256"].items():
        if sha256(ROOT/path) != expected:
            raise ValueError(f"Frozen input changed: {path}")
    return lock
