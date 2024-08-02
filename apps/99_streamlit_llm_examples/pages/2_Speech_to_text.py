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
    "[Go to Azure Portal to get an Azure OpenAI API key](https://portal.azure.com/)"
    "[Go to Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_llm_examples/pages/2_Speech_to_text.py)"

st.title("Speech to text")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_stt_model:
    st.warning("サイドバーに Azure OpenAI の設定を入力してください")
    st.stop()

st.info("ファイルをアップロードすると、AI が音声をテキストに変換します。結果はダウンロードできます。")

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

    if st.button("音声文字起こしを実行する"):
        with st.spinner("考え中..."):
            response = client.audio.transcriptions.create(
                model=azure_openai_stt_model,
                file=uploaded_file,
                response_format="text",
            )
        st.write(response)
        transcript_encoded = base64.b64encode(response.encode()).decode()
        # ダウンロードリンクを作成する
        st.markdown(
            f'<a href="data:file/txt;base64,{transcript_encoded}" download="transcript.txt">Download Result</a>',
            unsafe_allow_html=True,
        )
