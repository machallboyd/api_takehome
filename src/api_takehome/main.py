from fastapi import FastAPI

from api_takehome.app import etl, query_average_experiments_per_user, query_user_reports
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


@app.get("/report")
def report():
    latest_avg = query_average_experiments_per_user()
    json_reports = [
        {"name": name, "count": count, "fav_compound": fav_compound}
        for name, count, fav_compound in query_user_reports()
    ]
    return {"average_experiment_count": latest_avg, "user_reports": json_reports}, 200
