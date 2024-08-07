# Call Azure AI Search from Python

This application explains how to call Azure AI Search from Python.

## Prerequisites

- Python 3.10 or later
- Azure AI Search
- Azure OpenAI Service

## Usage

1. Get the API key for Azure AI Search
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run scripts in the [apps/6_call_azure_ai_search](./) directory

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Create an index in Azure AI Search and upload documents
# Note: This script should be run only once to avoid creating duplicate indexes
$ python apps/6_call_azure_ai_search/1_create_index.py

# Search documents in Azure AI Search
$ python apps/6_call_azure_ai_search/2_search_index.py

> All meetings must include a 5-minute meditation session.
> All meetings must begin with a joke.
> All meetings must have a theme, such as pirate or superhero.
```

## References

- [How to recursively split text by characters](https://python.langchain.com/v0.2/docs/how_to/recursive_text_splitter/)
- [LangChain > Azure AI Search](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/)
