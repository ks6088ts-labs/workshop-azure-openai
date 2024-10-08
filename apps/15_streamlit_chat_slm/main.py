import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

SUPPORTED_MODELS = [
    "phi3",
]
with st.sidebar:
    slm_model = st.selectbox(
        label="Model",
        options=SUPPORTED_MODELS,
        index=0,
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/15_streamlit_chat_slm/main.py)"


def is_configured():
    return slm_model in SUPPORTED_MODELS


st.title("15_streamlit_chat_slm")

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
    client = ChatOllama(
        model=slm_model,
        temperature=0,
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        response = client.invoke(
            input=st.session_state.messages,
        )
    msg = response.content
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": msg,
        }
    )
    st.chat_message("assistant").write(msg)
