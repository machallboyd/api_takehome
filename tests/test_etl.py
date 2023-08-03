import csv
import io

import pytest

from api_takehome.app import csv_cleaner

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

clean_output = [
    ["1", "Alice", "alice@example.com", "2023-01-01"],
    ["2", "Bob", "bob@example.com", "2023-02-01"],
]


@pytest.mark.parametrize("test_input", user_csvs)
def test_cleaner(test_input):
    with io.StringIO() as f:
        print(test_input)
        f.write(test_input)
        f.seek(0)
        assert clean_output == list(csv_cleaner(csv.reader(f)))

