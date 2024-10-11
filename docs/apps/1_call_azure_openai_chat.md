# 1. Call Azure OpenAI Service API from Python

This app demonstrates how to call the Azure OpenAI Service API from Python.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service

## Overview

To call Azure OpenAI Service API, you can send HTTP requests directly to the API endpoint or use the [OpenAI Python API library](https://pypi.org/project/openai/).

**Send HTTP requests directly to the API endpoint**

```shell
YOUR_AOAI_NAME="your-aoai-name"
YOUR_DEPLOYMENT_ID="your-deployment-id"
YOUR_API_KEY="your-api-key"

curl -X 'POST' \
  "https://$YOUR_AOAI_NAME.openai.azure.com/openai/deployments/$YOUR_DEPLOYMENT_ID/chat/completions?api-version=2023-12-01-preview" \
  -H "api-key: $YOUR_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the weather like in Boston and New York?"}
    ]
  }'
```

**Use OpenAI Python API library**

```python
# Import modules
from os import getenv
from openai import AzureOpenAI

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
)

# Call completion API and get a response to user input
response = client.chat.completions.create(
    model=getenv("AZURE_OPENAI_GPT_MODEL"),
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
    ],
)
```

For more information, see the following references.

- API Reference: [Azure OpenAI Service REST API reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- OpenAPI Spec: [Cognitive Services AzureOpenAI SDKs](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference).

## Usage

1. Get Azure OpenAI Service API key
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
$ python apps/1_call_azure_openai_chat/main.py
```

### Example

To call the Azure OpenAI Service API, run the following command.

Detailed information is described in the [Quickstart: Get started using GPT-35-Turbo and GPT-4 with Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python).

```shell
$ python apps/1_call_azure_openai_chat/main.py
{
  "id": "chatcmpl-9tVzJwEczzb40cXT1gHZkk7ThX5Lm",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Hello! How can I assist you today?",
        "role": "assistant",
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1723018029,
  "model": "gpt-4o-2024-05-13",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_abc28019ad",
  "usage": {
    "completion_tokens": 9,
    "prompt_tokens": 18,
    "total_tokens": 27
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

## References

- Python basics
  - [Python Cheatsheet > Basics](https://www.pythoncheatsheet.org/cheatsheet/basics)
  - [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
- Azure OpenAI Basics
  - [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/ai-services/openai/)
  - [Quickstart: Get started generating text using Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python)
