import streamlit as st
import requests
from PIL import Image
import os
import io
import json

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")
st.title("YOLOv8 Object Detection")
st.write("Upload an image to detect objects using YOLOv8.")

# Get API URL from environment variable
API_URL = os.getenv("API_URL", "http://api:8000/detect")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button("Detect Objects", type="primary"):
            with st.spinner("Detecting..."):
                try:
                    # Send image to FastAPI backend
                    files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"confidence_threshold": confidence}
                    
                    response = requests.post(API_URL, files=files, data=data)
                    
                    if response.status_code == 200:
                        st.session_state['detection_result'] = response.json()
                        st.session_state['detection_success'] = True
                    else:
                        st.error(f"Error from API: {response.text}")
                        st.session_state['detection_success'] = False
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to API. Error: {e}")
                    st.session_state['detection_success'] = False

with col2:
    st.subheader("Output")
    if 'detection_success' in st.session_state and st.session_state['detection_success']:
        # The API saves the annotated image to /app/output/last_annotated.jpg
        # Since docker-compose shares the volume, we can read it directly from the shared volume path
        # But a more robust way is to either return the image from API or just read from the volume
        # We will read from the volume mapping: /app/output (in UI container) -> /app/output (in API container)
        
        output_image_path = "/app/output/last_annotated.jpg"
        
        if os.path.exists(output_image_path):
            annotated_image = Image.open(output_image_path)
            st.image(annotated_image, caption="Annotated Image", use_column_width=True)
            st.success("Detection complete!")
            
            # Display JSON summary
            result_json = st.session_state['detection_result']
            st.subheader("Detection Summary")
            
            st.write("Counts by Class:")
            st.json(result_json.get("summary", {}))
            
            with st.expander("Detailed Bounding Boxes"):
                st.json(result_json.get("detections", []))
        else:
            st.warning("Annotated image not found in the output directory. Check volume mappings.")
