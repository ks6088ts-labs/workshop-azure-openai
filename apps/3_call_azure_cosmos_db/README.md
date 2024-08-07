# Call Azure Cosmos DB from Python

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
$ python apps/3_call_azure_cosmos_db/main.py Hello
Created item:
{'_attachments': 'attachments/',
 '_etag': '"8100471f-0000-2300-0000-66b32f2b0000"',
 '_rid': 'Ny9FAOMmTIMKAAAAAAAAAA==',
 '_self': 'dbs/Ny9FAA==/colls/Ny9FAOMmTIM=/docs/Ny9FAOMmTIMKAAAAAAAAAA==/',
 '_ts': 1723019051,
 'content': 'Hello, world!',
 'id': 'Hello',
 'role': 'assistant'}
Read item:
{'_attachments': 'attachments/',
 '_etag': '"8100471f-0000-2300-0000-66b32f2b0000"',
 '_rid': 'Ny9FAOMmTIMKAAAAAAAAAA==',
 '_self': 'dbs/Ny9FAA==/colls/Ny9FAOMmTIM=/docs/Ny9FAOMmTIMKAAAAAAAAAA==/',
 '_ts': 1723019051,
 'content': 'Hello, world!',
 'id': 'Hello',
 'role': 'assistant'}
```

## References

- [Get started with Azure Cosmos DB for NoSQL using Python](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-python-get-started?tabs=env-virtual%2Cazure-cli%2Clinux)
- [Examples for Azure Cosmos DB for NoSQL SDK for Python](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/samples-python)
- [Azure Cosmos DB SQL API client library for Python Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/samples)
