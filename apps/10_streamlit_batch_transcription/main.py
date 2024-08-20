from os import getenv
from urllib.parse import urljoin

import requests
import streamlit as st
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

with st.sidebar:
    "[Microsoft Learn > What is batch transcription?](https://learn.microsoft.com/azure/ai-services/speech-service/batch-transcription)"
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/10_streamlit_batch_transcription/main.py)"


st.title("10_streamlit_batch_transcription")

# ---------------
# Upload an audio file
# ---------------
st.header("Upload audio file")
st.info("Upload an audio file to transcribe")
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=(
        "wav",
        "mp3",
    ),
)
if uploaded_file:
    bytes_data = uploaded_file.read()
    if st.button(
        "Submit",
        key="submit",
    ):
        with st.spinner("Uploading..."):
            try:
                response = (
                    BlobServiceClient(
                        account_url=getenv("AZURE_BLOB_ACCOUNT_URL"),
                        credential=getenv("AZURE_BLOB_SAS_TOKEN"),
                    )
                    .get_blob_client(
                        container=getenv("AZURE_BLOB_CONTAINER_NAME"),
                        blob=uploaded_file.name,
                    )
                    .upload_blob(
                        data=bytes_data,
                        blob_type="BlockBlob",
                        overwrite=True,
                    )
                )
                st.success("Uploaded successfully")
                st.write(response)

            except Exception as e:
                st.error(e)
st.markdown("---")

# ---------------
# Create a batch transcription: https://learn.microsoft.com/azure/ai-services/speech-service/batch-transcription-create?pivots=rest-api
# ---------------
st.header("Create a batch transcription")
st.info("Create a batch transcription")
blob_name = st.text_input(
    label="Blob name",
    key="blob_name",
    help="Enter the blob name to create a batch transcription",
)
if st.button(
    "Create a batch transcription",
    key="create",
    disabled=not blob_name,
):
    with st.spinner("Creating..."):
        try:
            response = requests.post(
                url=urljoin(
                    getenv("AZURE_AI_SPEECH_API_ENDPOINT"),
                    "speechtotext/v3.2/transcriptions",
                ),
                headers={
                    "Ocp-Apim-Subscription-Key": getenv("AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY"),
                    "Content-Type": "application/json",
                },
                json={
                    "contentUrls": [
                        urljoin(
                            getenv("AZURE_BLOB_ACCOUNT_URL"),
                            f"{getenv('AZURE_BLOB_CONTAINER_NAME')}/{blob_name}",
                        ),
                    ],
                    "locale": "ja-JP",
                    "displayName": "My Transcription",
                    "model": None,
                    "properties": {
                        "wordLevelTimestampsEnabled": True,
                        "languageIdentification": {
                            "candidateLocales": ["ja-JP", "en-US"],
                        },
                    },
                },
            )
            response.raise_for_status()
            st.success("Created successfully")
            st.write(response)
            st.write(response.json())
            st.write(f"Transcription ID: {response.json()['self'].split('/')[-1]}")
        except Exception as e:
            st.error(e)
st.markdown("---")

# ---------------
# Get transcription status
# ---------------
st.header("Get transcription status")
st.info("Get transcription status")
transcription_id = st.text_input(
    label="Transcription ID",
    key="transcription_id",
    help="Enter the batch transcription ID",
)
if st.button(
    "Get transcription status",
    key="get_transcription_status",
    disabled=not transcription_id,
):
    with st.spinner("Retrieving..."):
        try:
            response = requests.get(
                url=urljoin(
                    getenv("AZURE_AI_SPEECH_API_ENDPOINT"),
                    f"speechtotext/v3.2/transcriptions/{transcription_id}",
                ),
                headers={
                    "Ocp-Apim-Subscription-Key": getenv("AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY"),
                },
            )
            response.raise_for_status()
            st.write(response.json())
        except Exception as e:
            st.error(e)
st.markdown("---")

# ---------------
# Get transcription results
# ---------------
st.header("Get transcription results")
st.info("Get transcription results")
transcription_id_result = st.text_input(
    label="transcription_id_result",
    key="transcription_id_result",
    help="Enter the batch transcription ID",
)
if st.button(
    "Get transcription results",
    key="get_transcription_results",
    disabled=not transcription_id_result,
):
    with st.spinner("Retrieving..."):
        try:
            response = requests.get(
                url=urljoin(
                    getenv("AZURE_AI_SPEECH_API_ENDPOINT"),
                    f"speechtotext/v3.2/transcriptions/{transcription_id_result}/files",
                ),
                headers={
                    "Ocp-Apim-Subscription-Key": getenv("AZURE_AI_SPEECH_API_SUBSCRIPTION_KEY"),
                },
            )
            response.raise_for_status()
            st.write(response.json())
        except Exception as e:
            st.error(e)
