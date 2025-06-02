from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import re
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect('logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, level TEXT, message TEXT)''')
conn.commit()

log_pattern = r"\[(.*?)\]\s+\[(.*?)\]\s+(.*)"

@app.post("/upload-log/")
async def upload_log(file: UploadFile):
    content = await file.read()
    text = content.decode("utf-8")
    lines = text.split("\n")
    parsed = []

    for line in lines:
        match = re.match(log_pattern, line)
        if match:
            timestamp, level, message = match.groups()
            parsed.append((timestamp, level, message))
            c.execute("INSERT INTO logs VALUES (?, ?, ?)", (timestamp, level, message))
    conn.commit()
    return {"status": "success", "count": len(parsed)}
