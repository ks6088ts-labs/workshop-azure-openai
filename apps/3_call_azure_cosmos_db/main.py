import sys
from os import getenv
from pprint import pprint

from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

if __name__ == "__main__":
    # .env ファイルをパースして環境変数にセット
    load_dotenv()

    # コマンドライン引数から item_id を取得
    if len(sys.argv) < 2:
        print("Usage: python main.py <item_id>")
        sys.exit(1)
    item_id = sys.argv[1]

    # Azure Cosmos DB に接続
    try:
        client = CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING"))
        database = client.create_database_if_not_exists(id=getenv("AZURE_COSMOS_DB_DATABASE_NAME"))
        partition_key_path = PartitionKey(
            path="/id",
            kind="Hash",
        )
        container = database.create_container_if_not_exists(
            id=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
            partition_key=partition_key_path,
        )
    except Exception as e:
        print(f"Failed to connect to Azure Cosmos DB: {e}")
        sys.exit(1)

    # Item を操作
    try:
        response = container.create_item(
            body={
                "id": item_id,
                "role": "assistant",
                "content": "こんにちは、何かお手伝いできますか？",
            }
        )
        print("Created item:")
        pprint(response)
        response = container.read_item(
            item=item_id,
            partition_key=item_id,
        )
        print("Read item:")
        pprint(response)

    except Exception as e:
        print(f"Failed to create item: {e}")
        sys.exit(1)
