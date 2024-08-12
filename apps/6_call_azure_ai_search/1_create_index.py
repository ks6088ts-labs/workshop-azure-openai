from os import getenv
from pprint import pprint

from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_texts() -> list:
    # for simplicity, hardcoding the path to the text file
    with open("./datasets/contoso_rules.csv") as f:
        return f.readlines()


if __name__ == "__main__":
    """
    This script demonstrates how to:
        - Embed text with Azure OpenAI Service
        - Index text with Azure AI Search
    """
    load_dotenv()

    # Get documents
    texts = load_texts()

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
        index_name=getenv("AZURE_AI_SEARCH_INDEX_NAME"),
        embedding_function=embeddings.embed_query,
        additional_search_client_options={
            "retry_total": 4,
        },
    )

    # add documents
    docs_ids = search.add_documents(documents=documents)
    pprint(docs_ids)
