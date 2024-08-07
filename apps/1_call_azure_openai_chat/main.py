from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI

if __name__ == "__main__":
    # Parse .env file and set environment variables
    load_dotenv()

    # Initialize AzureOpenAI client
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # Call completion API and get a response to user input
    response = client.chat.completions.create(
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
        ],
    )

    # Print response to console
    print(response.model_dump_json(indent=2))
