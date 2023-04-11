import pandas as pd
import streamlit as st


# データ読み込み
@st.cache_resource
def load_data():
    data = pd.read_csv("sample.csv")
    return data
