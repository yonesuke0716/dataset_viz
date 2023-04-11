import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

from draw import px_draw


def main():
    # ********* read dataset *********
    df = sns.load_dataset("iris")
    column_names = list(df.columns)

    # ********* sidebar *********
    st.sidebar.subheader("graph_config")
    x_axis = st.sidebar.selectbox("X軸の列名(hist, scatter共有)の選択", column_names)
    y_axis = st.sidebar.selectbox("Y軸の列名(scatterのみ)の選択", column_names)
    nbins = st.sidebar.number_input(
        "histのbin数の指定", min_value=1, max_value=100, value=10
    )

    # ********* contents *********
    st.title("Dataset Checker")
    # 全てのデータセットの可視化
    st.subheader("All data")
    st.markdown("##### describe")
    st.write(df.describe())

    px_draw(
        df,
        x_axis=x_axis,
        y_axis="count",
        st=st,
        graph_type="hist",
        color="species",
        nbins=nbins,
        width=700,
    )
    px_draw(
        df,
        x_axis,
        y_axis,
        st=st,
        graph_type="scatter",
        color="species",
        width=700,
    )

    # train/testの可視化
    st.subheader("Split data")
    test_rate = st.number_input(
        "test_sizeを指定(0.0~1.0)", min_value=0.0, max_value=1.0, value=0.25
    )
    seed_value = st.number_input(
        "seed値を指定(0~100)", min_value=0, max_value=100, value=10
    )
    is_shuffle = st.checkbox("データをシャッフルするか？")
    is_stf = st.checkbox("層化抽出するか？")
    if is_stf:
        target_stf = df["species"]
    else:
        target_stf = None

    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("species", axis=1),
        df["species"],
        test_size=test_rate,
        shuffle=is_shuffle,
        random_state=seed_value,
        stratify=target_stf,
    )
    df_train = pd.concat([X_train, y_train], axis=1)
    df_test = pd.concat([X_test, y_test], axis=1)
    col1, col2 = st.columns(2)

    col1.subheader("train")
    col1.write(df_train.describe())
    col2.subheader("test")
    col2.write(df_test.describe())

    # ヒストグラムの描画
    px_draw(
        df_train,
        x_axis=x_axis,
        y_axis="count",
        st=col1,
        graph_type="hist",
        color="species",
        nbins=nbins,
    )
    px_draw(
        df_test,
        x_axis=x_axis,
        y_axis="count",
        st=col2,
        graph_type="hist",
        color="species",
        nbins=nbins,
    )
    # 散布図の描画
    px_draw(df_train, x_axis, y_axis, st=col1, graph_type="scatter", color="species")
    px_draw(df_test, x_axis, y_axis, st=col2, graph_type="scatter", color="species")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
