from os import getenv

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

if __name__ == "__main__":
    # Parse .env file and set environment variables
    load_dotenv(override=True)

    project = AIProjectClient.from_connection_string(
        conn_str=getenv("AZURE_AI_FOUNDRY_PROJECT_CONNECTION_STRING"),
        credential=DefaultAzureCredential(),
    )

    chat = project.inference.get_chat_completions_client()
    response = chat.complete(
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant",
            },
            {"role": "user", "content": "Hello, how are you?"},
        ],
    )

    print(response.choices[0].message.content)
