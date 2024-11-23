# Setup

```shell
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install typer python-dotenv azure-cosmos langchain-openai langchain-community
# pip install -r requirements.txt

python vector_database.py --help
```

# References

- [Azure Cosmos DB No SQL](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db_no_sql/)
- [Learn Azure Azure Cosmos DB Vector database](https://learn.microsoft.com/azure/cosmos-db/vector-database)
- [AzureDataRetrievalAugmentedGenerationSamples/Python/CosmosDB-NoSQL_VectorSearch](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/Python/CosmosDB-NoSQL_VectorSearch)
- [Azure Cosmos DB ベクター検索機能と RAG の実装ガイド](https://note.com/generativeai_new/n/n3fcb2e57d195)
- [Azure CosmosDB for NoSQL でベクトル検索しよう！！](https://zenn.dev/nomhiro/articles/cosmos-nosql-vector-search)
