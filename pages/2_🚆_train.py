import os
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


st.title("Training Page")

# datasetフォルダからcsvファイルを読み込む
csv_files = os.listdir("dataset")
csv_files = [csv_file for csv_file in csv_files if csv_file.endswith(".csv")]
csv_file = st.multiselect("読み込むcsvファイルを選択", csv_files, csv_files[0])
if len(csv_file) == 0:
    st.error("csvファイルがありません")
df = pd.DataFrame()
for file in csv_file:
    df = pd.concat([df, pd.read_csv(f"dataset/{file}")])
# indexを振り直す
df = df.reset_index(drop=True)

# snsのirisデータセットを読み込む
# df = sns.load_dataset("iris")
column_names = list(df.columns)

Y = df["species"]
X = df.drop(["species"], axis=1)
target_names = ["species"]

st.write(X)
if st.button("訓練開始"):
    # データをトレーニングセットとテストセットに分割
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    # ランダムフォレストモデルを作成
    random_forest = RandomForestClassifier(n_estimators=100, random_state=42)

    # モデルをトレーニング
    random_forest.fit(X_train, y_train)

    # テストデータを使って予測
    y_pred = random_forest.predict(X_test)

    # 精度を評価
    accuracy = accuracy_score(y_test, y_pred)

    # Streamlitアプリケーションの作成
    st.title("Irisデータの分類")
    st.write("ランダムフォレストによるIrisデータの分類結果")

    # 精度を表示
    st.write(f"正解率 (Accuracy): {accuracy:.2f}")

    # 予測結果と正解値のDataFrameを作成
    results = pd.DataFrame({"Sample": range(len(y_test)), "Predicted": y_pred, "Actual": y_test})

    # 結果をCSVファイルとして出力
    results.to_csv("iris_classification_results.csv", index=False)
