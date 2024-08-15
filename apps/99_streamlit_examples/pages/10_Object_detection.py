import cv2
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()

with st.sidebar:
    model_name = st.selectbox(
        label="Select a model",
        options=[
            "yolov8n.pt",
            "yolov9c.pt",
            "yolov10n.pt",
            # https://docs.ultralytics.com/models/yolov8/#supported-tasks-and-modes
        ],
        key="model_name",
        index=0,
    )


st.title("Object detection")

st.info("Upload an image and AI will detect objects in the image.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=(
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
    ),
)
if uploaded_file is not None:
    button = st.button("Detect objects")

row1_left, row1_right = st.columns(2)
with row1_left:
    if uploaded_file:
        st.image(
            uploaded_file,
            use_column_width=True,
            caption="Input image",
        )

with row1_right:
    if uploaded_file and button:
        with st.spinner("Thinking..."):
            model = YOLO(model_name)
            bytes_data = uploaded_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            results = model(cv2_img, conf=0.5, classes=[0])
            output_img = results[0].plot(labels=True, conf=True)
            output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
            categories = results[0].boxes.cls
            person_num = len(categories)

            # Output
            st.image(
                output_img,
                use_column_width=True,
                caption="Output image",
            )
            st.text(f"Number of people: {person_num}")
