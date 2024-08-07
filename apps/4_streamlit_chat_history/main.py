from os import getenv
from pprint import pprint
from uuid import uuid4

import streamlit as st
from azure.cosmos import ContainerProxy, CosmosClient, PartitionKey
from dotenv import load_dotenv
from openai import AzureOpenAI
from streamlit.runtime.scriptrunner import get_script_run_ctx

load_dotenv()


def get_container_client() -> ContainerProxy:
    client = CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING"))
    database = client.create_database_if_not_exists(id=getenv("AZURE_COSMOS_DB_DATABASE_NAME"))
    return database.create_container_if_not_exists(
        id=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
        partition_key=PartitionKey(
            path="/id",
            kind="Hash",
        ),
    )


def get_session_id():
    return get_script_run_ctx().session_id


def store_chat_history(container: ContainerProxy):
    response = container.create_item(
        body={
            "id": uuid4().hex,
            "session_id": get_session_id(),
            "messages": st.session_state.messages,
        }
    )
    pprint(response)


# To reuse the session for Cosmos DB, just define the container globally
container = get_container_client()

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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/4_streamlit_chat_history/main.py)"

st.title("4_streamlit_chat_history")
if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("Please fill in the required fields at the sidebar.")
    st.stop()

st.write(f"Session ID: {get_session_id()}")

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
if prompt := st.chat_input():
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
    # !! Here's the only difference from apps/2_streamlit_chat/main.py
    store_chat_history(container)
    st.chat_message("assistant").write(msg)
