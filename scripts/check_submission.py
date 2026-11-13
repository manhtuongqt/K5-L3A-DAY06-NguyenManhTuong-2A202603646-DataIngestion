"""Submission checks with separate technical and human-review completion."""
from __future__ import annotations
import csv
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.common import now,read_json,write_json
from src.pipeline import verify


def main():
    verify()
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"))
    test_result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (ROOT/"results/tests.txt").write_text(stream.getvalue(),encoding="utf-8")
    assert test_result.wasSuccessful(),stream.getvalue()
    required=["STUDENT.md","README.md","requirements.txt","requirements-lock.txt","THIRD_PARTY_NOTICES.md",
        "src/pipeline.py","data/manifest.json","benchmark/questions.json","benchmark/protocol.json","benchmark/lock.json",
        "artifacts/experiment_log.csv","results/traces_dev.jsonl","results/traces_test.jsonl","results/metrics.json",
        "results/store_checks.json","results/runtime.json","results/audit/labels.csv","results/audit/REVIEW.md",
        "report/individual/2A202603646_NguyenManhTuong.md","docs/GATE_CHECKLIST.md"]
    missing=[p for p in required if not (ROOT/p).exists()]
    assert not missing,f"Missing artifacts: {missing}"
    documents=["README.md","THIRD_PARTY_NOTICES.md","results/audit/README.md","report/individual/2A202603646_NguyenManhTuong.md"]
    broken=[]
    for filename in documents:
        text=(ROOT/filename).read_text(encoding="utf-8")
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            target=target.split('#')[0].strip('<>')
            if not target or re.match(r'^[a-z]+:',target):
                continue
            if not ((ROOT/filename).parent/unquote(target)).exists():
                broken.append((filename,target))
    assert not broken,f"Broken file links: {broken}"
    # Check files that would be committed; never print any matched credential content.
    paths=subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard"],cwd=ROOT,text=True).splitlines()
    patterns=[re.compile(r'sk-(?:proj-)?[A-Za-z0-9_-]{24,}'),re.compile(r'AIza[0-9A-Za-z_-]{30,}'),
              re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(r'tvly-[A-Za-z0-9_-]{20,}')]
    findings=[]
    for relative in paths:
        p=ROOT/relative
        assert '.venv/' not in relative and '.local/' not in relative and p.name!='.env',f"Private/local file would be committed: {relative}"
        if p.is_file():
            text=p.read_text(encoding="utf-8",errors="ignore")
            if any(pattern.search(text) for pattern in patterns):
                findings.append(relative)
    assert not findings,f"Potential credential patterns in: {findings}"
    with (ROOT/"artifacts/experiment_log.csv").open(encoding="utf-8",newline="") as f:
        experiments=list(csv.DictReader(f))
    assert [r['strategy'] for r in experiments]==['A','B','C']
    assert all(r['test_hit3'] and r['dev_hit3'] for r in experiments)
    with (ROOT/"results/audit/labels.csv").open(encoding="utf-8",newline="") as f:
        labels=list(csv.DictReader(f))
    assert len(labels)==110 and len({r['id'] for r in labels})==110
    for row in labels:
        allowed={'0','1','2'} if row['kind'] in ('coherence','grounding') else {'0','1'}
        assert row['label'] in allowed and row['reason'] and row['annotator'],f"Missing primary audit data: {row['id']}"
    audit=read_json("results/audit/status.json")
    pending=sum(g['pending'] for g in audit['groups'].values())
    gold_valid=all(r['human_label']=='1' for r in labels if r['kind']=='gold')
    result={"checked_at":now(),"technical_checks_passed":True,"full_submission_ready":pending==0 and gold_valid,
        "unit_integration_tests":{"run":test_result.testsRun,"failures":len(test_result.failures),"errors":len(test_result.errors)},
        "frozen_input_and_trace_verification":True,"artifact_structure":True,"local_file_links":True,
        "secret_pattern_scan":"No patterns found; heuristic check, not a proof of all possible secrets",
        "human_audit_pending":pending,"human_gold_semantics_all_confirmed_valid":gold_valid,
        "lms":"Student submits; not submitted by agent"}
    write_json("results/submission_check.json",result)
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
