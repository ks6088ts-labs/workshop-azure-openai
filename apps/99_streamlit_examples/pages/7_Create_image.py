import json
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
    azure_openai_dalle_model = st.text_input(
        label="AZURE_OPENAI_DALLE_MODEL",
        value=getenv("AZURE_OPENAI_DALLE_MODEL"),
        key="AZURE_OPENAI_DALLE_MODEL",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/7_Create_image.py)"

st.title("Create image")

if (
    not azure_openai_api_key
    or not azure_openai_endpoint
    or not azure_openai_api_version
    or not azure_openai_dalle_model
):
    st.warning("Please fill in the required fields at the sidebar.")
    st.stop()

st.info("Create an image from a text description.")

description = st.text_input(
    "Describe the image",
    placeholder="Please describe the content of the image",
)

if description:
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    with st.spinner("Thinking..."):
        result = client.images.generate(
            model=azure_openai_dalle_model,
            prompt=description,
            n=1,
        )
        json_response = json.loads(result.model_dump_json())

    st.link_button("Show image", json_response["data"][0]["url"])
    st.write(json_response)
