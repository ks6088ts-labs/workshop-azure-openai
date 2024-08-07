# Search Chat History

This application is used to search the chat history accumulated in [4_streamlit_chat_history](../4_streamlit_chat_history/).

## Prerequisites

- Python 3.10 or later
- Azure Cosmos DB

## Usage

1. Get the connection string for Azure Cosmos DB
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
$ python -m streamlit run apps/5_streamlit_query_chat_history/main.py
```

### 実行例

Access `http://localhost:8501` and set the required fields in the sidebar to search the chat history.

When you click the "Search" button, the chat history will be displayed.

![Main page](../../docs/images/5_streamlit_query_chat_history.main.png)
