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
    azure_openai_gpt_model = st.text_input(
        label="AZURE_OPENAI_GPT_MODEL",
        value=getenv("AZURE_OPENAI_GPT_MODEL"),
        key="AZURE_OPENAI_GPT_MODEL",
        type="default",
    )
    "[Go to Azure Portal to get an Azure OpenAI API key](https://portal.azure.com/)"
    "[Go to Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_llm_examples/pages/1_File_Q&A.py)"

st.title("Image Q&A")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("サイドバーに Azure OpenAI の設定を入力してください")
    st.stop()

st.info("ファイルをアップロードして質問をすると、AI が回答します")

uploaded_file = st.file_uploader(
    "Upload an article",
    type=(
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
    ),
)
question = st.text_input(
    "アップロードしたファイルについて質問してください",
    placeholder="画像の内容について説明してください",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    encoded_image = base64.b64encode(uploaded_file.read()).decode()

    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    print(question)
    with st.spinner("考え中..."):
        response = client.chat.completions.create(
            model=azure_openai_gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": "あなたはアップロードされた画像についての質問に日本語で回答する AI です",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                        },
                        {
                            "type": "text",
                            "content": question,
                        },
                    ],
                },
            ],
        )
    msg = response.choices[0].message.content
    st.write("### 回答")
    st.chat_message("assistant").write(msg)
