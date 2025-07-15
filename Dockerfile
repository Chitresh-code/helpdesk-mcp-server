# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# ----------------- Builder stage -----------------
FROM base AS builder

# Install uv (prebuilt binary)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better cache performance
COPY --link pyproject.toml requirements.txt ./

# Set PATH for venv
ENV PATH="/app/.venv/bin:$PATH"

# Create venv & install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    uv pip install -r requirements.txt

# Copy the server code
COPY --link server ./server

# ----------------- Final stage -----------------
FROM base AS final

WORKDIR /app

# Create non-root user
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

# Copy virtual environment and code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/server ./server

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Use non-root user
USER appuser

# Expose port used by uvicorn
EXPOSE 8000

# Run the main MCP server (runs server/main.py)
CMD ["python", "-m", "server.main", "--port", "8000"]