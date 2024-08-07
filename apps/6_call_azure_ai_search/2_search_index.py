from os import getenv

from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

if __name__ == "__main__":
    """
    Search for documents in Azure AI Search
    """
    load_dotenv()

    embeddings = AzureOpenAIEmbeddings(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
    )

    vector_store = AzureSearch(
        azure_search_endpoint=getenv("AZURE_AI_SEARCH_ENDPOINT"),
        azure_search_key=getenv("AZURE_AI_SEARCH_API_KEY"),
        index_name=getenv("AZURE_AI_SEARCH_INDEX_NAME"),
        embedding_function=embeddings.embed_query,
        additional_search_client_options={
            "retry_total": 4,
        },
    )

    # search for documents
    results = vector_store.hybrid_search(
        query="meetings",
        k=3,
    )
    for result in results:
        print(result.page_content)
