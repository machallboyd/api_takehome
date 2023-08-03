import csv
import io

import pytest

import api_takehome.app
from api_takehome.app import csv_cleaner, transform_csvs, load_users, load_report, load_compounds, load_avg_experiments
from api_takehome.db.experiment_summaries import test_engine, User, ExperimentSummary, Compound, create_test_db

from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime

user_csvs = [
    """

user_id,	name,	email,	signup_date
1,	Alice,	alice@example.com,	2023-01-01
2,	Bob,	bob@example.com,	2023-02-01
""",
    """
user_id,	name,	email,	signup_date
1,	Alice,	alice@example.com,	2023-01-01
2,	Bob,	bob@example.com,	2023-02-01
""",
    """
    
1,	Alice,	alice@example.com,	2023-01-01
2,	Bob,	bob@example.com,	2023-02-01
    """,
    """
1,	Alice,	alice@example.com,	2023-01-01
2,	Bob,	bob@example.com,	2023-02-01
    """,
]


@pytest.mark.parametrize("test_input", user_csvs)
def test_cleaner(test_input):
    clean_output = [
        ["1", "Alice", "alice@example.com", "2023-01-01"],
        ["2", "Bob", "bob@example.com", "2023-02-01"],
    ]
    with io.StringIO() as f:
        print(test_input)
        f.write(test_input)
        f.seek(0)
        assert clean_output == list(csv_cleaner(csv.reader(f)))


test_files = {
    "users": """
    
user_id,	name,	email,	signup_date
1,	Alice,	alice@example.com,	2023-01-01
2,	Bob,	bob@example.com,	2023-02-01
""",
    "user_experiments": """
experiment_id,	user_id,	experiment_compound_ids,	experiment_run_time
1,	1,	1;2,	10
2,	1,	2;3,	15
3,	2,	1;3,	20
""",
    "compounds": """
compound_id,	compound_name,	compound_structure
1,	Compound A,	C20H25N3O
2,	Compound B,	C21H30O2
3,	Compound C,	C8H11NO2
""",
}


@pytest.fixture
def test_dir(tmp_path):
    for key, content in test_files.items():
        newf = tmp_path / f"{key}.csv"
        newf.write_text(content)
    return tmp_path


@pytest.fixture
def patch_data_dir(test_dir, monkeypatch):
    monkeypatch.setattr(api_takehome.app, "data_path", test_dir)

transformed_csv_data = {
        "compounds": [
            ["1", "Compound A", "C20H25N3O"],
            ["2", "Compound B", "C21H30O2"],
            ["3", "Compound C", "C8H11NO2"],
        ],
        "user_experiments": [
            ["1", "1", "1;2", "10"],
            ["2", "1", "2;3", "15"],
            ["3", "2", "1;3", "20"],
        ],
        "users": [
            ["1", "Alice", "alice@example.com", "2023-01-01"],
            ["2", "Bob", "bob@example.com", "2023-02-01"],
        ],
    }

def test_transform_csvs(patch_data_dir):
    result = dict(transform_csvs())
    assert result == transformed_csv_data

@pytest.fixture
def setup_db():
    create_test_db()

def test_load_users(patch_data_dir, setup_db):
    result = dict(transform_csvs())
    load_users(result['users'])
    with Session(test_engine()) as session:
        result = session.execute(select(User.id, User.name, User.email, User.signup_date)).all()
    assert list(result) == [tuple((int(row[0]), row[1], row[2], datetime.fromisoformat(row[3]))) for row in transformed_csv_data['users']]


