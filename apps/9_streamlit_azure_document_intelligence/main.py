import base64
import json
from os import getenv

import streamlit as st
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, ContentFormat
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

with st.sidebar:
    azure_document_intelligence_endpoint = st.text_input(
        label="AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        value=getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        key="AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        type="default",
    )
    azure_document_intelligence_api_version = st.text_input(
        label="AZURE_DOCUMENT_INTELLIGENCE_API_VERSION",
        value=getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION"),
        key="AZURE_DOCUMENT_INTELLIGENCE_API_VERSION",
        type="default",
    )
    azure_document_intelligence_api_key = st.text_input(
        label="AZURE_DOCUMENT_INTELLIGENCE_API_KEY",
        key="AZURE_DOCUMENT_INTELLIGENCE_API_KEY",
        type="password",
    )
    output_content_format = st.selectbox(
        label="output_content_format",
        key="output_content_format",
        options=[
            ContentFormat.MARKDOWN,
            ContentFormat.TEXT,
        ],
        index=0,
        format_func=lambda x: x.value,
    )

    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/9_streamlit_azure_document_intelligence/main.py)"


def is_configured():
    return (
        azure_document_intelligence_endpoint
        and azure_document_intelligence_api_version
        and azure_document_intelligence_api_key
    )


def get_client():
    return DocumentIntelligenceClient(
        credential=AzureKeyCredential(azure_document_intelligence_api_key),
        endpoint=azure_document_intelligence_endpoint,
        api_version=azure_document_intelligence_api_version,
    )


st.title("9_streamlit_azure_document_intelligence")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

# ---------------
# Upload file
# ---------------
st.header("Upload file")
st.info("Upload a file")
uploaded_file = st.file_uploader(
    "Upload an input file",
    type=(
        "txt",
        "text",
        "pdf",
        "pptx",
        "jpg",
        "jpeg",
        "png",
    ),
)
if uploaded_file:
    bytes_data = uploaded_file.read()
    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")
    st.write(f"File size: {len(bytes_data)} bytes")

if st.button(
    "Analyze",
    key="Analyze",
    disabled=not is_configured(),
):
    with st.spinner("Analyzing..."):
        try:
            poller = get_client().begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=bytes_data,
                content_type="application/octet-stream",
                output_content_format=output_content_format,
            )
            result: AnalyzeResult = poller.result()
            output_encoded = base64.b64encode(
                json.dumps(
                    result.as_dict(),
                    indent=2,
                ).encode()
            ).decode()
            # Generate a link to download the result
            st.markdown(
                f'<a href="data:file/txt;base64,{output_encoded}" \
                    download="{uploaded_file.name}.{output_content_format}.json">Download Result</a>',
                unsafe_allow_html=True,
            )
            st.write(result.as_dict())
        except Exception as e:
            st.error(e)
