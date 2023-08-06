# dataset_viz
MLOps+DataOpsな分析基盤の検討

## 実行方法：
【通常】

streamlit run 1_📊_ds_design.py

【Docker】

$ docker build -t ds_design .

(Mac/Linux)
$ docker run --rm -v $(pwd):/app -p 8501:8501 -it ds_design
(Windows)
$ docker run --rm -v %cd%:/app -p 8501:8501 -it ds_design
http://localhost:8501/
