from fastapi import FastAPI

from api_takehome.app import etl
from api_takehome.db.experiment_summaries import create_test_db

app = FastAPI()


@app.get("/csv")
def trigger_etl():
    etl()
    return {"message": "ETL process started"}, 200


@app.get("/setup_test_db")
def setup_test_db():
    create_test_db()
    return {"message": "Triggering test db setup"}, 200
