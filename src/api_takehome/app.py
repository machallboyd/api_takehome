import csv
import os
from collections.abc import Generator
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

from db.experiment_summaries import engine, User, create_test_db, AverageExperimentsReport, ExperimentSummary, Compound
from sqlalchemy import insert, update
from sqlalchemy.orm import Session

def csv_cleaner(reader: csv.reader) -> Generator[list[str]]:
    """
    Quick hack to screen out blank lines or header info
    This also blocked an attempt at csv.DictReader which would have been great
    Messy data is life, though
    """
    for row in reader:
        try:
            int(row[0])

        except ValueError:
            continue
        except IndexError:
            continue
        yield [cell.strip() for cell in row]

def transform_csvs() -> Generator[tuple[str, list[list[str]]]]:
    """
    Produce lists of strings from csv files, as well as the name of the file it came from
    """
    with os.scandir(Path("./data")) as csv_files:
        for csv_file in csv_files:
            with open(csv_file.path) as f:
                yield csv_file.name.split('.csv')[0], list(csv_cleaner(csv.reader(f)))

def load_users(data: list[list[str]]):
    """
    Insert found users into the database
    """
    column_mappings = ['id', 'name', 'email', 'signup_date']
    user_dicts = [{key: value for key, value in zip(column_mappings, row)} for row in data]
    for user_dict in user_dicts:
        user_dict['signup_date'] = datetime.strptime(user_dict['signup_date'], '%Y-%d-%m').date()
    with Session(engine) as session:
        session.execute(
            insert(User), user_dicts
        )

def load_compounds(data: list[list[str]]):
    """
        Insert found components into the database
    """
    column_mappings = ["id", 'compound_name', 'compound_structure']
    user_dicts = [{key: value for key, value in zip(column_mappings, row)} for row in data]
    with Session(engine) as session:
        session.execute(
            insert(Compound), user_dicts
        )


def load_avg_experiments(data: list[list[str]]):
    """
    Calculate and load into the database the average number of experiments per user for this data set
    """
    counts_by_id = Counter(row[1] for row in data)
    dataset_average = counts_by_id.total() / len(counts_by_id.keys())
    with Session(engine) as session:
        session.execute(
            insert(AverageExperimentsReport).values(avg=dataset_average)
        )

def load_report(alldata: dict[str, list[list[str]]]):
    """
    Generates a per-user report for total experiments and records it to the database
    """
    exp_counts_by_user_id = Counter(row[1] for row in alldata['user_experiments'])
    compounds_by_user_id = defaultdict(list)
    for row in alldata['user_experiments']:
        compounds_by_user_id[row[1]].extend(int(i) for i in row[2].split(';'))
    fav_by_user_id = {user_id: Counter(compounds).most_common() for user_id, compounds in compounds_by_user_id.items()}
    reports = [{'user_id': user_id, 'fav_compound_id': fav_by_user_id[user_id], 'total': exp_counts_by_user_id[user_id]} for user_id in compounds_by_user_id.keys()]
    with Session(engine) as session:
        session.execute(insert(ExperimentSummary), reports)



def etl():
    csv_data = {filename: data for filename, data in transform_csvs()}
    load_users(csv_data['users'])
    load_compounds(csv_data['compounds'])
    load_avg_experiments(csv_data['user_experiments'])



create_test_db()
etl()