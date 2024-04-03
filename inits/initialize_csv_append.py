"""
Initialize a CSV writer
"""

from csv import writer
from os import getenv

from dotenv import load_dotenv


def initialize_csv_append() -> tuple:
    """
    Initialize a CSV writer
    :return: CSV writer
    """
    load_dotenv()

    csv_file = open(getenv("HAND_LANDMARKS_DATASET"), "a", newline="", encoding="utf-8")
    csv_writer = writer(csv_file)
    return csv_file, csv_writer
