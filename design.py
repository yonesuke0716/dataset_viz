import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold


# データ読み込み
@st.cache_resource
def load_data():
    data = pd.read_csv("sample.csv")
    return data


# 分割パラメータ設定
def hold_out(st, df):
    test_rate = st.number_input(
        "test_sizeを指定(0.0~1.0)", min_value=0.0, max_value=1.0, value=0.25
    )
    is_shuffle = st.checkbox("データをシャッフルするか？")
    if is_shuffle:
        seed_value = st.number_input(
            "seed値を指定(0~100)", min_value=0, max_value=100, value=10
        )
    else:
        seed_value = 0
    is_stf = st.checkbox("層化抽出するか？")
    if is_stf:
        # "species"(目的変数)は適宜調整すること
        target_stf = df["species"]
    else:
        target_stf = None

    # "species"(目的変数)は適宜調整すること
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

    return df_train, df_test


# 分割パラメータ設定
def kfold(st, df):
    n_splits = st.number_input("n_splitsを指定(2~10)", min_value=2, max_value=10, value=5)
    is_shuffle = st.checkbox("データをシャッフルするか？")
    if is_shuffle:
        seed_value = st.number_input(
            "seed値を指定(0~100)", min_value=0, max_value=100, value=10
        )
    else:
        seed_value = None

    kf = KFold(n_splits=n_splits, shuffle=is_shuffle, random_state=seed_value)
    df_train_list = []
    df_test_list = []
    for train_index, test_index in kf.split(df):
        df_train = df.iloc[train_index]
        df_test = df.iloc[test_index]
        df_train_list.append(df_train)
        df_test_list.append(df_test)

    n_fold = st.selectbox("何番目の分割データを見るか？", range(len(df_train_list)))

    return df_train_list[n_fold], df_test_list[n_fold]
