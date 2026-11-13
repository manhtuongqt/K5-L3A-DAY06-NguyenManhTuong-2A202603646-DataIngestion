"""A pinned, real quantized BGE ONNX model. No API key or fallback vectors."""
from __future__ import annotations

import time
import importlib.metadata
import platform
import requests
import numpy as np
from fastembed import TextEmbedding

from .common import ROOT, now, read_json, sha256, write_json

MODEL = "BAAI/bge-small-en-v1.5"
HF_REPO = "qdrant/bge-small-en-v1.5-onnx-q"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
FILES = ["config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "model_optimized.onnx"]


def prepare():
    directory = ROOT / ".local/model"
    directory.mkdir(parents=True, exist_ok=True)
    lock_path = ROOT / "benchmark/model.json"
    if lock_path.exists():
        lock = read_json("benchmark/model.json")
        revision = lock["revision"]
    else:
        response = requests.get(f"https://huggingface.co/api/models/{HF_REPO}", timeout=60)
        response.raise_for_status()
        revision = response.json()["sha"]
        lock = None
    file_hashes = {}
    for name in FILES:
        path = directory / name
        if not path.exists():
            print(f"Downloading pinned model file: {name}", flush=True)
            response = requests.get(f"https://huggingface.co/{HF_REPO}/resolve/{revision}/{name}", stream=True, timeout=(30, 180))
            response.raise_for_status()
            temp = path.with_suffix(path.suffix + ".part")
            with temp.open("wb") as out:
                for block in response.iter_content(1024 * 1024):
                    out.write(block)
            temp.replace(path)
        file_hashes[name] = sha256(path)
    if lock and file_hashes != lock["files_sha256"]:
        raise ValueError("Model file hash mismatch; refusing a silent model change")
    if not lock:
        write_json("benchmark/model.json", {"model": MODEL, "provider": "local ONNX Runtime CPU / FastEmbed",
            "onnx_repository": HF_REPO, "revision": revision, "dimensions": 384, "quantization": "Qdrant ONNX quantized",
            "query_prefix": QUERY_PREFIX, "document_prefix": "", "pooling": "CLS with L2 normalization (FastEmbed BGE)",
            "max_tokens": 512, "threads": 4, "files_sha256": file_hashes,
            "model_card": "https://huggingface.co/BAAI/bge-small-en-v1.5", "license": "MIT", "prepared_at": now()})
    return directory


class Embedder:
    def __init__(self):
        started = time.perf_counter()
        directory = prepare()
        self.model = TextEmbedding(MODEL, specific_model_path=str(directory), threads=4, providers=["CPUExecutionProvider"])
        self.load_seconds = time.perf_counter() - started

    def documents(self, texts):
        vectors = np.asarray(list(self.model.passage_embed(texts, batch_size=32)), dtype=np.float32)
        self._validate(vectors)
        return vectors

    def queries(self, texts):
        vectors = np.asarray(list(self.model.query_embed([QUERY_PREFIX + t for t in texts], batch_size=16)), dtype=np.float32)
        self._validate(vectors)
        return vectors

    @staticmethod
    def _validate(vectors):
        if vectors.ndim != 2 or vectors.shape[1] != 384 or not np.isfinite(vectors).all():
            raise ValueError("Invalid real embedding output")
        if not np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-4):
            raise ValueError("Unexpected unnormalized embedding")

    def token_count(self, texts):
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_file(str(ROOT / ".local/model/tokenizer.json"))
        tokenizer.no_truncation()
        return [len(tokenizer.encode(t).ids) for t in texts]


def runtime():
    names = ["beautifulsoup4", "requests", "fastembed", "qdrant-client", "onnxruntime", "numpy", "tokenizers"]
    return {"python": platform.python_version(), "platform": platform.platform(),
            "packages": {name: importlib.metadata.version(name) for name in names},
            "model": read_json("benchmark/model.json"), "vector_store": "QdrantClient local persistent",
            "path": ".local/qdrant", "distance": "cosine", "search": "exact", "api_calls": 0,
            "api_cost_usd": 0, "cost_limit": "No paid API calls; electricity, hardware and bandwidth not priced.", "recorded_at": now()}


if __name__ == "__main__":
    prepare()
    print("Pinned model snapshot ready", flush=True)
