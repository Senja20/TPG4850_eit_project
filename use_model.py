"""
This file is used to load the model and use it for inference
"""
from os import getenv
import torch
import cv2
import mediapipe as mp
from dotenv import load_dotenv
from config import label_map

# utils
from utils import load_model, get_device

from frame_drawing import draw_landmarks, draw_top_scores


def process_frame_landmarks(frame, model):
    """
    Process a frame and return the results
    :param frame: frame to process
    :param model: model to use for processing
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the BGR image to RGB
    return model.process(rgb_frame)


def classify_gesture(landmark_data, model, device):
    """
    Classify a gesture based on the landmark data
    :param landmark_data: landmark data to use for classification
    :param model: model to use for classification
    :param device: device to use for classification
    """
    new_data = torch.tensor(landmark_data)
    new_data = new_data.to(
        device
    )  # Send data to the same device (cuda or cpu) as your model
    outputs = model.forward(new_data)

    with torch.no_grad():
        if outputs.dim() > 1:
            _, predicted_class = torch.max(outputs, 1)
        else:
            _, predicted_class = torch.max(outputs, 0)

    predicted_class = predicted_class.item()

    return predicted_class, outputs


def initialize():
    """
    Initialize the model and the device
    :return: device and swapped label map
    """
    load_dotenv()
    return get_device(), {v: k for k, v in label_map.items()}


def main():
    """
    Main function
    """
    device, swapped_label_map = initialize()

    loaded_model = load_model(device)

    hands = mp.solutions.hands.Hands()

    cap = cv2.VideoCapture(0)

    frame_counter = 0
    skip_frames = 4  # Skip processing for the next 4 frames
    num_classes = int(getenv("OUTPUT_LAYER"))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        if frame_counter % (skip_frames + 1) == 0:
            results_landmark = process_frame_landmarks(frame, hands)

            if results_landmark.multi_hand_landmarks:
                for hand_landmarks in results_landmark.multi_hand_landmarks:
                    landmark_data = []
                    # Access hand landmarks (21 points)
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        # Add the coordinates of the landmark to the list
                        frame = draw_landmarks(idx, frame, landmark)
                        landmark_data.extend([landmark.x, landmark.y, landmark.z])

                    predicted_class, output_scores = classify_gesture(
                        landmark_data, loaded_model, device
                    )

                    print(
                        "predicted class: ", swapped_label_map[float(predicted_class)]
                    )

                    top_scores, top_indices = torch.topk(output_scores, num_classes)

                    draw_top_scores(
                        frame,
                        top_scores,
                        [
                            f"Class {swapped_label_map[float(idx)]}"
                            for idx in top_indices
                        ],
                    )

            cv2.imshow("Hand Landmarks", frame)

            key = cv2.waitKey(1)

            if (
                key & 0xFF == ord("q") or key == 27
            ):  # 27 is the ASCII value for Escape key
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
