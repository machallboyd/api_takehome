from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/csv")
def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    return {"message": "ETL process started"}, 200

