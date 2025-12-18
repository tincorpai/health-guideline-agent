FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install fastapi uvicorn

COPY apps apps

CMD ["uvicorn", "apps.agent_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
