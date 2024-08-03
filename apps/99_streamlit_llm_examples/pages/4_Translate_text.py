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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_llm_examples/pages/4_Translate_text.py)"

st.title("Translate text")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("サイドバーに Azure OpenAI の設定を入力してください")
    st.stop()

st.info("翻訳アプリ")

supported_languages = [
    "英語",
    "日本語",
    "丁寧な日本語",
    "関西弁",
    "青森弁",
]


def translate(target: str, input: str) -> str:
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
                    You are a professional translator. Please translate the following text into {target}.
                    ---
                    {input}
                    ---
                """,
            },
        ],
    )
    return response.choices[0].message.content


# ---
# 2カラムレイアウト

# 1行目
row1_left, row1_right = st.columns(2)
with row1_left:
    target = st.selectbox(
        "ターゲット言語",
        supported_languages,
        key="target",
        index=0,
    )

with row1_right:
    translate_button = st.button("翻訳")

# 2行目
row2_left, row2_right = st.columns(2)

default_input = """むかし、むかし、ある所におじいさんとおばあさんが住んでいました。
おじいさんは山へしば刈りに、おばあさんは川へ洗濯に行きました。
おばあさんが川で洗濯をしていると大きな桃が流れてきました。
「なんと大きな桃じゃろう！家に持って帰ろう。」
とおばあさんは背中に担いで家に帰り、その桃を切ろうとすると、なんと桃から大きな赤ん坊が出てきたのです。
「おっとたまげた。」
二人は驚いたけれども、とても喜び、
「何という名前にしましょうか。」
「桃から生まれたから、桃太郎というのはどうだろう。」
「それがいい。」
桃太郎はあっと言う間に大きくなり、立派な優しい男の子になりました。
"""

with row2_left:
    input = st.text_area(
        "入力テキスト",
        height=400,
        placeholder="翻訳したい文章を入力してください",
        key="input",
        value=default_input,
    )

with row2_right:
    if input != "" and translate_button:
        with st.spinner("翻訳中..."):
            output = translate(
                target=target,
                input=input,
            )
            st.write(output)
