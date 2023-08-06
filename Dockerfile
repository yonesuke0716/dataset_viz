FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "1_📊_dataset.py", "--theme.base", "dark"]