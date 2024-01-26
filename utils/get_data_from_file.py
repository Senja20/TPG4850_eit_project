from pandas import read_csv, to_numeric
from sklearn.model_selection import train_test_split


def get_data_from_file(
    file_name: str,
    label_name: str = "Label",
    test_size: float = 0.1,
    random_state: int = 42,
):
    df = read_csv(file_name)

    # Ensure that the 'Label' column is of type string - important: it will be converted into number based on string label
    df[label_name] = df[label_name].astype(str)

    # make sure that data are numbers
    landmarks_columns = (
        [f"X{i}" for i in range(21)]
        + [f"Y{i}" for i in range(21)]
        + [f"Z{i}" for i in range(21)]
    )
    df[landmarks_columns] = df[landmarks_columns].apply(to_numeric, errors="coerce")

    # Drop rows with missing values
    df = df.dropna()

    # data split into training and not training
    return train_test_split(
        df, test_size=test_size, random_state=random_state, stratify=df["Label"]
    )
