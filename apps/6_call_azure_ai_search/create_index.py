from os import getenv
from pprint import pprint

from datasets import load_texts
from dotenv import load_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

if __name__ == "__main__":
    """
    テキストを Azure OpenAI Service で埋め込み化し、Azure AI Search にインデックス化します。
    """
    load_dotenv()

    # ドキュメントを取得
    texts = load_texts(
        file_path="./apps/6_call_azure_ai_search/data/test.txt",
    )

    # テキストを分割
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

    # Azure AI Search でのインデックス化
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
