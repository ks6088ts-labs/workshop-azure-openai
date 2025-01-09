# 15. Streamlit Chat with SLM

## Overview

```shell
# Run Ollama server
$ ollama serve

# Pull Phi3 model
$ ollama pull phi3

# Run a simple chat with Ollama
$ poetry run python apps/15_streamlit_chat_slm/chat.py

# Run summarization with SLM
$ poetry run python apps/15_streamlit_chat_slm/summarize.py

# Run streamlit app
$ poetry run python -m streamlit run apps/15_streamlit_chat_slm/main.py

# List models
$ ollama list
NAME           ID              SIZE      MODIFIED
phi3:latest    4f2222927938    2.2 GB    3 minutes ago
phi4:latest    ac896e5b8b34    9.1 GB    55 minutes ago
```

## Usage

### Use Phi3 model

```shell
# Pull Phi3 model
$ ollama pull phi3

# Measure time to run the chat
$ time poetry run python apps/15_streamlit_chat_slm/chat.py \
  --model phi3 \
  --prompt "hello"
{
  "content": "Hello! How can I help you today?",
  "additional_kwargs": {},
  "response_metadata": {
    "model": "phi3",
    "created_at": "2025-01-09T03:30:05.706397262Z",
    "message": {
      "role": "assistant",
      "content": ""
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 540964618,
    "load_duration": 5078297,
    "prompt_eval_count": 22,
    "prompt_eval_duration": 229000000,
    "eval_count": 10,
    "eval_duration": 305000000
  },
  "type": "ai",
  "name": null,
  "id": "run-54f0d2a6-b3d4-4ef5-b009-0c72b23297ac-0",
  "example": false,
  "tool_calls": [],
  "invalid_tool_calls": [],
  "usage_metadata": {
    "input_tokens": 22,
    "output_tokens": 10,
    "total_tokens": 32
  }
}
poetry run python apps/15_streamlit_chat_slm/chat.py --model phi3 --prompt   1.57s user 0.16s system 68% cpu 2.515 total
```

### Use Phi4 model

```shell
# Pull Phi4 model
$ ollama pull phi4

# Measure time to run the chat
$ time poetry run python apps/15_streamlit_chat_slm/chat.py \
  --model phi4 \
  --prompt "hello"
{
  "content": "Hello! How can I assist you today? If you have any questions or need information, feel free to let me know. 😊",
  "additional_kwargs": {},
  "response_metadata": {
    "model": "phi4",
    "created_at": "2025-01-09T03:16:19.661532868Z",
    "message": {
      "role": "assistant",
      "content": ""
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 10662476906,
    "load_duration": 10769327,
    "prompt_eval_count": 23,
    "prompt_eval_duration": 426000000,
    "eval_count": 28,
    "eval_duration": 10223000000
  },
  "type": "ai",
  "name": null,
  "id": "run-16375018-116e-422f-afd4-84692af42bd6-0",
  "example": false,
  "tool_calls": [],
  "invalid_tool_calls": [],
  "usage_metadata": {
    "input_tokens": 23,
    "output_tokens": 28,
    "total_tokens": 51
  }
}
poetry run python apps/15_streamlit_chat_slm/chat.py --model phi4 --prompt   1.48s user 0.12s system 12% cpu 12.455 total
```

Note:

- Update Ollama to the latest version to run phi4 model
- To use Ollama on WSL2, you may need to enable systemd. For more information, see [Use systemd to manage Linux services with WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd#how-to-enable-systemd)

# References

- [ChatOllama](https://python.langchain.com/docs/integrations/chat/ollama/)
- [Summarize Text](https://python.langchain.com/docs/tutorials/summarization/)
