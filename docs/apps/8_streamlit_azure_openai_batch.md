# 8. Call Azure OpenAI Batch API with Streamlit

This app demonstrates how to call Azure OpenAI Batch API with Streamlit.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service ([Global batch deployment](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/batch?tabs=standard-input&pivots=programming-language-python))

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
$ python -m streamlit run apps/8_streamlit_azure_openai_batch/main.py
```

### Example

![Streamlit Chat](../images/8_streamlit_azure_openai_batch.main.png)

## References

- [Getting started with Azure OpenAI global batch deployments (preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/batch?tabs=standard-input&pivots=programming-language-python)
