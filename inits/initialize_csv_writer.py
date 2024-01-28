"""
Initialize a CSV writer
"""

from csv import writer


def initialize_csv_writer():
    """
    Initialize a CSV writer
    :return: CSV writer
    """
    with open(
        "hand_landmarks_dataset.csv", "w", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = writer(csv_file)
        header_row = (
            ["X" + str(i) for i in range(21)]
            + ["Y" + str(i) for i in range(21)]
            + ["Z" + str(i) for i in range(21)]
            + ["Label"]
        )
        csv_writer.writerow(header_row)

        return csv_file, csv_writer
