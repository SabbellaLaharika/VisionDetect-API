FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV UI_PORT=8501
EXPOSE $UI_PORT

CMD ["sh", "-c", "streamlit run app.py --server.port ${UI_PORT} --server.address 0.0.0.0"]
