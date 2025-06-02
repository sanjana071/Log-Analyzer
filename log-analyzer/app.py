import streamlit as st
import requests
import pandas as pd
import sqlite3

st.title("📝 Log File Analyzer")

uploaded_file = st.file_uploader("Upload a .log file", type="log")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    res = requests.post("http://localhost:8000/upload-log/", files={"file": uploaded_file})
    st.success("Log file uploaded and processed!")

    st.subheader("Parsed Log Data")
    conn = sqlite3.connect('logs.db')
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()

    log_levels = st.multiselect("Filter by Log Level", df["level"].unique())
    if log_levels:
        df = df[df["level"].isin(log_levels)]

    st.dataframe(df)
    st.subheader("📊 Log Level Count")
    st.bar_chart(df["level"].value_counts())
