import base64
import io

from openai import AzureOpenAI
from promptflow.connections import AzureOpenAIConnection
from promptflow.contracts.multimedia import Image
from promptflow.core import tool


@tool
def my_python_tool(
    connection: AzureOpenAIConnection,
    image: Image,
    model: str,
    system_prompt: str,
    user_prompt: str,
) -> str:
    image_stream = io.BytesIO(image)
    encoded_image = base64.b64encode(image_stream.read()).decode("utf-8")

    client = AzureOpenAI(
        api_key=connection.api_key,
        api_version=connection.api_version,
        azure_endpoint=connection.api_base,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
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
                        "text": user_prompt,
                    },
                ],
            },
        ],
    )
    return response.choices[0].message.content
