"""
Create model

This module is used to get data, train a model and save model to the current directory.
"""

import torch
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
import torch.nn as nn
import torch.optim as optim

from Classes.HandLandmarksDataset import HandLandmarksDataset
from Classes.GestureClassifier import GestureClassifier

from utils import get_data_from_file

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# hyperparameters
input_size = 21 * 3  # Assuming 21 landmarks with X, Y, and Z coordinates
hidden_size = 64
output_size = 2  # Number of classes (UP or DOWN)
num_epochs = 15
batch_size = 10
learning_rate = 0.001


train_set, val_set = get_data_from_file("hand_landmarks_dataset.csv")

# create data loader instances
train_loader = DataLoader(
    HandLandmarksDataset(train_set), batch_size=batch_size, shuffle=True
)
val_loader = DataLoader(
    HandLandmarksDataset(val_set), batch_size=batch_size, shuffle=False
)


train_loader_iterator = iter(train_loader)
features, labels = next(train_loader_iterator)

model = GestureClassifier(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

n_total_steps = len(train_loader)

for epoch in range(num_epochs):
    for index, (features, labels) in enumerate(train_loader):
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
