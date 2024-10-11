# 11. Getting Started with Prompt flow

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
Some of the examples are extracted from [github.com/microsoft/promptflow/examples](https://github.com/microsoft/promptflow/tree/main/examples) to guide you through the basic usage of Prompt flow.

**Set up connection**

```shell
$ cd apps/11_promptflow

# List connections
$ pf connection list

# Set parameters
$ AZURE_OPENAI_KEY=<your_api_key>
$ AZURE_OPENAI_ENDPOINT=<your_api_endpoint>
$ CONNECTION_NAME=open_ai_connection

# Delete connection (if needed)
$ pf connection delete \
    --name $CONNECTION_NAME

# Create connection
$ pf connection create \
    --file connection_azure_openai.yaml \
    --set api_key=$AZURE_OPENAI_KEY \
    --set api_base=$AZURE_OPENAI_ENDPOINT \
    --name $CONNECTION_NAME

# Show connection
$ pf connection show \
    --name $CONNECTION_NAME
```

### [chat_minimal](https://github.com/microsoft/promptflow/tree/main/examples/flex-flows/chat-minimal)

A chat flow defined using function with minimal code. It demonstrates the minimal code to have a chat flow.

Tracing feature is available in Prompt flow, which allows you to trace the flow of the conversation. You can see its implementation in this example.
Details are available in [Tracing](https://microsoft.github.io/promptflow/how-to-guides/tracing/index.html)

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

`--column-mapping` is used to map the data in the JSONL file to the flow. For more details, refer to [Use column mapping](https://microsoft.github.io/promptflow/how-to-guides/run-and-evaluate-a-flow/use-column-mapping.html).

### playground_chat

```shell
cd apps/11_promptflow

# Initialize a new flow
$ pf flow init \
    --flow playground_chat \
    --type chat

$ cd playground_chat

# Interact with chat flow
$ pf flow test \
    --flow . \
    --interactive

# Test flow
$ pf flow test \
    --flow . \
    --inputs question="What's the capital of France?"

# Create run with multiple lines data
$ RUN_NAME=playground_chat-$(date +%s)
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping question='${data.question}' \
    --stream

# Show run details
$ pf run show-details --name $RUN_NAME
```

### playground_evaluation

```shell
cd apps/11_promptflow

# Initialize a new flow
$ pf flow init \
    --flow playground_evaluation \
    --type evaluation

$ cd playground_evaluation

# Create run with multiple lines data
$ RUN_NAME=playground_evaluation-$(date +%s)
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping \
        groundtruth='${data.groundtruth}' \
        prediction='${data.prediction}' \
    --stream

# Show run details
$ pf run show-details --name $RUN_NAME
```

### playground_standard

```shell
cd apps/11_promptflow

# Initialize a new flow
$ pf flow init \
    --flow playground_standard \
    --type standard

$ cd playground_standard

# Create run with multiple lines data
$ RUN_NAME=playground_standard-$(date +%s)
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping text='${data.text}' \
    --stream

# Show run details
$ pf run show-details --name $RUN_NAME
```

### image_qa

To run the image QA flow with GPT-4o, we customize an LLM tool.
Following documents provide more details:

- docs: [Customizing an LLM Tool](https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/customize_an_llm_tool.html)
- example codes: [promptflow/examples/flows/chat/chat-with-image](https://github.com/microsoft/promptflow/tree/main/examples/flows/chat/chat-with-image)

With the image QA flow sample, you can ask questions about an image and get answers from the model.

```shell
cd apps/11_promptflow/image_qa

# Create run with multiple lines data
$ RUN_NAME=image_qa-$(date +%s)
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping image='${data.image}' \
    --stream

# Show run details
$ pf run show-details --name $RUN_NAME
```

### [chat-math-variant](https://github.com/microsoft/promptflow/tree/main/examples/flows/chat/chat-math-variant)

Tuning prompts using `variants` is a powerful feature in Prompt flow. It allows you to test different prompts and see which one works best for your use case.

Prompt flow repository provides an example of a chat flow with math variants at [examples/flows/chat/chat-math-variant](https://github.com/microsoft/promptflow/tree/main/examples/flows/chat/chat-math-variant).

To understand how to use variants, you can refer to the [How-to Guides > Tune prompts using variants](https://microsoft.github.io/promptflow/how-to-guides/tune-prompts-with-variants.html) document.

```shell
cd apps/11_promptflow/chat-math-variant

# Create run with multiple lines data with variant
$ RUN_NAME=chat-math-variant-$(date +%s)
$ VARIANT='${chat.variant_0}'
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping question='${data.question}' \
    --variant $VARIANT \
    --stream

# Show run details
$ pf run show-details --name $RUN_NAME
```

[Tutorial: How prompt flow helps on quality improvement](https://github.com/microsoft/promptflow/blob/main/examples/tutorials/flow-fine-tuning-evaluation/promptflow-quality-improvement.md) provides a detailed guide on how to use Prompt flow to improve the quality of your LLM applications.

### [eval-chat-math](https://github.com/microsoft/promptflow/tree/main/examples/flows/evaluation/eval-chat-math)

This example shows how to evaluate the answer of math questions, which can compare the output results with the standard answers numerically.
Details are available in the [eval-chat-math/README.md](./eval-chat-math/README.md).
To understand how to operate the flow in VS Code, you can refer to the [Build your high quality LLM apps with Prompt flow](https://www.youtube.com/watch?v=gcIe6nk2gA4).
This video shows how to evaluate the answer of math questions and guide you to tune the prompts using variants.

### flex_flow_langchain

To guide you through working with LangChain, we provide an example flex flow that

```shell
$ cd apps/11_promptflow/flex_flow_langchain
$ pf flow test \
    --flow main:LangChainRunner \
    --inputs question="What's 2+2?" \
    --init custom_connection=open_ai_connection

$ RUN_NAME=flex_flow_langchain-$(date +%s)
$ pf run create \
    --name $RUN_NAME \
    --flow . \
    --data ./data.jsonl \
    --column-mapping question='${data.question}' \
    --stream

$ pf run show-details --name $RUN_NAME
```

### evaluators

To guide you through working with evaluators, a helpful document is available at [Evaluate with the prompt flow SDK](https://learn.microsoft.com/azure/ai-studio/how-to/develop/flow-evaluate-sdk).

```shell
# Show help
python apps/11_promptflow/evaluators/main.py --help
```

<!-- TODO: rag, deployments -->

## References

- [Repository](https://github.com/microsoft/promptflow)
  - [examples](https://github.com/microsoft/promptflow/tree/main/examples)
- [Documents](https://microsoft.github.io/promptflow/)
  - [How-to Guides](https://microsoft.github.io/promptflow/how-to-guides/index.html)
  - [Tutorials](https://microsoft.github.io/promptflow/tutorials/index.html#)
