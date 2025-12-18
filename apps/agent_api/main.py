from fastapi import FastAPI

app = FastAPI(title = "Clinical Guideline Assistant")


@app.get("/health")
def health():
  return {"status": "ok"}


