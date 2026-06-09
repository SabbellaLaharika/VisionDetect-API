# YOLOv8 Object Detection API & Web App

This project provides a complete, containerized solution for real-time object detection using the state-of-the-art YOLOv8 model. It features a FastAPI REST backend for high-performance inference and a Streamlit frontend for an intuitive user experience.

## Features

- **Real-Time Inference**: Powered by YOLOv8 for fast and accurate object detection.
- **RESTful API**: A robust FastAPI service with health checks and a dedicated `/detect` endpoint.
- **Interactive UI**: A Streamlit web app to easily upload images, adjust confidence thresholds, and view annotated results alongside detailed JSON summaries.
- **Fully Containerized**: Uses Docker and Docker Compose for seamless, portable, and scalable deployment.

## Project Structure

- `api/`: FastAPI application code, Dockerfile, and requirements.
- `ui/`: Streamlit application code, Dockerfile, and requirements.
- `models/`: Directory where the pre-trained YOLOv8 model is stored.
- `scripts/`: Helper scripts, including the model download script.
- `output/`: Directory for saving annotated images after successful detection.

## Setup Instructions

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Environment Variables

Create a `.env` file based on the provided template:

```bash
cp .env.example .env
```

You can customize the port numbers and other settings in the `.env` file if necessary.

### 2. Download the YOLOv8 Model

To keep the repository lightweight, the model is not included. Download it using the provided script (this requires `wget` or `curl`):

```bash
bash scripts/download_model.sh
```

This will download `yolov8n.pt` into the `models/` directory.

### 3. Build and Run Containers

Use Docker Compose to build and start both the API and UI services:

```bash
docker-compose up --build -d
```

- The API service will be available at `http://localhost:8000` (or your configured `API_PORT`).
- The Streamlit UI will be available at `http://localhost:8501` (or your configured `UI_PORT`).

## Usage

### Using the Web UI

1. Open your browser and navigate to `http://localhost:8501`.
2. Upload an image (JPG, JPEG, or PNG).
3. Adjust the confidence threshold if needed.
4. Click "Detect Objects". The annotated image and a summary of detected objects will be displayed.

### Using the API directly

You can also interact directly with the FastAPI service.

**Check API Health:**
```bash
curl http://localhost:8000/health
```

**Perform Object Detection:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/your/image.jpg" \
  -F "confidence_threshold=0.25"
```

The API will return a JSON response containing bounding boxes, labels, scores, and a summary count of detected objects. It will also save the annotated image to `output/last_annotated.jpg` (mapped to the host's `output/` directory).

## Stopping the Application

To stop the running containers:

```bash
docker-compose down
```
