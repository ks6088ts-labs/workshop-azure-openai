from enum import Enum

import cv2
import streamlit as st
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()


# define enum for processors
class ProcessorType(Enum):
    BLUR = "blur"
    CANNY = "canny"
    INVERT = "invert"
    YOLOV8 = "yolov8"


class Processor:
    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        raise NotImplementedError


class BlurProcessor(Processor):
    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        output_img = cv2.GaussianBlur(
            src=frame,
            ksize=(21, 21),
            sigmaX=0,
        )
        return cv2.cvtColor(
            src=output_img,
            code=cv2.COLOR_BGR2RGB,
        )


class CannyProcessor(Processor):
    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        gray = cv2.cvtColor(
            src=frame,
            code=cv2.COLOR_BGR2GRAY,
        )
        output_img = cv2.Canny(
            image=gray,
            threshold1=100,
            threshold2=200,
        )
        return cv2.cvtColor(
            src=output_img,
            code=cv2.COLOR_GRAY2RGB,
        )


class InvertProcessor(Processor):
    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        output_img = cv2.bitwise_not(
            src=frame,
        )
        return cv2.cvtColor(
            src=output_img,
            code=cv2.COLOR_BGR2RGB,
        )


class Yolov8Processor(Processor):
    def __init__(
        self,
        model_name: str = "yolov8n.pt",
        confidence: float = 0.5,
    ):
        # model_name: https://docs.ultralytics.com/models/yolov8/#supported-tasks-and-modes
        self.model = YOLO(model_name)
        self.confidence = confidence

    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        results = self.model(
            frame,
            conf=self.confidence,
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


def get_processor(processor_type: ProcessorType) -> Processor:
    if processor_type == ProcessorType.BLUR:
        return BlurProcessor()
    elif processor_type == ProcessorType.CANNY:
        return CannyProcessor()
    elif processor_type == ProcessorType.INVERT:
        return InvertProcessor()
    elif processor_type == ProcessorType.YOLOV8:
        return Yolov8Processor()
    else:
        raise ValueError(f"Unknown processor type: {processor_type}")


with st.sidebar:
    # device: https://docs.opencv.org/4.10.0/d8/dfe/classcv_1_1VideoCapture.html#a5d5f5dacb77bbebdcbfb341e3d4355c1
    device = st.text_input(
        label="input your video/camera device",
        value="0",
    )
    if device.isnumeric():
        # e.g. "0" -> 0
        device = int(device)
    processor_type = st.radio(
        label="processor type",
        options=[
            ProcessorType.BLUR,
            ProcessorType.CANNY,
            ProcessorType.INVERT,
            ProcessorType.YOLOV8,
        ],
        index=0,
        format_func=lambda x: x.value,
    )

st.title("Video processing")

start_button = st.button("Start")
stop = st.button("Stop")

image_loc = st.empty()
processor = get_processor(processor_type)

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
