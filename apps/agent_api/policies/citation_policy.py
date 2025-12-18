import re
from typing import List
from apps.agent_api.schemas.evidence import CitedAnswer, Citation

CLINICAL_ACTION_VERBS = re.compile(
    r"\b(screen|screening|treat|treatment|diagnos|prescrib|dose|medication|start|stop|recommend)\b",
    re.IGNORECASE
)

def needs_citations(user_query: str, draft_answer: str) -> bool:
    # v1 rule: if answer contains clinical action verbs or is long, require citations
    if CLINICAL_ACTION_VERBS.search(user_query) or CLINICAL_ACTION_VERBS.search(draft_answer):
        return True
    if len(draft_answer.split()) >= 30:
        return True
    return False

def enforce_citations(resp: CitedAnswer) -> CitedAnswer:
    """
    If citations are required and missing, convert to a refusal (safe behavior).
    """
    if resp.refusal:
        return resp

    require = needs_citations(user_query=resp.reason or "", draft_answer=resp.answer)
    # NOTE: we stash user_query into resp.reason temporarily in agent (see below)
    if require and len(resp.citations) == 0:
        resp.refusal = True
        resp.reason = "I can't support this answer from the available guideline sources (no citations found)."
        resp.answer = "I don’t have enough guideline evidence in my local corpus to answer that safely."
    return resp

def pick_citations_from_evidence(evidence, max_cites: int = 2) -> List[Citation]:
    cites = []
    for e in evidence[:max_cites]:
        cites.append(Citation(source_id=e.source_id, chunk_id=e.chunk_id))
    return cites
