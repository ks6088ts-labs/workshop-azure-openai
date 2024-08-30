from pathlib import Path

from dotenv import load_dotenv
from promptflow.core import Prompty
from promptflow.tracing import start_trace, trace

BASE_DIR = Path(__file__).absolute().parent


@trace
def chat(question: str) -> str:
    load_dotenv()
    prompty = Prompty.load(source=f"{BASE_DIR}/chat.prompty")
    return prompty(question=question)


if __name__ == "__main__":
    start_trace()

    result = chat("What's the capital of France?")
    print(result)
