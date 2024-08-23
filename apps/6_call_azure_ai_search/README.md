# Call Azure AI Search from Python

This application explains how to call Azure AI Search from Python.

## Prerequisites

- Python 3.10 or later
- Azure AI Search
- Azure OpenAI Service

## Overview

Azure AI Search (formerly known as Azure Cognitive Search) is a fully managed cloud search service that provides information retrieval over user-owned content.
Data plane REST APIs are used for indexing and query workflows, and are documented in this section.
[Azure AI Search REST API reference](https://learn.microsoft.com/rest/api/searchservice/?view=rest-searchservice-2023-11-01) provides detailed information about the APIs.

REST API specs in OpenAPI format are available in the [Azure/azure-rest-api-specs](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/search/data-plane/Azure.Search) repository.

[Samples for Azure Cognitive Search client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples) are available in the Azure SDK for Python repository.

[Azure AI Search client library for Python - version 11.5.1](https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python) provides primitive APIs for working with Azure AI Search. It is flexible and allows you to work with the service at a lower level.

**Introducing LangChain**

[LangChain](https://github.com/langchain-ai/langchain) is a framework for developing applications powered by large language models (LLMs).
It provides a set of tools and libraries to help you build, train, and deploy LLMs in production.

![LangChain Framework](https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/svg/langchain_stack_062024.svg)

On the other hand, for example, the OpenAI Python SDK provides a direct interface to OpenAI's API, enabling developers to integrate OpenAI's powerful language models into their applications

The relationship between LangChain and the OpenAI Python SDK is complementary. LangChain leverages the OpenAI Python SDK to access and utilize OpenAI's models, providing a higher-level abstraction that simplifies the integration of these models into more complex workflows and applications.

**Use LangChain to access Azure AI Search easily**

[Azure AI Search](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/) interface in LangChain provides a simple and easy way to access Azure AI Search from Python.

**Use RecursiveCharacterTextSplitter to recursively split text by characters**

It is necessary to split text by characters when you need to put text into a search index.
Implementing text splitting by characters is a common task in natural language processing (NLP) and information retrieval (IR) applications but it is tedious and error-prone.
So we introduce `RecursiveCharacterTextSplitter` which provides a simple and easy way to recursively split text by characters. Details are available in the following link.

- [How to recursively split text by characters](https://python.langchain.com/v0.2/docs/how_to/recursive_text_splitter/)

## Usage

1. Get the API key for Azure AI Search
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run scripts in the [apps/6_call_azure_ai_search](./) directory

> [!CAUTION]
> `AZURE_AI_SEARCH_INDEX_NAME` in `.env` should be unique and should not be changed once set.
> If you change the index name, you will need to recreate the index and re-upload the documents.

Set up the environment and install dependencies:

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

Create an index in Azure AI Search and upload documents:

> [!CAUTION]
> This script should be run only once to avoid creating duplicate indexes.

```shell
$ python apps/6_call_azure_ai_search/1_create_index.py
```

Search documents in Azure AI Search:

```shell
$ python apps/6_call_azure_ai_search/2_search_index.py

> All meetings must include a 5-minute meditation session.
> All meetings must begin with a joke.
> All meetings must have a theme, such as pirate or superhero.
```
