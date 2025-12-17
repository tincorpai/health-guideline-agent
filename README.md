# health-guideline-agent
Agentic clinical guideline assistant with AWS-based CI/CD, regression evals, and safety guardrails (non-PHI)



A **production-oriented, agentic clinical guideline assistant** designed for the health sector.  
This system retrieves and synthesizes **evidence-based clinical guidelines** and produces **citation-grounded, non-diagnostic responses**, with **end-to-end CI/CD on AWS** and agent-specific quality controls.

> **Important:** This project is **non-PHI** and intended for **informational and research use only**.  
> It does **not** provide medical advice, diagnosis, or treatment recommendations.

---

## 🚑 Motivation

Clinical guidelines are extensive, frequently updated, and difficult to navigate under time constraints.  
This project demonstrates how **agentic AI systems** can be safely deployed in healthcare contexts by combining:

- Retrieval-grounded generation (no hallucinations)
- Explicit safety and escalation policies
- Agent regression testing in CI
- Cloud-native deployment (AWS ECS)

The goal is to show **how to build health-aware agentic systems responsibly**, not just how to build a chatbot.

---

## 🧠 What This Agent Does

- Retrieves relevant passages from approved clinical guideline sources
- Synthesizes concise, structured summaries
- Requires **explicit citations** for every clinical claim
- Refuses or escalates out-of-scope or diagnostic requests
- Logs and audits agent decisions for traceability

---

## 🏗️ Architecture Overview

```text
Client → FastAPI → Policies → Agent → Tools → Retrieval
                         ↓
                     Audit Logs
