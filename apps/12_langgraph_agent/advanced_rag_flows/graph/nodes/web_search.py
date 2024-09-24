from os import getenv
from typing import Any

from langchain.schema import Document
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper

from graph.state import GraphState

web_search_tool = BingSearchResults(
    api_wrapper=BingSearchAPIWrapper(
        bing_search_url=getenv("BING_SEARCH_URL"),
        bing_subscription_key=getenv("BING_SUBSCRIPTION_KEY"),
        k=1,
    ),
    num_results=1,
)


def web_search(state: GraphState) -> dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]

    docs: str = web_search_tool.invoke({"query": question})
    docs = eval(docs)
    web_results = "\n".join([d["snippet"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}
