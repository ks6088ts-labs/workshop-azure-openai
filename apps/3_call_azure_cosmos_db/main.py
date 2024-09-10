import argparse
import logging
import sys
from os import getenv
from pprint import pprint

from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cosmosdb",
        description="",
    )
    parser.add_argument("-i", "--item-id", default="test", help="Item ID")
    parser.add_argument("-p", "--partition-key-path", default="/id", help="Partition key")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-c", "--command", default="create", help="Command to execute: create, read, delete")
    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Parse .env file and get environment variables
    load_dotenv()

    item_id = args.item_id

    # Connect to Azure Cosmos DB
    try:
        client = CosmosClient.from_connection_string(getenv("AZURE_COSMOS_DB_CONNECTION_STRING"))
        database = client.create_database_if_not_exists(id=getenv("AZURE_COSMOS_DB_DATABASE_NAME"))
        partition_key_path = PartitionKey(
            path=args.partition_key_path,
            kind="Hash",
        )
        container = database.create_container_if_not_exists(
            id=getenv("AZURE_COSMOS_DB_CONTAINER_NAME"),
            partition_key=partition_key_path,
        )
    except Exception as e:
        print(f"Failed to connect to Azure Cosmos DB: {e}")
        sys.exit(1)

    if args.command == "create":
        # Create and read an item
        print("Create item")
        try:
            response = container.create_item(
                body={
                    "id": item_id,
                    "role": "assistant",
                    "content": "Hello, world!",
                }
            )
            pprint(response)
        except Exception as e:
            print(f"Failed to create item: {e}")
            sys.exit(1)
    elif args.command == "read":
        # Read an item
        print("Read item:")
        try:
            response = container.read_item(
                item=item_id,
                partition_key=item_id,
            )
            pprint(response)

        except Exception as e:
            print(f"Failed to read item: {e}")
            sys.exit(1)
    elif args.command == "delete":
        # Delete an item
        print("Delete item:")
        try:
            container.delete_item(
                item=item_id,
                partition_key=item_id,
            )
        except Exception as e:
            print(f"Failed to delete item: {e}")
            sys.exit(1)
    else:
        print(f"Invalid command {args.command}")
        sys.exit(1)
