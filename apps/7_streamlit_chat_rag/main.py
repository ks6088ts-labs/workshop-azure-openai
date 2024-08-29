from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import AzureChatOpenAI
from streamlit.runtime.scriptrunner import get_script_run_ctx
from tools.fetch_contents import fetch_contents

CUSTOM_SYSTEM_PROMPT = """
You are the general affairs department of Contoso Corporation.
Please respond to inquiries from within the company with sincerity and accuracy.
Please note that we will only answer general questions about the internal rules of Contoso Corporation.
Please refrain from asking questions about other topics.
When answering questions about "Contoso Corporation", be sure to use the tool to find the answer.
Please answer in the language the user used to ask the question.
For example, if the user asks a question in English, be sure to answer in English.
If you are unsure about the answer, please ask the user for more information.
By doing so, you can understand the user's intentions and provide appropriate answers.
For example, if a user asks, "Where is the office located?" please ask the user for their prefecture first.
In most cases, users do not want to know the location of offices across Japan.
They want to know the location of offices in their own prefecture.
Therefore, please do not search for offices across Japan and answer until you truly understand the user's intentions.
Please note that this is just an example.
Please understand the user's intentions and provide appropriate answers in other cases as well.
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
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/7_streamlit_chat_rag/main.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")


def get_session_id():
    return get_script_run_ctx().session_id


def init_page():
    st.title("7_streamlit_chat_rag")
    st.write(f"Session ID: {get_session_id()}")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome to our chat service. How can I help you today?",
            }
        ]
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
    tools = [
        fetch_contents,
        # Add more tools here
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

    if prompt := st.chat_input(placeholder="Type your message here...", disabled=not is_configured()):
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response = customer_support_agent.invoke(
                {
                    "input": prompt,
                },
                config=RunnableConfig(
                    {
                        "callbacks": [
                            st_cb,
                        ],
                    },
                ),
            )
            st.write(response["output"])


if __name__ == "__main__":
    load_dotenv()

    main()
