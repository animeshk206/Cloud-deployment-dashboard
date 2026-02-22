from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cloudops tracker Running"}