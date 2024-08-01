from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI

if __name__ == "__main__":
    # .env ファイルをパースして環境変数にセット
    load_dotenv()

    # Azure OpenAI API クライアントを初期化
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # Chat API を呼び出して、ユーザーの入力に対する応答を取得
    response = client.chat.completions.create(
        model=getenv("AZURE_OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "こんにちは"},
        ],
    )

    # 応答を出力
    print(response.choices[0].message.content)

    # レスポンスの JSON を出力
    print(response.model_dump_json(indent=2))
