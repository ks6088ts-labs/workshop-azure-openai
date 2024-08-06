# Streamlit のチャットアプリに RAG 機能を追加する

[4_streamlit_chat_history](../4_streamlit_chat_history/) で作成した履歴保存機能付きチャットアプリに、RAG (Retrieval Augmented Generation) 機能を追加します。

## 前提条件

- Python 3.11+ がインストールされていること
- Azure OpenAI Service が利用できること
- Azure OpenAI Service の API キーが取得できていること
- Azure Cosmos DB のアカウントが作成されていること
- Azure Cosmos DB の接続文字列が取得できていること
- Azure AI Search が利用できること
- Azure AI Search の API キーが取得できていること

## 手順

1. Azure OpenAI Service の API キーを取得する
1. Azure Cosmos DB の接続文字列を取得する
1. Azure AI Search の API キーを取得する
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
streamlit run ./apps/7_streamlit_chat_history_rag/main.py
```

### 実行例

http://localhost:8501 にアクセスすると、以下のような画面が表示されます。

![Streamlit Chat](../../docs/images/7_streamlit_chat_history_rag.png)
