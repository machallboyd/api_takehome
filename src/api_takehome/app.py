import csv
import os
from collections.abc import Generator
from collections import Counter
from pathlib import Path
from datetime import datetime

from db.experiment_summaries import engine, User, create_test_db, AverageExperimentsReport
from sqlalchemy import insert
from sqlalchemy.orm import Session

def csv_cleaner(reader: csv.reader) -> Generator[list[str]]:
    for row in reader:
        try:
            int(row[0])
            #quick hack to screen out blank lines or header info
        except ValueError:
            continue
        except IndexError:
            continue
        yield [cell.strip() for cell in row]

def transform_csvs() -> Generator[tuple[str, list[list[str]]]]:
    with os.scandir(Path("./data")) as csv_files:
        for csv_file in csv_files:
            with open(csv_file.path) as f:
                yield csv_file.name.split('.csv')[0], list(csv_cleaner(csv.reader(f)))

def load_users(data: list[list[str]]):
    column_mappings = ['user_id', 'name', 'email', 'signup_date']
    user_dicts = [{key: value for key, value in zip(column_mappings, row)} for row in data]
    for user_dict in user_dicts:
        user_dict['signup_date'] = datetime.strptime(user_dict['signup_date'], '%Y-%d-%m').date()
    session = Session(engine)
    session.execute(
        insert(User), user_dicts
    )

def load_avg_experiments(data):
    counts_by_id = Counter(row[1] for row in data['user_experiments'])
    dataset_average = counts_by_id.total() / len(counts_by_id.keys())
    session = Session(engine)
    session.execute(
        insert(
            AverageExperimentsReport(
                avg = dataset_average
            )
        )
    )

def etl():
    raw_data = {filename: data for filename, data in transform_csvs()}
    load_users(raw_data['users'])
    load_avg_experiments(raw_data)


create_test_db()
etl()