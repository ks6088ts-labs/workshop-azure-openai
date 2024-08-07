import sys
from os import getenv
from pprint import pprint

from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

if __name__ == "__main__":
    # Parse .env file and get environment variables
    load_dotenv()

    # Get item_id from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <item_id>")
        sys.exit(1)
    item_id = sys.argv[1]

    # Connect to Azure Cosmos DB
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

    # Create and read an item
    try:
        response = container.create_item(
            body={
                "id": item_id,
                "role": "assistant",
                "content": "Hello, world!",
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
