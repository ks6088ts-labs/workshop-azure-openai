import argparse
import logging

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="slm_chat",
        description="Chat with SLM model",
    )
    parser.add_argument("-m", "--model", default="phi3")
    parser.add_argument("-s", "--system", default="You are a helpful assistant.")
    parser.add_argument("-p", "--prompt", default="What is the capital of France?")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and set environment variables
    load_dotenv()

    llm = ChatOllama(
        model=args.model,
        temperature=0,
    )

    ai_msg: AIMessage = llm.invoke(
        input=[
            ("system", args.system),
            ("human", args.prompt),
        ]
    )
    print(ai_msg.model_dump_json(indent=2))
    # print(ai_msg.content)
