# Realtime transcription with Azure AI Speech Service

This app demonstrates how to use Azure AI Speech Service for realtime transcription.

## Prerequisites

- Python 3.10 or later
- Azure AI Speech Service
- Azure OpenAI Service

## Overview

```shell
# Speech to Text script
poetry run python apps/14_streamlit_azure_ai_speech/speech_to_text.py --help

# WIP: Streamlit app
poetry run python -m streamlit run apps/14_streamlit_azure_ai_speech/main.py
```

# References

- [How to recognize speech](https://learn.microsoft.com/azure/ai-services/speech-service/how-to-recognize-speech?pivots=programming-language-python)
- [Quickstart: Create real-time diarization](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-stt-diarization?tabs=windows&pivots=programming-language-python)
- [Speech to text containers with Docker](https://learn.microsoft.com/azure/ai-services/speech-service/speech-container-stt?tabs=container&pivots=programming-language-python)
- [AzureSpeechService でリアルタイム議事録](https://zenn.dev/o_ken_surprise/articles/991f5b592b91ee)
