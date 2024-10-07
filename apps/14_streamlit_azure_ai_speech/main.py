import pathlib
import subprocess
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Initialize the session state
if "transcribed_result" not in st.session_state:
    st.session_state["transcribed_result"] = ""

with st.sidebar:
    inference_type = st.selectbox(
        label="INEFERENCE_TYPE",
        options=[
            "azure",
            "local",
        ],
        key="INEFERENCE_TYPE",
    )
    azure_ai_speech_api_language = st.selectbox(
        label="AZURE_AI_SPEECH_API_LANGUAGE",
        options=[
            "en-US",
            "ja-JP",
        ],
        key="AZURE_AI_SPEECH_API_LANGUAGE",
    )
    if inference_type == "local":
        path_to_model = st.text_input(
            label="PATH_TO_MODEL",
            value="./model",
            key="PATH_TO_MODEL",
            type="default",
        )
        stt_host = st.text_input(
            label="STT_HOST",
            value="ws://localhost:5000",
            key="STT_HOST",
            type="default",
        )
        st.warning("yet to be implemented")
    if inference_type == "azure":
        azure_openai_endpoint = st.text_input(
            label="AZURE_OPENAI_ENDPOINT",
            value=getenv("AZURE_OPENAI_ENDPOINT"),
            key="AZURE_OPENAI_ENDPOINT",
            type="default",
        )
        azure_openai_api_key = st.text_input(
            label="AZURE_OPENAI_API_KEY",
            value=getenv("AZURE_OPENAI_API_KEY"),
            key="AZURE_OPENAI_API_KEY",
            type="password",
        )
        azure_openai_api_version = st.text_input(
            label="AZURE_OPENAI_API_VERSION",
            value=getenv("AZURE_OPENAI_API_VERSION"),
            key="AZURE_OPENAI_API_VERSION",
            type="default",
        )
        azure_openai_gpt_model = st.text_input(
            label="AZURE_OPENAI_GPT_MODEL",
            value=getenv("AZURE_OPENAI_GPT_MODEL"),
            key="AZURE_OPENAI_GPT_MODEL",
            type="default",
        )
        azure_ai_speech_api_subscription_key = st.text_input(
            label="AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY",
            value=getenv("AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY"),
            key="AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY",
            type="password",
        )
        azure_ai_speech_api_region = st.text_input(
            label="AZURE_AI_SPEECH_API_REGION",
            value=getenv("AZURE_AI_SPEECH_API_REGION"),
            key="AZURE_AI_SPEECH_API_REGION",
            type="default",
        )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/14_streamlit_azure_ai_speech/main.py)"


def is_configured():
    if inference_type == "local":
        return path_to_model and stt_host
    if inference_type == "azure":
        return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


st.title("transcribe text")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

st.info("This is a sample to transcribe text.")

# ---
# 2 column layout

# 1st row
row1_left, row1_right = st.columns(2)
with row1_left:
    input = st.text_area(
        "Transcribed text",
        height=400,
        placeholder="Please enter the text to transcribe.",
        key="input",
        value=st.session_state["transcribed_result"],
    )

with row1_right:
    start_transcribe_button = st.button("start", disabled=not is_configured())
    stop_transcribe_button = st.button("stop", disabled=not is_configured())
    transcription_status = st.empty()

# line break horizontal line
st.markdown("---")

# 2nd row
row2_left, row2_right = st.columns(2)

with row2_left:
    selected_task = st.selectbox(
        "Task",
        [
            "Create summaries from the following text",
            "Extract 3 main points from the following text",
            # Add more tasks here
        ],
        key="selected_task",
        index=0,
    )

with row2_right:
    run_task_button = st.button("run_task", disabled=not is_configured())

path_to_transcribed_text = ".transcribed.txt"


def start_recognition():
    global process
    if inference_type == "local":
        command = f"python apps/14_streamlit_azure_ai_speech/speech_to_text.py --output {path_to_transcribed_text} --endpoint {stt_host} --language {azure_ai_speech_api_language} --type local --verbose"  # noqa
        process = subprocess.Popen(command, shell=True)
        st.warning("Local inference is not yet implemented.")
        return
    if inference_type == "azure":
        command = f"python apps/14_streamlit_azure_ai_speech/speech_to_text.py --output {path_to_transcribed_text} --subscription {azure_ai_speech_api_subscription_key} --region {azure_ai_speech_api_region} --language {azure_ai_speech_api_language} --type azure --verbose"  # noqa
        process = subprocess.Popen(command, shell=True)


def run_task(selected_task: str, input: str) -> str:
    if inference_type == "local":
        st.warning("Local inference is not yet implemented.")
        return
    if inference_type == "azure":
        client = AzureOpenAI(
            api_key=azure_openai_api_key,
            api_version=azure_openai_api_version,
            azure_endpoint=azure_openai_endpoint,
        )

        response = client.chat.completions.create(
            model=azure_openai_gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
                        Task: {selected_task}.
                        ---
                        {input}
                        ---
                    """,
                },
            ],
        )
        return response.choices[0].message.content
    raise ValueError(f"Inference type is not supported: {inference_type}")


def load_transcribed_text():
    with open(path_to_transcribed_text) as f:
        return f.read()


if start_transcribe_button:
    if not st.session_state.get("process"):
        transcription_status.info(f"Transcribing... (language={azure_ai_speech_api_language})")
        start_recognition()
    else:
        transcription_status.warning("Transcription is already running.")

if stop_transcribe_button:
    pathlib.Path(".stop").touch()
    output = load_transcribed_text()
    st.session_state.transcribed_result = output
    st.rerun()

if run_task_button:
    with st.spinner("Running..."):
        output = run_task(
            selected_task=selected_task,
            input=input,
        )
        st.write(output)
