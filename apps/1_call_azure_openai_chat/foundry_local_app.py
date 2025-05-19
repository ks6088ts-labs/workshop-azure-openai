import argparse
import logging

from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="foundry_local_app",
        description="Translate English to Japanese using Foundry Local.",
    )
    parser.add_argument("-i", "--input", default="I love to code.")
    parser.add_argument("-a", "--alias", default="phi-3-mini-4k")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def main(
    alias: str,
    input: str,
) -> None:
    manager = FoundryLocalManager(alias)

    llm = ChatOpenAI(
        model=manager.get_model_info(alias).id,
        base_url=manager.endpoint,
        api_key=manager.api_key,
        temperature=0.0,
        streaming=False,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    try:
        ai_msg = chain.invoke(
            {
                "input_language": "English",
                "output_language": "Japanese",
                "input": input,
            },
        )
        logger.debug(f"AI message: {ai_msg}")
        print(f"Response: {ai_msg.content}")
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    """
    # Usage
        $ uv run python apps/1_call_azure_openai_chat/foundry_local_app.py --help
    # Example
        $ uv run python apps/1_call_azure_openai_chat/foundry_local_app.py --verbose
    # References
        - Get started with Foundry Local: https://learn.microsoft.com/azure/ai-foundry/foundry-local/get-started
        - Build a translation application with LangChain: https://learn.microsoft.com/azure/ai-foundry/foundry-local/how-to/how-to-use-langchain-with-foundry-local?pivots=programming-language-python
    """
    args = init_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    main(
        alias=args.alias,
        input=args.input,
    )
