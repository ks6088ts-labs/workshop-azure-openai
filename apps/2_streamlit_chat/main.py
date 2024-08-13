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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/2_streamlit_chat/main.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


st.title("2_streamlit_chat")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! I'm a helpful assistant.",
        }
    ]

# Show chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Receive user input
if prompt := st.chat_input(disabled=not is_configured()):
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=azure_openai_gpt_model,
            messages=st.session_state.messages,
        )
    msg = response.choices[0].message.content
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": msg,
        }
    )
    st.chat_message("assistant").write(msg)
