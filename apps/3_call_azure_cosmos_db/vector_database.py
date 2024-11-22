import logging
from os import getenv

import typer
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores.azure_cosmos_db_no_sql import AzureCosmosDBNoSqlVectorSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
logger = logging.getLogger(__name__)
app = typer.Typer()


# https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db_no_sql/
@app.command()
def insert_data(
    pdf_url: str = "https://arxiv.org/pdf/2303.08774.pdf",
    chunk_size: int = 2000,
    chunk_overlap: int = 0,
    verbose: bool = True,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Load the PDF
    loader = PyMuPDFLoader(file_path=pdf_url)
    data = loader.load()

    # Split the text into chunks
    docs = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    ).split_documents(data)

    try:
        # Insert the data into Azure Cosmos DB
        database_name = getenv("AZURE_COSMOS_DB_DATABASE_NAME")
        AzureCosmosDBNoSqlVectorSearch.from_documents(
            documents=docs,
            embedding=AzureOpenAIEmbeddings(
                api_key=getenv("AZURE_OPENAI_API_KEY"),
                api_version=getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
                model=getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
            ),
            cosmos_client=CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING")),
            database_name=database_name,
            container_name=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
            vector_embedding_policy={
                "vectorEmbeddings": [
                    {
                        "path": "/embedding",
                        "dataType": "float32",
                        "distanceFunction": "cosine",
                        "dimensions": 3072,  # for text-embedding-3-large
                    }
                ]
            },
            indexing_policy={
                "indexingMode": "consistent",
                "includedPaths": [{"path": "/*"}],
                "excludedPaths": [{"path": '/"_etag"/?'}],
                "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
            },
            cosmos_container_properties={"partition_key": PartitionKey(path="/id")},
            cosmos_database_properties={"id": database_name},  # need to add this
        )
    except Exception as e:
        logger.error(f"error: {e}")


@app.command()
def query_data(
    query: str = "What were the compute requirements for training GPT 4",
    verbose: bool = True,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    database_name = getenv("AZURE_COSMOS_DB_DATABASE_NAME")
    vector_search = AzureCosmosDBNoSqlVectorSearch(
        embedding=AzureOpenAIEmbeddings(
            api_key=getenv("AZURE_OPENAI_API_KEY"),
            api_version=getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
            model=getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
        ),
        cosmos_client=CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING")),
        database_name=database_name,
        container_name=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
        vector_embedding_policy={
            "vectorEmbeddings": [
                {
                    "path": "/embedding",
                    "dataType": "float32",
                    "distanceFunction": "cosine",
                    "dimensions": 3072,  # for text-embedding-3-large
                }
            ]
        },
        indexing_policy={
            "indexingMode": "consistent",
            "includedPaths": [{"path": "/*"}],
            "excludedPaths": [{"path": '/"_etag"/?'}],
            "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
        },
        cosmos_container_properties={"partition_key": PartitionKey(path="/id")},
        cosmos_database_properties={"id": database_name},
    )

    try:
        results = vector_search.similarity_search(query=query)
        for idx, result in enumerate(results):
            print(f"Result {idx + 1}: {result}")
    except Exception as e:
        logger.error(f"error: {e}")


if __name__ == "__main__":
    load_dotenv()
    app()
