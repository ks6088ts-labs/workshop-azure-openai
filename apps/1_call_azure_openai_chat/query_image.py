import argparse
import base64
import logging
from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="query_image",
        description="Query Azure OpenAI Chat with an image",
    )
    parser.add_argument("-f", "--file")
    parser.add_argument("-s", "--system", default="You are a professional image analyst. Describe the image.")
    parser.add_argument("-p", "--prompt", default="Please describe the content of the image")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and set environment variables
    load_dotenv()

    # Initialize AzureOpenAI client
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # Read image file and encode it to base64
    try:
        with open(args.file, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()
    except Exception as e:
        print(e)
        exit(1)

    # Call completion API and get a response to user input
    response = client.chat.completions.create(
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": args.system,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                    {
                        "type": "text",
                        "text": args.prompt,
                    },
                ],
            },
        ],
    )

    # Print response to console
    # print(response.model_dump_json(indent=2))
    print(response.choices[0].message.content)
