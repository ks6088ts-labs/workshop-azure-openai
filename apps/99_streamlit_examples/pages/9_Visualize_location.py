import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


with st.sidebar:
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/workshop-azure-openai/blob/main/apps/99_streamlit_examples/pages/9_Visualize_location.py)"

st.title("Visualize location")
st.info("This is a sample to visualize location.")
uploaded_file = st.file_uploader("Upload an article", type=("csv"))

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Loaded data")
else:
    # Sample data
    df = pd.DataFrame(
        {
            "lat": [
                35.681236,
                35.689487,
            ],
            "lon": [
                139.767125,
                139.691706,
            ],
        }
    )
    st.write("Sample data")
st.write(df)
st.map(
    data=df,
    size=1,
)
