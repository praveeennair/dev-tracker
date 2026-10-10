import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

REPORTERS_FILE = os.path.join(BASE_DIR, 'reporters.json')
ISSUES_FILE = os.path.join(BASE_DIR, 'issues.json')


def create_json_file_if_not_exists(filename):
    """
    Create the JSON file with an empty list
    if the file does not exist.
    """

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f, indent=4)


def read_json(filename):
    """
    Read data from a JSON file.
    If the file does not exist, create it first.
    """

    create_json_file_if_not_exists(filename)

    with open(filename, 'r') as f:
        return json.load(f)


def write_json(filename, data):
    """
    Write data to a JSON file.
    """

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
