"""
Initialize a CSV writer
"""

from csv import writer
from os import getenv

from dotenv import load_dotenv


def initialize_csv_append():
    """
    Initialize a CSV writer
    :return: CSV writer
    """
    load_dotenv()

    with open(
        getenv("HAND_LANDMARKS_DATASET"), "a", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = writer(csv_file)
        return csv_file, csv_writer
