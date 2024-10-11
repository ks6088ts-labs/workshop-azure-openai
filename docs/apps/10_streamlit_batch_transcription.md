# 10. Call Batch Transcription API with Streamlit

This is a Streamlit app that calls Azure AI Speech Batch Transcription API.

## Prerequisites

- Python 3.10 or later
- Azure AI Speech Service subscription key

### Infrastructure setup

Follow the steps in [Assign a resource access role](https://learn.microsoft.com/azure/ai-services/speech-service/batch-transcription-audio-data?tabs=portal#assign-resource-access-role) to assign the Storage Blob Data Reader role to the managed identity of your Speech resource.

FIXME: automate this step

## Usage

1. Get Azure AI Speech Service subscription key
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
$ python -m streamlit run apps/10_streamlit_batch_transcription/main.py
```

### Example

![Streamlit](../images/10_streamlit_batch_transcription.main.png)

## References

- [What is batch transcription?](https://learn.microsoft.com/azure/ai-services/speech-service/batch-transcription)
