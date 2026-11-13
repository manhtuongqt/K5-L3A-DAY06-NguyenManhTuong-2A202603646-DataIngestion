"""Create a review package. Proposed machine labels never become human labels."""
from __future__ import annotations

import csv
from .common import ROOT, read_json, read_jsonl, write_json, now

FIELDS = ["id","kind","strategy","question_id","page","chunk_id","label","reason","annotator","review_status",
          "human_label","human_reason","reviewer","reviewed_at"]


def metadata_correct(hit, pages):
    page = pages.get(hit["page"])
    return bool(page and hit["document_id"] == page["document_id"] and hit["source"] == page["source"]
        and hit["metadata"] == page["metadata"] and page["text"][hit["start"]:hit["end"]] == hit["text"])


def fence(text):
    return "\n````text\n" + text + "\n````\n"


def build():
    pages = {p["page"]:p for p in read_jsonl("data/pages.jsonl")}
    traces = read_jsonl("results/traces_test.jsonl")
    configs = {s:read_jsonl(f"results/chunks_{'A' if s=='A' else 'B'}.jsonl") for s in ("A","B","C")}
    rows, review = [], ["# Gói kiểm tra của người học", "",
        "Bản chính đã được Codex đọc và điền nhãn theo nội dung thật. Đây là nhãn hỗ trợ của AI, chưa ghi thành nhãn thủ công của người học.",
        "Đọc nguồn/chunk, rồi điền `human_label`, `human_reason`, `reviewer`, `reviewed_at` trong `labels.csv`. Không cần đồng ý với đề xuất.",
        "Coherence/grounding dùng 0–2. Metadata/gold dùng 0=sai, 1=đúng. Khi sửa gold, ghi vào lý do và giữ nguyên benchmark đã chạy; không sửa âm thầm để thay điểm.",
        "Mẫu coherence và tập test đã chốt trong `benchmark/protocol.json` trước khi chạy. Nguồn đầy đủ ở `data/normalized/` và `data/raw/`."]
    overrides = read_json("results/audit/ai_review.json")["overrides"] if (ROOT/"results/audit/ai_review.json").exists() else {}
    content = read_json("results/audit/content_review.json") if (ROOT/"results/audit/content_review.json").exists() else {}
    for anchor_index, anchor in enumerate(read_json("benchmark/protocol.json")["audit_anchors"],1):
        page = pages[anchor["page"]]
        for s in ("A","B","C"):
            chunk = next(c for c in configs[s] if c["page"] == anchor["page"] and c["start"] <= anchor["offset"] < c["end"])
            starts = chunk["start"] == 0 or page["text"][max(0,chunk["start"]-2):chunk["start"]].endswith("\n\n")
            ends = chunk["end"] == len(page["text"]) or chunk["text"].endswith("\n\n")
            label = 2 if starts and ends else 1 if starts or ends else 0
            reason = f"Structural proxy only: begins at paragraph boundary={starts}, ends at paragraph boundary={ends}. Semantic completeness must be reviewed."
            rid = f"COH-{anchor_index:02d}-{s}"
            semantic_id = f"COH-{anchor_index:02d}-{'B' if s=='C' else s}"
            if semantic_id in content.get("coherence",{}):
                label,reason = content["coherence"][semantic_id]
                if s == "C":
                    reason += " C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk."
            rows.append(dict(id=rid,kind="coherence",strategy=s,page=anchor["page"],chunk_id=chunk["chunk_id"],proposed_label=label,proposal_reason=reason))
            review += [f"\n## {rid}: coherence", f"Nguồn: {page['source']} — {page['page']}, anchor {anchor['offset']}; chunk [{chunk['start']}, {chunk['end']}).",
                       "Ngữ cảnh quanh vị trí nguồn:",fence(page["text"][max(0,anchor["offset"]-200):anchor["offset"]+350]),
                       "Chunk cần chấm:",fence(chunk["text"]),f"Nhãn bản chính (Codex): {label}/2. {reason}"]
    for t in traces:
        q, s = t["question"],t["strategy"]
        for hit in t["hits"]:
            rid = f"META-{q['id']}-{s}-{hit['rank']}"
            valid = metadata_correct(hit,pages)
            reason = (f"document_id={hit['document_id']}, source={hit['source']}, page={hit['page']}, "
                      f"document_type={hit['metadata']['document_type']}, version={hit['metadata']['version']}; "
                      "đối chiếu URL/tiêu đề nguồn, page trong manifest và text/offsets đều khớp." if valid else "Có sai lệch giữa metadata và nguồn chuẩn; cần xem lại bản ghi.")
            if q["filter"] and any(hit["metadata"].get(k)!=v for k,v in q["filter"].items()):
                reason += " Kết quả ngoài scope người dùng, nhưng metadata phản ánh đúng nguồn; lỗi này tính riêng ở filter compliance."
            rows.append(dict(id=rid,kind="metadata",strategy=s,question_id=q["id"],page=hit["page"],chunk_id=hit["chunk_id"],proposed_label=int(valid),
                proposal_reason=reason))
        label = 2 if t["evidence_hit_at_3"] else 1 if any(h["page"] in {g["page"] for g in q["gold_alternatives"]} for h in t["hits"]) else 0
        rid = f"GRD-{q['id']}-{s}"
        reason = "Mechanical proposal: 2=full strict evidence found; 1=gold page retrieved without full quote; 0=no gold page. Equivalent evidence and missing context require semantic review."
        if rid in overrides:
            label,reason = overrides[rid]["label"],overrides[rid]["reason"]
        if f"{q['id']}-{s}" in content.get("grounding",{}):
            label,reason = content["grounding"][f"{q['id']}-{s}"]
        rows.append(dict(id=rid,kind="grounding",strategy=s,question_id=q["id"],proposed_label=label,proposal_reason=reason))
        review += [f"\n## {rid}: grounding và metadata top-3", f"Câu hỏi: {q['question']}", f"Đáp án dự kiến: {q['expected_answer']}",
                   f"Gold: {q['gold_source_id']} / {q['gold_page']}",fence(q["evidence_quote"]), f"Filter người dùng: {q['filter']}; filter thực tế: {t['applied_filter']}"]
        for h in t["hits"]:
            review += [f"### Top {h['rank']} / META-{q['id']}-{s}-{h['rank']}",
                f"Chunk {h['chunk_id']}; source {h['source']}; page {h['page']}; type {h['metadata']['document_type']}; version {h['metadata']['version']}; offsets [{h['start']},{h['end']}).",
                fence(h["text"])]
        review += [f"Nhãn grounding bản chính (Codex): {label}/2. {reason}"]
    for q in read_json("benchmark/questions.json"):
        rid = f"GOLD-{q['id']}"
        rows.append(dict(id=rid,kind="gold",question_id=q["id"],page=q["gold_page"],proposed_label=1,
            proposal_reason=content.get("gold",{}).get(q["id"],"Exact evidence exists in snapshot; semantic review pending.")))
        review += [f"\n## {rid}: gold",q["question"],f"Đáp án: {q['expected_answer']}",f"Nguồn: {q['gold_source_id']} / {q['gold_page']}",fence(q["evidence_quote"])]
    target = ROOT/"results/audit/labels.csv"
    target.parent.mkdir(parents=True,exist_ok=True)
    previous = {}
    if target.exists():
        with target.open(encoding="utf-8",newline="") as file:
            previous = {r["id"]:r for r in csv.DictReader(file)}
    for row in rows:
        row["label"] = row.pop("proposed_label")
        row["reason"] = row.pop("proposal_reason")
        row["annotator"] = "Codex (AI)"
        row["review_status"] = "assistant reviewed; student cross-check pending"
        for field in ("human_label","human_reason","reviewer","reviewed_at"):
            row[field] = previous.get(row["id"],{}).get(field,"")
        if row["human_label"] != "":
            allowed = {"0","1","2"} if row["kind"] in ("coherence","grounding") else {"0","1"}
            if row["human_label"] not in allowed:
                raise ValueError(f"Invalid human label for {row['id']}; expected {allowed}")
    with target.open("w",encoding="utf-8",newline="") as out:
        writer = csv.DictWriter(out,fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (target.parent/"REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    summary = {"generated_at":now(),"method":"Primary labels filled by Codex from source/trace content; no confirmed human audit", "assistant_labeled":len(rows), "groups":{}}
    for kind in ("coherence","metadata","grounding","gold"):
        subset = [r for r in rows if r["kind"]==kind]
        complete = [r for r in subset if r["human_label"] != "" and all(r[f] for f in ("human_reason","reviewer","reviewed_at"))]
        summary["groups"][kind] = {"required":len(subset),"human_confirmed":len(complete),"pending":len(subset)-len(complete)}
    write_json("results/audit/status.json",summary)
    ai_summary = {}
    for s in ("A","B","C"):
        ai_summary[s] = {}
        for kind in ("coherence","metadata","grounding"):
            subset = [r for r in rows if r["kind"]==kind and r["strategy"]==s]
            labels = [int(r["label"]) for r in subset]
            ai_summary[s][kind] = {"n":len(labels),"mean":sum(labels)/len(labels),
                "counts":{str(k):labels.count(k) for k in (0,1,2)}}
    write_json("results/audit/assistant_summary.json", {"annotator":"Codex (AI)","human_confirmed":False,"strategies":ai_summary})
    print(summary)
