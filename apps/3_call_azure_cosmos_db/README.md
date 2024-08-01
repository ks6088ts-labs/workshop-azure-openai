# Azure Cosmos DB にデータを書き込む

Azure Cosmos DB にデータを書き込むサンプルです。

## 前提条件

- Python 3.11+ がインストールされていること
- Azure Cosmos DB のアカウントが作成されていること
- Azure Cosmos DB の接続文字列が取得できていること

## 手順

1. Azure Cosmos DB のアカウントを作成する
1. Azure Cosmos DB の接続文字列を取得する
1. [.env.template](../../.env.template) をコピーして `.env` ファイルを作成する
1. `.env` ファイルに API キーを設定する
1. [main.py](./main.py) を実行する

```shell
# 仮想環境を作成してライブラリをインストールする
python -m venv .venv

# 仮想環境を有効化する
source .venv/bin/activate

# ライブラリをインストールする
pip install -r requirements.txt

# スクリプトを実行する
python apps/3_call_azure_cosmos_db/main.py ThisIsAnId
```

### 実行例

```shell
❯ python apps/3_call_azure_cosmos_db/main.py ThisIsAnId
Created item:
{'_attachments': 'attachments/',
 '_etag': '"070049c1-0000-2300-0000-66ab2af90000"',
 '_rid': 'NrlbAPNy-A4GAAAAAAAAAA==',
 '_self': 'dbs/NrlbAA==/colls/NrlbAPNy-A4=/docs/NrlbAPNy-A4GAAAAAAAAAA==/',
 '_ts': 1722493689,
 'content': 'こんにちは、何かお手伝いできますか？',
 'id': 'ThisIsAnId',
 'role': 'assistant'}
Read item:
{'_attachments': 'attachments/',
 '_etag': '"070049c1-0000-2300-0000-66ab2af90000"',
 '_rid': 'NrlbAPNy-A4GAAAAAAAAAA==',
 '_self': 'dbs/NrlbAA==/colls/NrlbAPNy-A4=/docs/NrlbAPNy-A4GAAAAAAAAAA==/',
 '_ts': 1722493689,
 'content': 'こんにちは、何かお手伝いできますか？',
 'id': 'ThisIsAnId',
 'role': 'assistant'}
```

## 参考資料

- [Python を使用して Azure Cosmos DB for NoSQL の使用を開始する](https://learn.microsoft.com/ja-jp/azure/cosmos-db/nosql/how-to-python-get-started?tabs=env-virtual%2Cazure-cli%2Clinux)
- [Python 用の Azure Cosmos DB for NoSQL SDK の例](https://learn.microsoft.com/ja-jp/azure/cosmos-db/nosql/samples-python)
- [Azure Cosmos DB SQL API client library for Python Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/samples)
