import base64
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
    azure_openai_gpt_model = st.text_input(
        label="AZURE_OPENAI_GPT_MODEL",
        value=getenv("AZURE_OPENAI_GPT_MODEL"),
        key="AZURE_OPENAI_GPT_MODEL",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/8_streamlit_azure_openai_batch/main.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


def get_client():
    return AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )


st.title("8_streamlit_azure_openai_batch")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

# ---------------
# Upload batch file
# ---------------
st.header("Upload batch file")
st.info("Upload a file in JSON lines format (.jsonl)")
uploaded_file = st.file_uploader("Upload an input file in JSON lines format", type=("jsonl"))
if uploaded_file:
    bytes_data = uploaded_file.read()
    st.write(bytes_data.decode().split("\n"))
    if st.button(
        "Submit",
        key="submit",
        disabled=not is_configured(),
    ):
        temp_file_path = "tmp.jsonl"
        with open(temp_file_path, "wb") as f:
            f.write(bytes_data)
        with st.spinner("Uploading..."):
            try:
                response = get_client().files.create(
                    # FIXME: hardcoded for now, use uploaded_file
                    file=open(temp_file_path, "rb"),
                    purpose="batch",
                )
                st.write(response.model_dump())
            except Exception as e:
                st.error(e)
st.markdown("---")

# ---------------
# Track file upload status
# ---------------
st.header("Track file upload status")
st.info("Track the file upload status using the file ID.")
track_file_id = st.text_input(
    label="File ID",
    key="track_file_id",
    help="Enter the file ID to track the file upload status",
)
if st.button(
    "Track",
    key="track",
    disabled=not track_file_id or not is_configured(),
):
    with st.spinner("Tracking..."):
        try:
            response = get_client().files.retrieve(track_file_id)
            st.write(response.model_dump())
            st.write(f"status: {response.status}")
        except Exception as e:
            st.error(e)
st.markdown("---")

# ---------------
# Create batch job
# ---------------
st.header("Create batch job")
st.info("Create a batch job using the file ID")
batch_file_id = st.text_input(
    label="File ID",
    key="batch_file_id",
    help="Enter the file ID to create a batch job",
)
if st.button(
    "Create batch job",
    key="create",
    disabled=not batch_file_id or not is_configured(),
):
    with st.spinner("Creating..."):
        try:
            response = get_client().batches.create(
                input_file_id=batch_file_id,
                endpoint="/chat/completions",
                completion_window="24h",
            )
            st.write(response.model_dump())
        except Exception as e:
            st.error(e)
st.markdown("---")

# ---------------
# Track batch job progress
# ---------------
st.header("Track batch job progress")
st.info("Track the batch job progress using the job ID")
track_batch_job_id = st.text_input(
    label="Batch job ID",
    key="track_batch_job_id",
    help="Enter the batch job ID to track the job progress",
)
if st.button(
    "Track batch job",
    key="track_batch_job",
    disabled=not track_batch_job_id or not is_configured(),
):
    with st.spinner("Tracking..."):
        try:
            response = get_client().batches.retrieve(track_batch_job_id)
            st.write(response.model_dump())
            st.write(f"status: {response.status}")
            st.write(f"output_file_id: {response.output_file_id}")
        except Exception as e:
            st.error(e)
st.markdown("---")

# ---------------
# Retrieve batch job output file
# ---------------
st.header("Retrieve batch job output file")
st.info("Retrieve the batch job output file using the job ID")
output_file_id = st.text_input(
    label="output_file_id",
    key="retrieve_batch_job_id",
    help="Enter the batch job ID to retrieve the output file",
)
if st.button(
    "Retrieve batch job output file",
    key="retrieve_batch_job",
    disabled=not output_file_id or not is_configured(),
):
    with st.spinner("Retrieving..."):
        try:
            file_response = get_client().files.content(output_file_id)
            raw_responses = file_response.text.strip().split("\n")

            for raw_response in raw_responses:
                json_response = json.loads(raw_response)
            st.write(json_response)

            output_encoded = base64.b64encode(json.dumps(json_response, indent=2).encode()).decode()
            # Generate a link to download the result
            st.markdown(
                f'<a href="data:file/txt;base64,{output_encoded}" download="{output_file_id}.json">Download Result</a>',
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(e)
