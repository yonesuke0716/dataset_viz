import streamlit as st
import pandas as pd
import os

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def select_experiment(key):
    exp_path = os.listdir("pages/experiment")
    exp_folder = st.selectbox(f"実験フォルダを選択({key})", exp_path, key=f"{key}_exp")
    csv_path = os.listdir(f"pages/experiment/{exp_folder}")
    csv_file = st.selectbox(f"実験結果を選択({key})", csv_path, key=f"{key}_csv")
    return pd.read_csv(f"pages/experiment/{exp_folder}/{csv_file}")


st.title("Prediction Page")

col1, col2 = st.columns(2)

# 変更前
with col1:
    df1 = select_experiment(key="before")

# 変更後
with col2:
    df2 = select_experiment(key="after")

# 正しくデータセットが指定されている
if (len(df1) > 0) & (len(df2) > 0):
    # かつ、表示したい意志をボタンで押下したら実行
    if st.button("変更前後を比較表示（散布図）"):
        # グラフを作成
        fig = go.Figure()

        # 予測値のプロット
        fig.add_trace(
            go.Scatter(
                x=df1["Sample"],
                y=df1["Predicted"],
                mode="markers",
                name="Predicted",
                marker=dict(color="blue", size=10, opacity=0.8),
            )
        )

        # 正解値のプロット
        fig.add_trace(
            go.Scatter(
                x=df2["Sample"],
                y=df2["Actual"],
                mode="markers",
                name="Actual",
                marker=dict(color="red", size=10, opacity=0.8),
            )
        )

        # グラフのレイアウトを設定
        fig.update_layout(
            title="Predicted vs. Actual Species", xaxis_title="Sample ID", yaxis_title="Species", showlegend=True
        )

        # プロットをStreamlitアプリケーションに表示
        st.plotly_chart(fig)
