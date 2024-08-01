# Streamlit のチャットアプリに履歴機能を追加する

Cosmos DB を利用して、チャットの履歴を保存する機能を追加します。

## 前提条件

- Python 3.11+ がインストールされていること
- Azure OpenAI Service が利用できること
- Azure OpenAI Service の API キーが取得できていること
- Azure Cosmos DB のアカウントが作成されていること
- Azure Cosmos DB の接続文字列が取得できていること

## 手順

1. Azure OpenAI Service の API キーを取得する
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
streamlit run ./apps/4_streamlit_chat_history/main.py
```

### 実行例

http://localhost:8501 にアクセスすると、以下のような画面が表示されます。

![Streamlit Chat](../../docs/images/4_streamlit_chat_history.png)
