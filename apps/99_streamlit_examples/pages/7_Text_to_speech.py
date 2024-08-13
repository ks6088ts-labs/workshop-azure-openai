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
    azure_openai_tts_model = st.text_input(
        label="AZURE_OPENAI_TTS_MODEL",
        value=getenv("AZURE_OPENAI_TTS_MODEL"),
        key="AZURE_OPENAI_TTS_MODEL",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/7_Text_to_speech.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_tts_model


st.title("Text to speech")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

st.info("This is a sample to convert text to speech.")

content = st.text_area(
    label="Text to speech",
    value="",
)
st.write(f"You wrote {len(content)} characters.")

voice_option = st.selectbox(
    "Select voice",
    (
        "alloy",
        "echo",
        "fable",
        "onyx",
        "nova",
        "shimmer",
    ),
)

if st.button("Convert", disabled=not content or not is_configured()):
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )
    path_to_output = "output.mp3"

    with st.spinner("Converting..."):
        response = client.audio.speech.create(
            input=content,
            voice=voice_option,
            model=azure_openai_tts_model,
            response_format="mp3",
        )
        response.write_to_file(path_to_output)

    st.audio(
        data=path_to_output,
        format="audio/mpeg",
        loop=False,
    )
