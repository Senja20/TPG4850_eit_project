"""
Create model

This module is used to get data, train a model and save model to the current directory.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from os import getenv
from dotenv import load_dotenv

from Classes.GestureClassifier import GestureClassifier
from utils import create_data_loaders, get_data_from_file


def main():
    load_dotenv()
    # device configuration (CPU or GPU) - CUDA is used if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # hyperparameters
    input_size = int(getenv("NUMBER_LANDMARKS")) * int(
        getenv("NUMBER_OF_CHANNELS")
    )  # Assuming 21 landmarks with X, Y, and Z coordinates
    hidden_size = 64
    output_size = int(getenv("OUTPUY_LAYER"))  # Number of classes (UP or DOWN)
    num_epochs = int(getenv("EPOCHS"))
    batch_size = int(getenv("BATCH_SIZE"))
    learning_rate = float(getenv("LEARNING_RATE"))

    train_set, val_set = get_data_from_file("hand_landmarks_dataset.csv")

    # create data loader instances
    train_loader, val_loader = create_data_loaders(train_set, val_set, batch_size)

    train_loader_iterator = iter(train_loader)
    features, labels = next(train_loader_iterator)

    model = GestureClassifier(input_size, hidden_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    n_total_steps = len(train_loader)

    for epoch in range(num_epochs):
        for index, (features, labels) in enumerate(train_loader):
            features = features.to(device)
            labels = labels.to(device)

            # forward
            outputs = model(features)

            loss = criterion(outputs, labels)

            # backwards
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (index + 1) % 10 == 0:
                print(
                    f"epoch {epoch + 1} / {num_epochs}, step {index+1} / {n_total_steps}, loss = {loss.item():.4}"
                )

    # test
    with torch.no_grad():
        n_correct = 0
        n_samples = 0
        for samples, labels in val_loader:
            samples = samples.to(device)
            labels = labels.to(device)

            outputs = model(samples)
            predicted_class = None
            # value index
            with torch.no_grad():
                if outputs.dim() > 1:
                    _, predicted_class = torch.max(outputs, 1)
                else:
                    _, predicted_class = torch.max(outputs, 0)
                n_samples += labels.shape[0]
                n_correct += (predicted_class == labels).sum().item()

        acc = 100.0 * n_correct / n_samples

        print(f"accuracy = {acc}")

    torch.save(model, "gesture_model.pth")


if __name__ == "__main__":
    main()
