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
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/4_Translate_text.py)"

st.title("Translate text")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("Please fill in the required fields at the sidebar.")
    st.stop()

st.info("This is a sample to translate text.")

supported_languages = [
    "English",
    "Japanese",
    "Polite Japanese",
    "Kansai dialect (Japanese)",
    "Aomori dialect (Japanese)",
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
# 2 column layout

# 1st row
row1_left, row1_right = st.columns(2)
with row1_left:
    target = st.selectbox(
        "Translate to",
        supported_languages,
        key="target",
        index=0,
    )

with row1_right:
    translate_button = st.button("Translate")

# 2nd row
row2_left, row2_right = st.columns(2)

default_input = """Hello, how are you?
"""

with row2_left:
    input = st.text_area(
        "Input",
        height=400,
        placeholder="Please enter the text to translate.",
        key="input",
        value=default_input,
    )

with row2_right:
    if input != "" and translate_button:
        with st.spinner("Translating..."):
            output = translate(
                target=target,
                input=input,
            )
            st.write(output)
