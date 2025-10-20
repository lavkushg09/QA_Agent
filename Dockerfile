FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps (add as needed)
RUN apt-get update && apt-get install -y vim && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv and create project venv
RUN pip install --no-cache-dir uv

# Prepare env and install deps with uv (leverages Docker layer cache)
COPY requirements.txt ./
RUN uv venv && \
    uv pip install -r requirements.txt

# Ensure the venv is on PATH
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the application
COPY . .

# Create runtime dirs
RUN mkdir -p uploaded_pdfs data/chroma logs

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


