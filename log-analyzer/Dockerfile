FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["sh", "-c", "uvicorn log_parser:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=8501"]
