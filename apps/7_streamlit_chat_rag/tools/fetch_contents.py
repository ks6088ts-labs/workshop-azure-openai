from os import getenv

from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import AzureOpenAIEmbeddings

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


class QueryInput(BaseModel):
    """This is a schema for the input arguments of the tool."""

    query: str = Field()
    k: int = Field(default=5)


@tool(args_schema=QueryInput)
def fetch_contents(query, k=5):
    """
    This tool fetches content from pre-registered documents that are related to the user's question.
    It helps to obtain specific knowledge such as internal rules related to "Contoso Corporation".

    This tool returns 'content'.
    - 'content' provides text related to the question.

    When an empty list is returned, it means that no related content was found.
    In that case, it is a good idea to ask the user to clarify the question.

    Returns
    -------
    List[Dict[str, Any]]:
    - page_content
      - content: str
    """
    docs = vector_store.hybrid_search(
        query=query,
        k=k,
    )
    return [
        {
            "content": doc.page_content,
        }
        for doc in docs
    ]
