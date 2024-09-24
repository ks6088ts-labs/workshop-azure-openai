from typing import Any

from ingestion import retriever

from graph.state import GraphState


def retrieve(state: GraphState) -> dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
