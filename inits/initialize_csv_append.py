"""
Initialize a CSV writer
"""

from csv import writer


def initialize_csv_append():
    """
    Initialize a CSV writer
    :return: CSV writer
    """
    with open(
        "hand_landmarks_dataset.csv", "a", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = writer(csv_file)
        return csv_file, csv_writer
