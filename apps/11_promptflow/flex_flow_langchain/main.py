from dataclasses import dataclass

from langchain_openai import AzureChatOpenAI
from promptflow.client import PFClient
from promptflow.connections import CustomConnection
from promptflow.tracing import trace


@dataclass
class Result:
    answer: str


class LangChainRunner:
    def __init__(self, custom_connection: CustomConnection):
        # https://python.langchain.com/v0.2/docs/integrations/chat/azure_chat_openai/
        self.llm = AzureChatOpenAI(
            temperature=0,
            api_key=custom_connection.secrets["api_key"],
            api_version=custom_connection.configs["api_version"],
            azure_endpoint=custom_connection.configs["api_base"],
            model="gpt-4o",
        )

    @trace
    def __call__(
        self,
        question: str,
    ) -> Result:
        response = self.llm.invoke(
            [
                (
                    "system",
                    "You are asking me to do some math, I can help with that.",
                ),
                ("human", question),
            ],
        )
        return Result(answer=response.content)


if __name__ == "__main__":
    from promptflow.tracing import start_trace

    start_trace()
    pf = PFClient()
    connection = pf.connections.get(name="open_ai_connection")
    runner = LangChainRunner(custom_connection=connection)
    result = runner(
        question="What's 2+2?",
    )
    print(result)
