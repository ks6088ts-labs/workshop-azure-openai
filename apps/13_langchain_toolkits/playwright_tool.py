import asyncio
from os import getenv

import nest_asyncio
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import run_async
from langchain_openai import AzureChatOpenAI
from playwright.async_api import async_playwright

load_dotenv()


async def main():
    nest_asyncio.apply()

    playwright = async_playwright()

    browser = run_async(playwright.start())
    browser = run_async(browser.chromium.launch(headless=True))

    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    tools = toolkit.get_tools()

    llm = AzureChatOpenAI(
        temperature=0,
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    result = await agent_chain.arun("Yahoo リアルタイム検索のトレンド上位 3 件を教えて")
    print(result)


asyncio.run(main())
