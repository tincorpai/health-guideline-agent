from typing import List
import numpy as np

from apps.agent_api.retrieval.index import RetrievalIndex
from apps.agent_api.schemas.evidence import EvidenceChunk

def retrieve(query: str, index: RetrievalIndex, top_k: int = 5) -> List[EvidenceChunk]:
    if not query.strip() or not index.chunks:
        return []

    q_vec = index.vectorizer.transform([query])
    scores = (index.matrix @ q_vec.T).toarray().ravel()
    if scores.size == 0:
        return []

    top_idx = np.argsort(-scores)[:top_k]
    results: List[EvidenceChunk] = []
    for i in top_idx:
        if scores[i] <= 0:
            continue
        c = index.chunks[int(i)]
        results.append(
            EvidenceChunk(
                source_id=f"v1/{c.source_id}",
                chunk_id=c.chunk_id,
                text=c.text,
                score=float(scores[i]),
            )
        )
    return results
