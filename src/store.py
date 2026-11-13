"""Use Qdrant's own persistent vector store, not a custom similarity engine."""
from __future__ import annotations

import uuid
from qdrant_client import QdrantClient, models

from .common import ROOT


class Store:
    def __init__(self, path=None):
        self.client = QdrantClient(path=str(path or ROOT / ".local/qdrant"))

    def close(self):
        self.client.close()

    def replace(self, collection, chunks, vectors):
        if len(chunks) != len(vectors):
            raise ValueError("Chunk/vector count mismatch")
        # Reconcile a complete snapshot through the official API. Recreating a local
        # collection can leave open SQLite files on Windows, so do not delete folders.
        if not self.client.collection_exists(collection):
            self.client.create_collection(collection, vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE))
        params = self.client.get_collection(collection).config.params.vectors
        if params.size != 384 or params.distance != models.Distance.COSINE:
            raise ValueError("Collection does not match the frozen embedding/metric")
        previous, offset = set(), None
        while True:
            points, offset = self.client.scroll(collection, limit=256, offset=offset, with_payload=False, with_vectors=False)
            previous.update(str(point.id) for point in points)
            if offset is None:
                break
        current = {str(uuid.UUID(c["chunk_id"])) for c in chunks}
        for start in range(0, len(chunks), 128):
            batch = [models.PointStruct(id=str(uuid.UUID(c["chunk_id"])), vector=v.tolist(),
                payload={**c, **c["metadata"]}) for c, v in zip(chunks[start:start+128], vectors[start:start+128])]
            self.client.upsert(collection_name=collection, points=batch, wait=True)
        obsolete = sorted(previous-current)
        if obsolete:
            self.client.delete(collection_name=collection, points_selector=models.PointIdsList(points=obsolete), wait=True)
        return self.client.count(collection, exact=True).count

    def search(self, collection, vector, filters=None, top_k=3):
        if filters and set(filters) - {"document_type", "language", "version"}:
            raise ValueError("Unsupported filter field; gold document/page IDs are forbidden")
        query_filter = models.Filter(must=[models.FieldCondition(key=k, match=models.MatchValue(value=v))
                                for k, v in (filters or {}).items()]) if filters else None
        points = self.client.query_points(collection_name=collection, query=vector.tolist(),
            query_filter=query_filter, limit=top_k, search_params=models.SearchParams(exact=True), with_payload=True).points
        return [{"rank": i+1, "score": p.score, **p.payload} for i, p in enumerate(points)]
