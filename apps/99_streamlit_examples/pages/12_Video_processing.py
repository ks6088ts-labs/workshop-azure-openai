import cv2
import streamlit as st
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()


class Processor:
    def __init__(self, model_name):
        self.model = YOLO(model_name)

    def process(self, frame):
        results = self.model(
            frame,
            conf=0.5,
            classes=[0],
        )
        output_img = results[0].plot(
            labels=True,
            conf=True,
        )
        return cv2.cvtColor(
            src=output_img,
            code=cv2.COLOR_BGR2RGB,
        )


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
    device = st.text_input(
        label="input your video/camera device",
        value="0",
    )
    if device.isnumeric():
        # e.g. "0" -> 0
        device = int(device)

st.title("Video processing")

start_button = st.button("Start")
stop = st.button("Stop")

image_loc = st.empty()
processor = Processor(
    model_name=model_name,
)

if start_button:
    capture = cv2.VideoCapture(device)

    while capture.isOpened:
        ret, frame = capture.read()

        if not ret:
            st.error("Failed to capture image")
            continue

        processed_frame = processor.process(
            frame=frame,
        )

        image_loc.image(
            image=processed_frame,
            use_column_width=True,
        )

        if stop:
            break

    capture.release()
