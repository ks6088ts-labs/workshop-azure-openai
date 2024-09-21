from os import getenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."  # noqa
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",  # noqa
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",  # noqa
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


llm = AzureChatOpenAI(
    temperature=0,
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    model=getenv("AZURE_OPENAI_GPT_MODEL"),
)

generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
