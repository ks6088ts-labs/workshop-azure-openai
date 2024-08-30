# Getting Started with Prompt flow

This application explains how to get started with [Prompt flow](https://github.com/microsoft/promptflow), a Python library that provides a simple and easy way to build conversational AI applications.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service

## Overview

Prompt flow is a suite of development tools designed to streamline the end-to-end development cycle of LLM-based AI applications, from ideation, prototyping, testing, evaluation to production deployment and monitoring. It makes prompt engineering much easier and enables you to build LLM apps with production quality.

## Usage

1. Get the API key for Azure OpenAI Service
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run scripts in the [apps/11_promptflow](./) directory

Set up the environment and install dependencies:

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

## Examples

[Prompt flow > Quick start](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html) provides a quick start guide to Prompt flow.

### [chat_minimal](https://github.com/microsoft/promptflow/tree/main/examples/flex-flows/chat-minimal)

**Run as normal Python script**

```shell
$ python apps/11_promptflow/chat_minimal/main.py
```

**Run from CLI**

```shell
$ cd apps/11_promptflow/chat_minimal

# Test flow
$ pf flow test \
    --flow main:chat \
    --inputs question="What's the capital of France?"

# Test flow: multi turn, access to http://localhost:{EPHEMERAL_PORT}
$ pf flow test \
    --flow main:chat \
    --ui

# Create run with multiple lines data
$ pf run create \
    --flow main:chat \
    --data ./data.jsonl \
    --column-mapping question='${data.question}' \
    --stream
```

## References

- [Prompt flow > repos](https://github.com/microsoft/promptflow)
- [Prompt flow > documents](https://microsoft.github.io/promptflow/)
