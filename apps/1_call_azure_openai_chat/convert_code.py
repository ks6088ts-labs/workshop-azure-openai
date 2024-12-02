import argparse
import logging
from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="convert_code",
        description="Convert code to a structured format",
    )
    parser.add_argument("-s", "--system", default="Extract the event information.")
    parser.add_argument("-u", "--user", default="Alice and Bob are going to a science fair on Friday.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


class ResponseFormat(BaseModel):
    # FIXME: Update the ResponseFormat class to match your actual response format
    name: str
    date: str
    participants: list[str]


def print_structured_output(
    system: str,
    user: str,
):
    """
    How to use:
        Support for structured outputs was first added in API version 2024-08-01-preview.
        It is available in the latest preview APIs as well as the latest GA API: 2024-10-21.

    Install dependencies:
        $ pip install openai python-dotenv pydantic

    References:
        - https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/structured-outputs?tabs=python
    """

    client = AzureOpenAI(
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
    )

    completion = client.beta.chat.completions.parse(
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format=ResponseFormat,
    )

    print(completion.choices[0].message.parsed)
    print(completion.model_dump_json(indent=2))


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and set environment variables
    load_dotenv()

    try:
        print_structured_output(
            system=args.system,
            user=args.user,
        )
    except Exception as e:
        logging.error(e)
