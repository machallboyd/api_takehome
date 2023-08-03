from collections import Counter, defaultdict
from collections.abc import Generator, Sequence
import csv
from datetime import datetime
import os
from pathlib import Path

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from api_takehome.db.experiment_summaries import (
    AverageExperimentsReport,
    Compound,
    engine,
    ExperimentSummary,
    User,
)

data_path = Path(__file__).parent.joinpath("data")

def csv_cleaner(reader: csv.reader) -> Generator[list[str]]:
    """
    Quick hack to screen out blank lines or header info

    If the first cell isn't an integer, skip it.
    A more robust approach might be to write a temp file.
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
    with os.scandir(data_path) as csv_files:
        for csv_file in csv_files:
            with open(csv_file.path) as f:
                yield csv_file.name.split(".csv")[0], list(csv_cleaner(csv.reader(f)))


def load_users(data: list[list[str]]):
    """
    Insert found users into the database
    """
    column_mappings = ["id", "name", "email", "signup_date"]
    user_dicts = [dict(zip(column_mappings, row)) for row in data]
    for user_dict in user_dicts:
        user_dict["signup_date"] = datetime.strptime(
            user_dict["signup_date"], "%Y-%m-%d"
        ).date()
    with Session(engine) as session, session.begin():
        session.execute(insert(User), user_dicts)


def load_compounds(data: list[list[str]]):
    """
    Insert found components into the database
    """
    column_mappings = ["id", "compound_name", "compound_structure"]
    user_dicts = [
        {key: value for key, value in zip(column_mappings, row)} for row in data
    ]
    with Session(engine) as session, session.begin():
        session.execute(insert(Compound), user_dicts)


def load_avg_experiments(data: list[list[str]]):
    """
    Calculate and load into the database the average number of experiments per user for this data set
    """
    counts_by_id = Counter(row[1] for row in data)
    dataset_average = counts_by_id.total() / len(counts_by_id.keys())
    with Session(engine) as session, session.begin():
        session.execute(insert(AverageExperimentsReport).values(avg=dataset_average))


def load_report(alldata: dict[str, list[list[str]]]):
    """
    Generates a per-user report for total experiments and records it to the database
    """
    exp_counts_by_user_id = Counter(row[1] for row in alldata["user_experiments"])
    compounds_by_user_id = defaultdict(list)
    for row in alldata["user_experiments"]:
        compounds_by_user_id[row[1]].extend(int(i) for i in row[2].split(";"))
    fav_by_user_id = {
        user_id: Counter(compounds).most_common(1)[0][0]
        for user_id, compounds in compounds_by_user_id.items()
    }
    reports = [
        {
            "user_id": user_id,
            "fav_compound_id": fav_by_user_id[user_id],
            "total": exp_counts_by_user_id[user_id],
        }
        for user_id in compounds_by_user_id.keys()
    ]
    with Session(engine) as session, session.begin():
        session.execute(insert(ExperimentSummary), reports)


def query_average_experiments_per_user() -> int:
    """
    Query for the average number of experiments users ran.
    """
    with Session(engine) as session, session.begin():
        latest_avg = session.scalar(
            select(AverageExperimentsReport.avg).order_by(
                AverageExperimentsReport.timestamp.desc()
            )
        )
    return latest_avg


def query_user_reports() -> Sequence:
    """
    Query for the per-user summary of activity.

    User name, total experiments run, most used compound
    """
    with Session(engine) as session, session.begin():
        return session.execute(
            select(User.name, ExperimentSummary.total, Compound.compound_name)
            .join(ExperimentSummary.user)
            .join(ExperimentSummary.fav_compound)
        ).all()


def etl():
    """
    Main process for extract, transform and load on local csv files
    """
    csv_data = dict(transform_csvs())
    load_users(csv_data["users"])
    load_compounds(csv_data["compounds"])
    load_avg_experiments(csv_data["user_experiments"])
    load_report(csv_data)
