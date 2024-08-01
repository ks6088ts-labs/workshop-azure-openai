# Azure OpenAI Service を Python から呼び出す

Azure OpenAI Service を Python から呼び出す方法を説明します。

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
python apps/1_call_azure_openai/main.py
```

### 実行例

```shell
❯ python apps/1_call_azure_openai_chat/main.py
こんにちは！どうされましたか？何かお手伝いできることがあれば教えてください。
{
  "id": "chatcmpl-9rHSFKIBtJDOlDheesev79CO7RNMz",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "こんにちは！どうされましたか？何かお手伝いできることがあれば教えてください。",
        "role": "assistant",
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1722485507,
  "model": "gpt-4o-2024-05-13",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_abc28019ad",
  "usage": {
    "completion_tokens": 23,
    "prompt_tokens": 18,
    "total_tokens": 41
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

## 参考資料

- [クイックスタート: Azure OpenAI Service で GPT-35-Turbo と GPT-4 を使い始める](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python)
