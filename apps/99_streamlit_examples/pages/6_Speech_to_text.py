import base64
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

with st.sidebar:
    azure_openai_endpoint = st.text_input(
        label="AZURE_OPENAI_ENDPOINT",
        value=getenv("AZURE_OPENAI_ENDPOINT"),
        key="AZURE_OPENAI_ENDPOINT",
        type="default",
    )
    azure_openai_api_key = st.text_input(
        label="AZURE_OPENAI_API_KEY",
        key="AZURE_OPENAI_API_KEY",
        type="password",
    )
    azure_openai_api_version = st.text_input(
        label="AZURE_OPENAI_API_VERSION",
        value=getenv("AZURE_OPENAI_API_VERSION"),
        key="AZURE_OPENAI_API_VERSION",
        type="default",
    )
    azure_openai_stt_model = st.text_input(
        label="AZURE_OPENAI_STT_MODEL",
        value=getenv("AZURE_OPENAI_STT_MODEL"),
        key="AZURE_OPENAI_STT_MODEL",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/6_Speech_to_text.py)"

st.title("Speech to text")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_stt_model:
    st.warning("Please fill in the required fields at the sidebar.")
    st.stop()

st.info("This is a sample to convert speech to text.")

uploaded_file = st.file_uploader(
    "Upload an article",
    type=(
        "m4a",
        "mp3",
        "webm",
        "mp4",
        "mpga",
        "wav",
    ),
)

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")

    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    if st.button("Convert"):
        with st.spinner("Converting..."):
            response = client.audio.transcriptions.create(
                model=azure_openai_stt_model,
                file=uploaded_file,
                response_format="text",
            )
        st.write(response)
        transcript_encoded = base64.b64encode(response.encode()).decode()
        # Generate a link to download the result
        st.markdown(
            f'<a href="data:file/txt;base64,{transcript_encoded}" download="transcript.txt">Download Result</a>',
            unsafe_allow_html=True,
        )
