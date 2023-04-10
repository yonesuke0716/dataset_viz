# dataset_viz
MLOps+DataOpsな分析基盤の検討

## 実行方法：
【通常】

streamlit run dataset_viz.py

【Docker】

$ docker build -t dataset_viz .

$ docker run --rm　-v $(pwd):/app -p 8501:8501 -it dataset_viz

http://localhost:8501/
