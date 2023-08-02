from fastapi import FastAPI

from app import etl
from db.experiment_summaries import create_test_db

app = FastAPI()

@app.get("/csv")
def trigger_etl():
    etl()
    return {"message": "ETL process started"}, 200

@app.get("/setup_test_db")
def setup_test_db():
    create_test_db()
    return {"message": "Triggering test db setup"}, 200