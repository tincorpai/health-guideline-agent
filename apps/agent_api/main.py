from fastapi import FastAPI
from pydantic import BaseModel
import os

from apps.agent_api.agents.clinical_agent import ClinicalGuidelineAgent
from apps.agent_api.schemas.evidence import CitedAnswer

app = FastAPI(title="Health Guideline Agent (Non-PHI)")

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "retrieval", "corpus", "v1")
agent = ClinicalGuidelineAgent(corpus_dir=CORPUS_DIR)

class AskRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=CitedAnswer)
def ask(req: AskRequest):
    return agent.answer(req.query, top_k=req.top_k)

