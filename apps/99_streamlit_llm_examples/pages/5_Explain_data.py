from os import getenv

import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
from pandas import DataFrame
from plotly.graph_objs import Figure

load_dotenv()


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
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_llm_examples/pages/5_Explain_data.py)"
    "[Streamlit > st.plotly_chart](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)"
    "[Plotly > Time Series and Date Axes in Python](https://plotly.com/python/time-series/)"

st.title("Explain data")

if not azure_openai_api_key or not azure_openai_endpoint or not azure_openai_api_version or not azure_openai_gpt_model:
    st.warning("サイドバーに Azure OpenAI の設定を入力してください")
    st.stop()

st.info("データを説明するサンプルです")


def get_dataset() -> DataFrame:
    return px.data.stocks()


def get_figure(df: DataFrame) -> Figure:
    fig = px.line(
        df,
        x="date",
        y=df.columns,
        hover_data={
            "date": "|%B %d, %Y",
        },
        title="2018 年の株価を基準とした株価の変化",
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
    )
    return fig


def analyze_data(df: DataFrame) -> str:
    return df.describe(include="all").__str__()


def explain_data(input: str) -> str:
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
    )

    response = client.chat.completions.create(
        model=azure_openai_gpt_model,
        messages=[
            {
                "role": "system",
                "content": f"""あなたはプロのデータ分析者です。与えられたデータについて説明します。
                ---
                {input}
                ---""",
            },
        ],
    )
    return response.choices[0].message.content


df = get_dataset()

fig = get_figure(df)

st.plotly_chart(
    figure_or_data=fig,
    theme="streamlit",
    use_container_width=True,
)

explain_button = st.button("説明")

if explain_button:
    with st.spinner("数値解析中..."):
        analyze_result = analyze_data(df)
    with st.spinner("LLM による解析中..."):
        explain_result = explain_data(input=analyze_result)
    # st.write(analyze_result)
    st.write(explain_result)
