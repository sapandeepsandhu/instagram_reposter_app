# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(title="Instagram Reposter API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Instagram Reposter API"}
