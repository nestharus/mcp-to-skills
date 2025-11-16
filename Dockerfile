FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl=8.14.1-2+deb13u2 ca-certificates=20250419 \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

RUN useradd -m -u 10000 appuser \
    && chown -R appuser:appuser /app

COPY --chown=appuser:appuser pyproject.toml uv.lock ./

USER appuser
RUN uv sync --frozen --no-cache

# app code
COPY --chown=appuser:appuser . .
RUN uv pip install --no-cache -e .

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "scripts/start-server.py", "--host", "0.0.0.0", "--port", "8000"]
