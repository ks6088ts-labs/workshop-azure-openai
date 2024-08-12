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


with st.sidebar:
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/4_streamlit_chat_history/main.py)"

st.title("5_streamlit_query_chat_history")

today = datetime.datetime.now().date()
result = st.slider(
    "Select a range.",
    value=(today - datetime.timedelta(days=30), today + datetime.timedelta(days=1)),
    format="YYYY-MM-DD (ddd)",
)


def convert_to_epoch(d: datetime.date) -> int:
    return int(time.mktime(time.strptime(d.isoformat(), "%Y-%m-%d")))


run = st.button("Retrieve chat history")
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

    with st.spinner("Retrieving chat history. Please wait."):
        items = get_container_client().query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        )

    for item in items:
        st.write(item)
