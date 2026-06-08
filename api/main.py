from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from ultralytics import YOLO
import io
import os
import collections

app = FastAPI(title="YOLOv8 Object Detection API")

# Load the YOLOv8 model on startup
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/yolov8n.pt")
# We use Ultralytics YOLO class to load the model
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Failed to load model from {MODEL_PATH}: {e}")
    model = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/detect")
async def detect_objects(
    image: UploadFile = File(...),
    confidence_threshold: float = Form(0.25)
):
    if model is None:
        return JSONResponse(status_code=500, content={"error": "Model not loaded"})

    # Validate image
    if not image.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "File uploaded is not an image"})

    try:
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Perform inference
        results = model.predict(source=img, conf=confidence_threshold)
        
        # Process results
        detections = []
        summary = collections.defaultdict(int)
        
        # results is a list of Results objects
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # box.xyxy is a tensor of shape [1, 4]
                b = box.xyxy[0].tolist()
                score = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = result.names[cls_id]
                
                detections.append({
                    "box": b,
                    "label": label,
                    "score": score
                })
                summary[label] += 1
                
        # Save annotated image
        output_dir = "/app/output"
        os.makedirs(output_dir, exist_ok=True)
        annotated_img_path = os.path.join(output_dir, "last_annotated.jpg")
        
        # We can use ultralytics plot method to get annotated image array
        annotated_array = results[0].plot()
        annotated_img = Image.fromarray(annotated_array[..., ::-1]) # Convert BGR to RGB
        annotated_img.save(annotated_img_path)
        
        return {
            "detections": detections,
            "summary": dict(summary)
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
