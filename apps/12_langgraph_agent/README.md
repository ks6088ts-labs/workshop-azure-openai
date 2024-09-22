# Create agents with LangGraph

This app demonstrates how to implement agents with LangGraph.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service

## Overview

**What is [LangGraph](https://langchain-ai.github.io/langgraph/)?**

LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows.

This chapter provides a practical example of how to use LangGraph to create an agent that can interact with users and external tools.

## Usage

1. Get Azure OpenAI Service API key
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run main.py

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the script
$ python apps/12_langgraph_agent/reflection_agent/main.py
```

### Example

## References

- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Udemy > LangGraph- Develop LLM powered agents with LangGraph](https://www.udemy.com/course/langgraph)
- [Prompt flow > Tracing](https://microsoft.github.io/promptflow/how-to-guides/tracing/index.html)
- [Reflection Agents](https://blog.langchain.dev/reflection-agents/)
- [LangChain > Reflexion](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/)
- [LangChain > Bing Search](https://python.langchain.com/docs/integrations/tools/bing_search/)
