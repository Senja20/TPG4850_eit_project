"""
This file is used to load the model and use it for inference
"""

from os import getenv

import cv2
import mediapipe as mp
import torch
from dotenv import load_dotenv

from config import label_map
from frame_drawing import draw_landmarks, draw_top_scores, process_frame_landmarks

# utils
from utils import get_device, load_model


class UseModel:
    """
    The class used for loading the model and using it for inference
    """

    frame_counter = 0
    skip_frames = 4  # Skip processing for the next 4 frames

    def __init__(self):
        """
        Initialize the model and the device
        :return: device and swapped label map
        """
        load_dotenv()

        self.num_classes = int(getenv("OUTPUT_LAYER"))
        self.device, self.swapped_label_map = get_device(), {
            v: k for k, v in label_map.items()
        }

        self.loaded_model = load_model(self.device)

        self.hands = mp.solutions.hands.Hands()

        self.cap = cv2.VideoCapture(0)

    def classify_gesture(self, landmark_data):
        """
        Classify a gesture based on the landmark data
        :param landmark_data: landmark data to use for classification
        :param model: model to use for classification
        :param device: device to use for classification
        """
        new_data = torch.tensor(landmark_data)
        new_data = new_data.to(
            self.device
        )  # Send data to the same device (cuda or cpu) as your model
        outputs = self.loaded_model.forward(new_data)

        with torch.no_grad():
            if outputs.dim() > 1:

                _, predicted_class = torch.max(outputs, 1)
            else:
                _, predicted_class = torch.max(outputs, 0)

        predicted_class = predicted_class.item()

        return predicted_class, outputs

    def increment_counter(self):
        """
        Increment the frame counter
        """
        self.frame_counter += 1

    def classified_gesture(self):
        """
        Main function
        :return: vector of gesture output scores, ret
        """

        ret, frame = self.cap.read()

        results_landmark = process_frame_landmarks(frame, self.hands)
        output_scores, predicted_class = None, None

        if results_landmark.multi_hand_landmarks:
            for hand_landmarks in results_landmark.multi_hand_landmarks:
                landmark_data = []
                # Access hand landmarks (21 points)
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    # Add the coordinates of the landmark to the list
                    frame = draw_landmarks(idx, frame, landmark)
                    landmark_data.extend([landmark.x, landmark.y, landmark.z])

                predicted_class, output_scores = self.classify_gesture(landmark_data)

                top_scores, top_indices = torch.topk(output_scores, self.num_classes)

                draw_top_scores(
                    frame,
                    top_scores,
                    [
                        f"Class {self.swapped_label_map[float(idx)]}"
                        for idx in top_indices
                    ],
                )

        # cv2.imshow("Hand Landmarks", mat=frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return output_scores, predicted_class, ret, frame


# pylint:disable=duplicate-code
if __name__ == "__main__":
    use_model = UseModel()
    while True:
        use_model.increment_counter()
        if use_model.frame_counter % (use_model.skip_frames + 1) == 0:
            use_model.classified_gesture()

            key = cv2.waitKey(1)
            if (
                key & 0xFF == ord("q") or key == 27
            ):  # 27 is the ASCII value for Escape key
                break

    use_model.cap.release()
    cv2.destroyAllWindows()
