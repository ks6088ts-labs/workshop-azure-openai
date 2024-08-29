import argparse
import logging
from os import getenv
from pprint import pprint

from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="create_index",
        description="Create an index in Azure AI Search",
    )
    parser.add_argument("-f", "--file", default="./datasets/contoso_rules.csv")
    parser.add_argument("-i", "--index-name", default="contoso-rules")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    """
    This script demonstrates how to:
        - Embed text with Azure OpenAI Service
        - Index text with Azure AI Search
    """
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    load_dotenv()

    # Get documents
    try:
        with open(args.file) as f:
            texts = f.readlines()
    except Exception as e:
        print(e)
        exit(1)

    # Split text into chunks
    # https://python.langchain.com/v0.2/docs/how_to/recursive_text_splitter/
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    documents = text_splitter.create_documents(
        texts=texts,
    )
    pprint(documents)

    embeddings = AzureOpenAIEmbeddings(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
    )

    # Index documents
    # https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/
    # create index
    search = AzureSearch(
        azure_search_endpoint=getenv("AZURE_AI_SEARCH_ENDPOINT"),
        azure_search_key=getenv("AZURE_AI_SEARCH_API_KEY"),
        index_name=args.index_name,
        embedding_function=embeddings.embed_query,
        additional_search_client_options={
            "retry_total": 4,
        },
    )

    # add documents
    docs_ids = search.add_documents(documents=documents)
    pprint(docs_ids)
