# 3. Call Azure Cosmos DB from Python

This app demonstrates how to call Azure Cosmos DB from Python.

## Prerequisites

- Python 3.10 or later
- Azure Cosmos DB

## Usage

1. Create an Azure Cosmos DB account
1. Get the connection string for Azure Cosmos DB
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run [main.py](./main.py)

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the script
$ python apps/3_call_azure_cosmos_db/main.py Hello
```

### Example

```shell
$ python apps/3_call_azure_cosmos_db/main.py --command create
Create item
{'_attachments': 'attachments/',
 '_etag': '"0000ef9c-0000-2300-0000-66dfd5140000"',
 '_rid': 'ipcwAJFKMxICAAAAAAAAAA==',
 '_self': 'dbs/ipcwAA==/colls/ipcwAJFKMxI=/docs/ipcwAJFKMxICAAAAAAAAAA==/',
 '_ts': 1725945108,
 'content': 'Hello, world!',
 'id': 'test',
 'role': 'assistant'}

$ python apps/3_call_azure_cosmos_db/main.py --command read
Read item:
{'_attachments': 'attachments/',
 '_etag': '"0000ef9c-0000-2300-0000-66dfd5140000"',
 '_rid': 'ipcwAJFKMxICAAAAAAAAAA==',
 '_self': 'dbs/ipcwAA==/colls/ipcwAJFKMxI=/docs/ipcwAJFKMxICAAAAAAAAAA==/',
 '_ts': 1725945108,
 'content': 'Hello, world!',
 'id': 'test',
 'role': 'assistant'}

$ python apps/3_call_azure_cosmos_db/main.py --command delete
Delete item:

$ python apps/3_call_azure_cosmos_db/main.py --command read
Read item:
Failed to read item: (NotFound) Entity with the specified id does not exist in the system. More info: https://aka.ms/cosmosdb-tsg-not-found,
```

## References

- [Get started with Azure Cosmos DB for NoSQL using Python](https://learn.microsoft.com/azure/cosmos-db/nosql/how-to-python-get-started?tabs=env-virtual%2Cazure-cli%2Clinux)
- [Examples for Azure Cosmos DB for NoSQL SDK for Python](https://learn.microsoft.com/azure/cosmos-db/nosql/samples-python)
- [Azure Cosmos DB SQL API client library for Python Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/samples)
