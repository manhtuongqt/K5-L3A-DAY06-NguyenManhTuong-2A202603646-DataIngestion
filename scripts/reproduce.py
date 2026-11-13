"""Rebuild once in an isolated directory; preserve the submitted experiment."""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    work = (ROOT/".local/reproduce"/name).resolve()
    if not work.is_relative_to((ROOT/".local/reproduce").resolve()):
        raise ValueError("Replay workspace must stay inside this repository")
    work.mkdir(parents=True)
    for directory in ("src","tests","data","benchmark"):
        shutil.copytree(ROOT/directory,work/directory,ignore=shutil.ignore_patterns("__pycache__"))
    (work/"artifacts").mkdir()
    (work/"results/audit").mkdir(parents=True)
    (work/"report/individual").mkdir(parents=True)
    shutil.copy2(ROOT/"results/ingestion_log.json",work/"results/ingestion_log.json")
    shutil.copy2(ROOT/"results/audit/ai_review.json",work/"results/audit/ai_review.json")
    shutil.copy2(ROOT/"results/audit/content_review.json",work/"results/audit/content_review.json")
    if (ROOT/".local/model").exists():
        shutil.copytree(ROOT/".local/model",work/".local/model")
    commands = [[sys.executable,"-m","src.pipeline",stage] for stage in ("index","check-store","dev","test","audit","verify")]
    commands.append([sys.executable,"-m","unittest","discover","-s","tests","-v"])
    with (work/"results/console.log").open("w",encoding="utf-8") as log:
        for command in commands:
            print("Replay:"," ".join(command[1:]),flush=True)
            result = subprocess.run(command,cwd=work,capture_output=True,text=True,encoding="utf-8",errors="replace",env={**os.environ,"PYTHONIOENCODING":"utf-8"})
            log.write("\n$ "+" ".join(command[1:])+"\n"+result.stdout+result.stderr)
            log.flush()
            if result.returncode:
                print(result.stdout+result.stderr)
                raise RuntimeError(f"Reproduction stage failed; see {work/'results/console.log'}")
    checks = []
    max_score_difference = 0.0
    for split in ("dev","test"):
        original = json.loads((ROOT/f"results/metrics_{split}.json").read_text(encoding="utf-8"))
        replay = json.loads((work/f"results/metrics_{split}.json").read_text(encoding="utf-8"))
        for strategy in ("A","B","C"):
            for field in ("hit_at_1","evidence_hit_at_3","filter_compliance"):
                checks.append(original["strategies"][strategy][field]==replay["strategies"][strategy][field])
        read = lambda path: [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        for first,second in zip(read(ROOT/f"results/traces_{split}.jsonl"),read(work/f"results/traces_{split}.jsonl")):
            checks.append([h["chunk_id"] for h in first["hits"]]==[h["chunk_id"] for h in second["hits"]])
            max_score_difference=max(max_score_difference,max(abs(a["score"]-b["score"]) for a,b in zip(first["hits"],second["hits"])))
    selected_original=json.loads((ROOT/"results/selection.json").read_text())["selected_strategy"]
    selected_replay=json.loads((work/"results/selection.json").read_text())["selected_strategy"]
    report={"completed_at":datetime.now(timezone.utc).isoformat(),"workspace":str(work.relative_to(ROOT)).replace("\\","/"),
        "passed":all(checks),"comparison_checks":len(checks),"max_score_absolute_difference":max_score_difference,
        "original_selected_strategy":selected_original,"replay_selected_strategy":selected_replay,
        "selection_note":"Latency tie-break can vary; original submission keeps its preregistered dev selection.",
        "scope":"Full fresh index, persisted-store checks, one dev/test retrieval per strategy, audit generation, frozen input verification and unit/integration tests; no strategy tuning.",
        "api_inference_calls":0,"api_cost_usd":0}
    (ROOT/"results/reproduction.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    shutil.copy2(work/"results/console.log",ROOT/"results/reproduction_console.txt")
    print(json.dumps(report,indent=2))
    if not report["passed"]:
        raise RuntimeError("Replay differs; inspect without overwriting the original experiment")


if __name__=="__main__":
    main()
