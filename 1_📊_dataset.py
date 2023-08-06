import os
import pandas as pd
import streamlit as st
import seaborn as sns

from draw import px_draw
from split import hold_out, kfold


def main():
    # ********* read dataset *********
    # datasetフォルダからcsvファイルを読み込む
    csv_files = os.listdir("dataset")
    csv_files = [csv_file for csv_file in csv_files if csv_file.endswith(".csv")]
    csv_file = st.multiselect("読み込むcsvファイルを選択", csv_files, csv_files[0])
    if len(csv_file) == 0:
        st.error("csvファイルがありません")
        return
    df = pd.DataFrame()
    for file in csv_file:
        df = pd.concat([df, pd.read_csv(f"dataset/{file}")])
    # indexを振り直す
    df = df.reset_index(drop=True)

    # snsのirisデータセットを読み込む
    # df = sns.load_dataset("iris")
    column_names = list(df.columns)
    # ********* augmentation *********
    st.subheader("Augmentation")
    st.write("データセットに前処理(かさ増し)を行う")

    # ********* sidebar *********
    st.sidebar.subheader("graph_config")
    x_axis = st.sidebar.selectbox("X軸の列名(hist, scatter共有)の選択", column_names)
    y_axis = st.sidebar.selectbox("Y軸の列名(scatterのみ)の選択", column_names)
    nbins = st.sidebar.number_input(
        "histのbin数の指定", min_value=1, max_value=100, value=10
    )

    # ********* contents *********
    st.subheader("All Dataset")
    st.write("読み込んだ全てのデータセットをデータフレームで表示")
    st.write(df)
    st.subheader("All Describe")
    st.write("読み込んだ全てのデータセットの統計量を表示")
    st.write(df.describe())

    # Allのヒストグラム
    st.subheader("All Histgram")
    st.write("読み込んだ全てのデータセットのヒストグラムを表示")
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
    st.subheader("All Scatter")
    st.write("読み込んだ全てのデータセットの散布図を表示")
    px_draw(
        df,
        x_axis,
        y_axis,
        st=st,
        graph_type="scatter",
        color="species",
        width=700,
    )
    # dataframeをcsvファイルで出力する
    st.subheader("Dataset to csv")
    csv_name = st.text_input("出力するcsvファイル名を入力してください", value="sample.csv")
    if st.button("Dataset to csv"):
        # フォルダを作成する
        os.makedirs("csv", exist_ok=True)
        df.to_csv(f"csv/{csv_name}", index=False)
        st.write(f"{csv_name}を出力しました")
    else:
        pass

    split_methods = [None, "hold_out", "KFold"]
    select_method = st.selectbox("train/test split?", split_methods)
    if select_method is None:
        pass
    else:
        st.subheader("Split data")
        st.write("train/test split用のパラメータを設定")
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
        page_icon="🧑‍💻",
        layout="wide",
    )
    st.title("Dataset Design Page")
    main()
