# Azure AI Search を Python から呼び出す

Azure AI Search を Python から呼び出す方法を説明します。

## 前提条件

- Python 3.11+ がインストールされていること
- Azure AI Search が利用できること
- Azure AI Search の API キーが取得できていること

## 手順

1. Azure AI Search の API キーを取得する
1. [.env.template](../../.env.template) をコピーして `.env` ファイルを作成する
1. `.env` ファイルに API キーを設定する

```shell
# 仮想環境を作成してライブラリをインストールする
python -m venv .venv

# 仮想環境を有効化する
source .venv/bin/activate

# ライブラリをインストールする
pip install -r requirements.txt
```

### 実行例

```shell
# Azure AI Search にインデックスを作成して、ドキュメントを追加する
python apps/6_call_azure_ai_search/create_index.py

# Azure AI Search にクエリを発行して、検索結果を取得する
python apps/6_call_azure_ai_search/search_index.py
```

## 参考資料

- [How to recursively split text by characters](https://python.langchain.com/v0.2/docs/how_to/recursive_text_splitter/)
- [青空文庫 > 吾輩は猫である](https://www.aozora.gr.jp/cards/000148/files/789_14547.html)
