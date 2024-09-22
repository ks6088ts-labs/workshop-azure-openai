from os import getenv

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI

load_dotenv()


react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled ->  multiplied by 3
    """
    return 3 * float(num)


tools = [
    BingSearchResults(
        api_wrapper=BingSearchAPIWrapper(
            bing_search_url=getenv("BING_SEARCH_URL"),
            bing_subscription_key=getenv("BING_SUBSCRIPTION_KEY"),
            k=1,
        ),
        num_results=1,
    ),
    triple,
]

llm = AzureChatOpenAI(
    temperature=0,
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    model=getenv("AZURE_OPENAI_GPT_MODEL"),
)

react_agent_runnable = create_react_agent(llm, tools, react_prompt)

if __name__ == "__main__":
    # https://python.langchain.com/docs/integrations/tools/bing_search/
    result = BingSearchAPIWrapper(
        k=1,
        bing_search_url=getenv("BING_SEARCH_URL"),
        bing_subscription_key=getenv("BING_SUBSCRIPTION_KEY"),
    ).run("python")
    print(result)
