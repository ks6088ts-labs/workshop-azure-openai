# GitHub: https://github.com/naotaka1128/llm_app_codes/chapter_010/main.py

from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

# models
from langchain_openai import AzureChatOpenAI
from streamlit.runtime.scriptrunner import get_script_run_ctx
from tools.fetch_contents import fetch_contents

CUSTOM_SYSTEM_PROMPT = """
あなたは上鳥羽製作所の総務係です。
社内からのお問い合わせに対して、誠実かつ正確な回答を心がけてください。

上鳥羽製作所の社内規則に関する一般的な知識についてのみ答えます。
それ以外のトピックに関する質問には、丁重にお断りしてください。

回答の正確性を保証するため「上鳥羽製作所」に関する質問を受けた際は、
必ずツールを使用して回答を見つけてください。

ユーザーが質問に使用した言語で回答してください。
例えば、ユーザーが英語で質問された場合は、必ず英語で回答してください。
スペイン語ならスペイン語で回答してください。

回答する際、不明な点がある場合は、ユーザーに確認しましょう。
それにより、ユーザーの意図を把握して、適切な回答を行えます。

例えば、ユーザーが「オフィスはどこにありますか？」と質問した場合、
まずユーザーの居住都道府県を尋ねてください。

日本全国のオフィスの場所を知りたいユーザーはほとんどいません。
自分の都道府県内のオフィスの場所を知りたいのです。
したがって、日本全国のオフィスを検索して回答するのではなく、
ユーザーの意図を本当に理解するまで回答しないでください。

あくまでこれは一例です。
その他のケースでもユーザーの意図を理解し、適切な回答を行ってください。
"""

with st.sidebar:
    azure_openai_endpoint = st.text_input(
        label="AZURE_OPENAI_ENDPOINT",
        value=getenv("AZURE_OPENAI_ENDPOINT"),
        key="AZURE_OPENAI_ENDPOINT",
        type="default",
    )
    azure_openai_api_key = st.text_input(
        label="AZURE_OPENAI_API_KEY",
        key="AZURE_OPENAI_API_KEY",
        type="password",
    )
    azure_openai_api_version = st.text_input(
        label="AZURE_OPENAI_API_VERSION",
        value=getenv("AZURE_OPENAI_API_VERSION"),
        key="AZURE_OPENAI_API_VERSION",
        type="default",
    )
    azure_openai_gpt_model = st.text_input(
        label="AZURE_OPENAI_GPT_MODEL",
        value=getenv("AZURE_OPENAI_GPT_MODEL"),
        key="AZURE_OPENAI_GPT_MODEL",
        type="default",
    )
    "[Go to Azure Portal to get an Azure OpenAI API key](https://portal.azure.com/)"
    "[Go to Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/4_streamlit_chat_history/main.py)"

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("サイドバーに Azure OpenAI の設定を入力してください")
    st.stop()


def get_session_id():
    return get_script_run_ctx().session_id


def init_page():
    st.title("Streamlit Chat")
    st.write(f"Session ID: {get_session_id()}")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        welcome_message = "ベアーモバイル カスタマーサポートへようこそ。ご質問をどうぞ🐻"
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]
        st.session_state["memory"] = ConversationBufferWindowMemory(
            return_messages=True, memory_key="chat_history", k=10
        )


def select_model():
    return AzureChatOpenAI(
        temperature=0,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
        model=azure_openai_gpt_model,
    )


def create_agent():
    ## https://learn.deeplearning.ai/functions-tools-agents-langchain/lesson/7/conversational-agent
    tools = [
        fetch_contents,
    ]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CUSTOM_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm = select_model()
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, memory=st.session_state["memory"])


def main():
    init_page()
    init_messages()
    customer_support_agent = create_agent()

    for msg in st.session_state["memory"].chat_memory.messages:
        st.chat_message(msg.type).write(msg.content)

    if prompt := st.chat_input(placeholder="法人で契約することはできるの？"):
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response = customer_support_agent.invoke({"input": prompt}, config=RunnableConfig({"callbacks": [st_cb]}))
            st.write(response["output"])


if __name__ == "__main__":
    load_dotenv()

    main()
