from io import BufferedReader, BytesIO

import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

with st.sidebar:
    # https://chuoling.github.io/mediapipe/solutions/pose.html#min_detection_confidence
    min_detection_confidence = st.number_input(
        label="Minimum detection confidence",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        key="min_detection_confidence",
    )
    # https://chuoling.github.io/mediapipe/solutions/pose.html#model_complexity
    model_complexity = st.selectbox(
        label="Model complexity",
        options=[
            0,
            1,
            2,
        ],
        index=1,
        key="model_complexity",
    )
    data_source = st.selectbox(
        label="Select a data source",
        options=[
            "file",
            "camera",
        ],
        key="data_source",
        index=0,
    )


st.title("Pose estimation")

if data_source == "camera":
    st.info("AI will detect objects in the camera image.")
    uploaded_file = st.camera_input("Take a picture")
if data_source == "file":
    st.info("Upload an image and AI will estimate the pose.")
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
    button = st.button("Estimate pose")

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
            mp_pose = mp.solutions.pose
            mp_drawing = mp.solutions.drawing_utils

            pose = mp_pose.Pose(
                static_image_mode=True,
                min_detection_confidence=min_detection_confidence,
                model_complexity=model_complexity,
            )

            bytes_data = uploaded_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            results = pose.process(img)
            output_img = img.copy()
            mp_drawing.draw_landmarks(
                output_img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=10),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=10),
            )
            ret, enco_img = cv2.imencode(".png", cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
            BytesIO_img = BytesIO(enco_img.tostring())
            BufferedReader_img = BufferedReader(BytesIO_img)

            # Output
            st.image(
                image=output_img,
                use_column_width=True,
                caption="Output image",
            )
            st.download_button(
                label="Download",
                data=BufferedReader_img,
                file_name="output.png",
                mime="image/png",
            )
