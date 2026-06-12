# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

# Stage 2: Final
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

ENV UI_PORT=8501
EXPOSE $UI_PORT

CMD ["sh", "-c", "streamlit run app.py --server.port ${UI_PORT} --server.address 0.0.0.0"]
