from os import getenv

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

embedding = AzureOpenAIEmbeddings(
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    model=getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
)

COLLECTION_NAME = "rag-chroma"
PERSIST_DIRECTORY = "./.chroma"


retriever = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embedding,
).as_retriever()

if __name__ == "__main__":
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250,
        chunk_overlap=0,
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Create vector store
    # import logging

    # logging.basicConfig(level=logging.DEBUG)
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name=COLLECTION_NAME,
        embedding=embedding,
        persist_directory=PERSIST_DIRECTORY,
    )

    # retrieve documents
    docs = retriever.invoke("What is LLM Powered autonomous agent?")
    print(f"got {len(docs)} documents")
