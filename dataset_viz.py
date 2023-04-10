import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns


# データ読み込み
@st.cache_resource
def load_data():
    data = pd.read_csv("LooptackTests.csv")
    return data


# ヒストグラム描画
def draw_histogram(df, x_axis, y_axis, color=None, nbins=None):
    fig = px.histogram(df, x=x_axis, y=y_axis, color=color, nbins=nbins)
    st.plotly_chart(fig)


# 散布図描画
def draw_scatter(df, x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig)


# Streamlitアプリケーション
def main():
    st.title("データセット設計")
    # データセット読み込み
    # df = load_data()

    # seaborn(iris)
    df = sns.load_dataset("iris")

    st.markdown("### describe")
    st.write(df.describe())
    column_names = list(df.columns)

    # 列名の選択
    x_axis = st.sidebar.selectbox("X軸の列名を選択してください", column_names)
    y_axis = st.sidebar.selectbox("Y軸の列名を選択してください", column_names)
    color = st.sidebar.selectbox("色分けする列名を選択してください（任意）", ["None"] + column_names)
    nbins = st.sidebar.number_input(
        "ビンの数を指定してください", min_value=1, max_value=100, value=10
    )

    # ヒストグラムの描画
    st.markdown("## ヒストグラム")
    st.write(f"X軸: {x_axis}, Y軸: {y_axis}, 色分け: {color}, ビン数: {nbins}")
    draw_histogram(
        df, x_axis, y_axis, color=color if color != "None" else None, nbins=nbins
    )
    # 散布図の描画
    st.markdown("## 散布図")
    draw_scatter(df, x_axis, y_axis)


if __name__ == "__main__":
    main()
