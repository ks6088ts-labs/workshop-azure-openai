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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/1_File_Q&A.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


st.title("File Q&A")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

st.info("Upload a file and ask a question. AI will answer the question.")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask a question about the uploaded file",
    placeholder="Please describe the content of the image",
    disabled=not uploaded_file,
)

if uploaded_file and question and is_configured():
    article = uploaded_file.read().decode()

    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    prompt = f"""Reference:\n\n<article>
    {article}\n\n</article>\n\nQuestion: {question}"""

    # st.chat_message("user").write(prompt)
    print(prompt)
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=azure_openai_gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional data analyst. Explain the given data.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
    msg = response.choices[0].message.content
    st.write("### Answer:")
    st.chat_message("assistant").write(msg)
