import streamlit as st
import seaborn as sns

from draw import px_draw
from design import hold_out, kfold


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
    st.subheader("All data")
    st.write(df)
    st.markdown("##### describe")
    st.write(df.describe())

    # Allのヒストグラム
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
    # Allの散布図
    px_draw(
        df,
        x_axis,
        y_axis,
        st=st,
        graph_type="scatter",
        color="species",
        width=700,
    )

    split_methods = [None, "hold_out", "KFold"]
    select_method = st.selectbox("train/test split?", split_methods)
    if select_method is None:
        pass
    else:
        st.subheader("Split data")
        if select_method == "hold_out":
            df_train, df_test = hold_out(st, df)
        elif select_method == "KFold":
            df_train, df_test = kfold(st, df)

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
        px_draw(
            df_train, x_axis, y_axis, st=col1, graph_type="scatter", color="species"
        )
        px_draw(df_test, x_axis, y_axis, st=col2, graph_type="scatter", color="species")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Dataset_Checker",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "Get Help": "https://www.extremelycoolapp.com/help",
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "# This is a header. This is an *extremely* cool app!",
        },
    )
    main()
