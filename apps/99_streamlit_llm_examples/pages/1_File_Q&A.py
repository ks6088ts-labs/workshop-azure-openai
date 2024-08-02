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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/4_streamlit_chat_history/main.py)"

st.title("File Q&A")
st.info("ファイルをアップロードして質問をすると、AI が回答します")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "アップロードしたファイルについて質問してください",
    placeholder="簡潔な要約を作成してください",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    if (
        not azure_openai_api_key
        or not azure_openai_endpoint
        or not azure_openai_api_version
        or not azure_openai_gpt_model
    ):
        st.info("サイドバーに Azure OpenAI の設定を入力してください")
        st.stop()

    article = uploaded_file.read().decode()

    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    prompt = f"""参考資料:\n\n<article>
    {article}\n\n</article>\n\n質問: {question}"""

    # st.chat_message("user").write(prompt)
    print(prompt)
    response = client.chat.completions.create(
        model=azure_openai_gpt_model,
        messages=[
            {
                "role": "assistant",
                "content": "あなたはアップロードされたファイルについての質問に回答する AI です",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    msg = response.choices[0].message.content
    st.write("### 回答")
    st.chat_message("assistant").write(msg)
