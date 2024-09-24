from os import getenv

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    temperature=0,
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    model=getenv("AZURE_OPENAI_GPT_MODEL"),
)
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
