from typing import Optional, List
from apps.agent_api.retrieval.index import build_index, RetrievalIndex
from apps.agent_api.retrieval.retrieve import retrieve
from apps.agent_api.schemas.evidence import CitedAnswer
from apps.agent_api.policies.citation_policy import pick_citations_from_evidence, enforce_citations

class ClinicalGuidelineAgent:
    def __init__(self, corpus_dir: str):
        self.corpus_dir = corpus_dir
        self._index: Optional[RetrievalIndex] = None

    def _ensure_index(self) -> RetrievalIndex:
        if self._index is None:
            self._index = build_index(self.corpus_dir)
        return self._index

    def answer(self, query: str, top_k: int = 5) -> CitedAnswer:
        index = self._ensure_index()
        evidence = retrieve(query, index=index, top_k=top_k)

        # v1 response: extract a brief grounded answer from evidence (no LLM yet)
        if not evidence:
            return CitedAnswer(
                answer="I don’t have enough guideline evidence in my local corpus to answer that.",
                citations=[],
                refusal=True,
                reason="No relevant guideline passages were retrieved.",
                evidence=[]
            )

        # very simple “grounded summary” from top evidence chunk
        top = evidence[0].text.strip()
        draft = (
            "Based on the retrieved guideline passages, here is the closest supported summary:\n\n"
            f"{top}"
        )

        resp = CitedAnswer(
            answer=draft,
            citations=pick_citations_from_evidence(evidence),
            refusal=False,
            reason=query,   # temporarily store query here for citation policy
            evidence=evidence
        )

        # enforce citations (turn into refusal if needed and missing)
        resp = enforce_citations(resp)

        # restore reason if not refusal
        if not resp.refusal:
            resp.reason = None

        return resp
