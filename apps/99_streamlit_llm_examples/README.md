# Streamlit のサンプル実装集

このアプリには、Streamlit を利用したサンプル実装が含まれています。

## 前提条件

- Python 3.11+ がインストールされていること
- Azure OpenAI Service が利用できること
- Azure OpenAI Service の API キーが取得できていること

## 手順

1. Azure OpenAI Service の API キーを取得する
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
streamlit run ./apps/99_streamlit_llm_examples/main.py
```

### 実行例

http://localhost:8501 にアクセスして、サイドバーから実行したいサンプルを選択してください。

## 参考文献

- [🎈 Streamlit + LLM Examples App](https://github.com/streamlit/llm-examples)
