import base64
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


class InputSourceType(Enum):
    CAMERA = "camera"
    FILE = "file"


class Processor:
    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        raise NotImplementedError

    def get_states(self) -> dict:
        return {}


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
        # https://stackoverflow.com/a/77479465
        classes: list[int] = None,
        target: int = 0,  # 0: 'person'
    ):
        # model_name: https://docs.ultralytics.com/models/yolov8/#supported-tasks-and-modes
        self.model = YOLO(model_name)
        # label names, 0: 'person', 1: 'bicycle', 2: 'car'
        # print(self.model.names)
        self.confidence = confidence
        self.classes = classes
        self.num = 0
        self.target = target

    def process(
        self,
        frame: cv2.UMat,
    ) -> cv2.UMat:
        results = self.model(
            frame,
            conf=self.confidence,
            classes=self.classes,
        )
        previous_num = self.num
        self.num = len([x for x in results[0].boxes.cls if x == self.target])
        output_img = results[0].plot(
            labels=True,
            conf=True,
        )

        # play alert sound if the number of target objects increases
        if previous_num < self.num:
            self._handle_event()

        return cv2.cvtColor(
            src=output_img,
            code=cv2.COLOR_BGR2RGB,
        )

    def get_states(self):
        return {
            "num": self.num,
        }

    def _handle_event(self):
        st.toast("Alert", icon="❗")
        try:
            # https://discuss.streamlit.io/t/how-to-play-an-audio-file-automatically-generated-using-text-to-speech-in-streamlit/33201
            # https://www.youtube.com/watch?v=U5Z76XLEwRM
            with open("./datasets/alert.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio controls autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(
                    md,
                    unsafe_allow_html=True,
                )
        except Exception as _:
            # st.toast("Failed to play alert sound", icon="❌")
            pass


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
    tab_input, tab_mode = st.tabs(
        [
            "source",
            "processor",
        ]
    )
    with tab_input:
        input_source_type = st.radio(
            label="input source",
            options=[
                InputSourceType.FILE,
                InputSourceType.CAMERA,
            ],
            index=0,
            format_func=lambda x: x.value,
        )
        if input_source_type == InputSourceType.FILE:
            file = st.file_uploader(
                label="upload video file",
                type=[
                    "mp4",
                    "mov",
                    "avi",
                ],
            )
            if file:
                file_path = f"/tmp/{file.name}"
                with open(file_path, "wb") as f:
                    f.write(file.read())
                device = file_path
        if input_source_type == InputSourceType.CAMERA:
            # device: https://docs.opencv.org/4.10.0/d8/dfe/classcv_1_1VideoCapture.html#a5d5f5dacb77bbebdcbfb341e3d4355c1
            device = st.text_input(
                label="input your video/camera device",
                value="0",
            )
            if device.isnumeric():
                # e.g. "0" -> 0
                device = int(device)

    with tab_mode:
        processor_type = st.radio(
            label="processor type",
            options=[
                ProcessorType.YOLOV8,
                ProcessorType.BLUR,
                ProcessorType.CANNY,
                ProcessorType.INVERT,
            ],
            index=0,
            format_func=lambda x: x.value,
        )

st.title("Video processing")

st.text(f"source: {input_source_type.value}")
st.text(f"processor: {processor_type.value}")

start_button = st.button("Start")
stop_button = st.button("Stop")

image_loc = st.empty()
states_loc = st.empty()
processor = get_processor(processor_type)

if start_button:
    capture = cv2.VideoCapture(device)

    while capture.isOpened:
        ret, frame = capture.read()

        if not ret:
            st.toast("End of video", icon="❗")
            break

        processed_frame = processor.process(
            frame=frame,
        )

        states = processor.get_states()
        states_loc.write(states)

        image_loc.image(
            image=processed_frame,
            use_column_width=True,
        )

        if stop_button:
            break

    capture.release()
