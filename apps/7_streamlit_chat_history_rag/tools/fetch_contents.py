# GitHub: https://github.com/naotaka1128/llm_app_codes/chapter_010/tools/fetch_qa_content.py

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
    """型を指定するためのクラス"""

    query: str = Field()
    k: int = Field(default=5)


@tool(args_schema=QueryInput)
def fetch_contents(query, k=5):
    """
    事前に登録されたドキュメントの中から、ユーザーの質問に関連するコンテンツを取得します。
    "上鳥羽製作所"に関する社内規則など具体的な知識を得るのに役立ちます。

    このツールは `content`（コンテンツ）を返します。
    - 'content'は、質問に関連したテキストを提供します。

    空のリストが返された場合、関連するコンテンツが見つからなかったことを意味します。
    その場合、ユーザーに質問内容を明確にしてもらうのが良いでしょう。

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
    return [{"content": doc.page_content} for doc in docs]
