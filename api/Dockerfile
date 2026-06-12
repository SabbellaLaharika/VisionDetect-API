# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Create a virtual environment
RUN uv venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
# Install dependencies into the virtual environment
RUN uv pip install --no-cache -r requirements.txt

# Stage 2: Final
FROM python:3.9-slim

WORKDIR /app

# Install only runtime system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

ENV API_PORT=8000
EXPOSE $API_PORT

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${API_PORT}"]
