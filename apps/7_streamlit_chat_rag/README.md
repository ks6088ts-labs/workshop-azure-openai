# Add RAG feature to Streamlit chat app

This app demonstrates how to add a feature to save chat history using Azure Cosmos DB to an Azure OpenAI Chat app using Streamlit.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service
- Azure AI Search

## Usage

1. Get Azure OpenAI Service API key
1. Get Azure AI Search API key
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run [main.py](./main.py)

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the script
$ python -m streamlit run apps/7_streamlit_chat_rag/main.py
```

### Example

Access `http://localhost:8501` and set the required fields in the sidebar to start a conversation.

When you send a question about Contoso Corporation, the chatbot will respond with an answer from Azure AI Search.

![RAG Chat](../../docs/images/7_streamlit_chat_rag.main.png)
