import datetime
import time
from os import getenv

import streamlit as st
from azure.cosmos import ContainerProxy, CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()


def get_container_client() -> ContainerProxy:
    client = CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING"))
    database = client.create_database_if_not_exists(id=getenv("AZURE_COSMOS_DB_DATABASE_NAME"))
    return database.create_container_if_not_exists(
        id=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
        partition_key=PartitionKey(
            path="/id",
            kind="Hash",
        ),
    )


container = get_container_client()

with st.sidebar:
    "[Go to Azure Portal to get an Azure OpenAI API key](https://portal.azure.com/)"
    "[Go to Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/4_streamlit_chat_history/main.py)"

st.title("Query chat history")

today = datetime.datetime.now().date()
result = st.slider(
    "期間を指定してください。",
    value=(today - datetime.timedelta(days=30), today + datetime.timedelta(days=1)),
    format="YYYY-MM-DD (ddd)",
)


def convert_to_epoch(d: datetime.date) -> int:
    return int(time.mktime(time.strptime(d.isoformat(), "%Y-%m-%d")))


run = st.button("チャット履歴を取得する")
if run:
    query = "SELECT * FROM c WHERE c._ts < @end_date AND c._ts > @start_date"
    parameters = [
        {
            "name": "@start_date",
            "value": convert_to_epoch(result[0]),
        },
        {
            "name": "@end_date",
            "value": convert_to_epoch(result[1]),
        },
    ]

    with st.spinner("チャット履歴を取得中です。しばらくお待ちください。"):
        items = container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        )

    for item in items:
        st.write(item)