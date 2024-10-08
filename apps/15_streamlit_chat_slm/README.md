# Streamlit Chat with SLM

## Overview

```shell
# Run Ollama server
$ ollama serve

# Install dependencies
$ ollama pull phi3

# Run a simple chat with Ollama
$ poetry run python apps/15_streamlit_chat_slm/chat.py

# Run summarization with SLM
$ poetry run python apps/15_streamlit_chat_slm/summarize.py

# Run streamlit app
$ poetry run python -m streamlit run apps/15_streamlit_chat_slm/main.py
```

# References

- [ChatOllama](https://python.langchain.com/docs/integrations/chat/ollama/)
- [Summarize Text](https://python.langchain.com/docs/tutorials/summarization/)
