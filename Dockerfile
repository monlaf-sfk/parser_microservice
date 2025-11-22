
FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


COPY pyproject.toml uv.lock ./


RUN uv pip install --system -r pyproject.toml


COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]