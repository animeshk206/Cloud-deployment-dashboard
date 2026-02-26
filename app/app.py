from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
 
app = FastAPI()
 

 
# -------------------------
# Database Connection Helper
# -------------------------
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )
 
 
# -------------------------
# Create Table (Run Once)
# -------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id SERIAL PRIMARY KEY,
            service_name VARCHAR(100),
            environment VARCHAR(50),
            version VARCHAR(50),
            status VARCHAR(50)
        )
    """)
 
    conn.commit()
    cursor.close()
    conn.close()
 
 
init_db()
 
 
# -------------------------
# Pydantic Model
# -------------------------
class Deployment(BaseModel):
    service_name: str
    environment: str
    version: str
    status: str
 
@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy" ,"error": str(e)}


# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def root():
    return {"message": "CloudOps Dashboard with PostgreSQL"}
 
 
# -------------------------
# Insert Deployment
# -------------------------
@app.post("/deployments")
def create_deployment(deployment: Deployment):
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute(
        "INSERT INTO deployments (service_name, environment, version, status) VALUES (%s, %s, %s, %s)",
        (deployment.service_name, deployment.environment, deployment.version, deployment.status)
    )
 
    conn.commit()
    cursor.close()
    conn.close()
 
    return {"message": "Deployment stored successfully"}
 
 
# -------------------------
# Get All Deployments
# -------------------------
@app.get("/deployments")
def get_deployments():
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT service_name, environment, version, status FROM deployments")
    rows = cursor.fetchall()
 
    cursor.close()
    conn.close()
 
    return rows
 