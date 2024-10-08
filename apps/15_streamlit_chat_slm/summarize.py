import asyncio
import operator
from os import getenv
from typing import Annotated, Literal, TypedDict

from langchain.chains.combine_documents.reduce import acollapse_docs, split_list_of_docs
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

token_max = 1000
url = "https://lilianweng.github.io/posts/2023-06-23-agent/"

llm_ollama = ChatOllama(
    model="phi3",
    temperature=0,
)
llm_azure_openai = AzureChatOpenAI(
    temperature=0,
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    model=getenv("AZURE_OPENAI_GPT_MODEL"),
)
# Use the Ollama model
llm = llm_ollama


def length_function(documents: list[Document]) -> int:
    """Get number of tokens for input contents."""
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)


# This will be the overall state of the main graph.
# It will contain the input document contents, corresponding
# summaries, and a final summary.
class OverallState(TypedDict):
    # Notice here we use the operator.add
    # This is because we want combine all the summaries we generate
    # from individual nodes back into one list - this is essentially
    # the "reduce" part
    contents: list[str]
    summaries: Annotated[list, operator.add]
    collapsed_summaries: list[Document]
    final_summary: str


# This will be the state of the node that we will "map" all
# documents to in order to generate summaries
class SummaryState(TypedDict):
    content: str


map_prompt = ChatPromptTemplate.from_messages([("system", "Write a concise summary of the following:\\n\\n{context}")])

map_chain = map_prompt | llm | StrOutputParser()


# Here we generate a summary, given a document
async def generate_summary(state: SummaryState):
    response = await map_chain.ainvoke(state["content"])
    return {"summaries": [response]}


# Here we define the logic to map out over the documents
# We will use this an edge in the graph
def map_summaries(state: OverallState):
    # We will return a list of `Send` objects
    # Each `Send` object consists of the name of a node in the graph
    # as well as the state to send to that node
    return [Send("generate_summary", {"content": content}) for content in state["contents"]]


def collect_summaries(state: OverallState):
    return {"collapsed_summaries": [Document(summary) for summary in state["summaries"]]}


# Also available via the hub: `hub.pull("rlm/reduce-prompt")`
reduce_template = """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary
of the main themes.
"""

reduce_prompt = ChatPromptTemplate([("human", reduce_template)])

reduce_chain = reduce_prompt | llm | StrOutputParser()


# Add node to collapse summaries
async def collapse_summaries(state: OverallState):
    doc_lists = split_list_of_docs(state["collapsed_summaries"], length_function, token_max)
    results = []
    for doc_list in doc_lists:
        results.append(await acollapse_docs(doc_list, reduce_chain.ainvoke))

    return {"collapsed_summaries": results}


# This represents a conditional edge in the graph that determines
# if we should collapse the summaries or not
def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = length_function(state["collapsed_summaries"])
    if num_tokens > token_max:
        return "collapse_summaries"
    else:
        return "generate_final_summary"


# Here we will generate the final summary
async def generate_final_summary(state: OverallState):
    response = await reduce_chain.ainvoke(state["collapsed_summaries"])
    return {"final_summary": response}


async def main():
    # Construct the graph
    # Nodes:
    graph = StateGraph(OverallState)
    graph.add_node("generate_summary", generate_summary)  # same as before
    graph.add_node("collect_summaries", collect_summaries)
    graph.add_node("collapse_summaries", collapse_summaries)
    graph.add_node("generate_final_summary", generate_final_summary)

    # Edges:
    graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
    graph.add_edge("generate_summary", "collect_summaries")
    graph.add_conditional_edges("collect_summaries", should_collapse)
    graph.add_conditional_edges("collapse_summaries", should_collapse)
    graph.add_edge("generate_final_summary", END)

    app = graph.compile()

    # create graph image
    app.get_graph().draw_mermaid_png(output_file_path="docs/images/15_streamlit_chat_slm.summarize_graph.png")

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)

    loader = WebBaseLoader(web_path=url)
    docs = loader.load()

    split_docs = text_splitter.split_documents(docs)
    print(f"Generated {len(split_docs)} documents.")

    async for step in app.astream(
        {"contents": [doc.page_content for doc in split_docs]},
        {"recursion_limit": 10},
    ):
        print(list(step.keys()))
        print(step)


asyncio.run(main())
