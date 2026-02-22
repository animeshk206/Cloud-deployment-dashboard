from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cloudops tracker Running"}

deployments = []
 
class Deployment(BaseModel):
    service_name: str
    environment: str
    version: str
    status: str
 
@app.post("/deploy")
def create_deployment(deployment: Deployment):
    deployments.append(deployment)
    return {"message": "Deployment recorded", "data": deployment}
 
@app.get("/deployments")
def get_deployments():
    return deployments
 