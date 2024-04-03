"""
This file is used to load the model and use it for inference
"""

from os import getenv

import mediapipe as mp
from cv2 import COLOR_BGR2RGB, VideoCapture, cvtColor, destroyAllWindows, flip, waitKey
from dotenv import load_dotenv
from pygame import surfarray
from torch import max as torch_max
from torch import no_grad, tensor, topk

from config import label_map
from frame_drawing import draw_landmarks, draw_top_scores, process_frame_landmarks

# utils
from utils import get_device, load_model


class UseModel:
    """
    The class used for loading the model and using it for inference
    """

    load_dotenv()

    frame_counter = int(getenv("FRAME_COUNTER"))
    skip_frames = int(getenv("SKIP_FRAMES"))  # Skip processing for the next 4 frames

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

        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            model_complexity=0,
            max_num_hands=1,
            min_tracking_confidence=0.5,
            min_detection_confidence=0.5,
        )

        self.cap = VideoCapture(0)

    def classify_gesture(self, landmark_data):
        """
        Classify a gesture based on the landmark data
        :param landmark_data: landmark data to use for classification
        :param model: model to use for classification
        :param device: device to use for classification
        """
        new_data = tensor(landmark_data)
        new_data = new_data.to(
            self.device
        )  # Send data to the same device (cuda or cpu) as your model
        outputs = self.loaded_model.forward(new_data)

        with no_grad():
            if outputs.dim() > 1:

                _, predicted_class = torch_max(outputs, 1)
            else:
                _, predicted_class = torch_max(outputs, 0)

        predicted_class = predicted_class.item()

        return predicted_class, outputs

    def increment_counter(self):
        """
        Increment the frame counter
        """
        self.frame_counter += 1

    def classified_gesture(self):
        """
        Classify the gesture and draw the top scores
        :return: output scores, predicted class, frame
        """

        _, frame = self.cap.read()

        frame = flip(frame, 1)

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

                top_scores, top_indices = topk(output_scores, self.num_classes)

                draw_top_scores(
                    frame,
                    top_scores,
                    [
                        f"Class {self.swapped_label_map[float(idx)]}"
                        for idx in top_indices
                    ],
                )

        frame = cvtColor(frame, COLOR_BGR2RGB)

        frame = surfarray.make_surface(frame.swapaxes(0, 1))

        return output_scores, predicted_class, frame


# pylint:disable=duplicate-code
if __name__ == "__main__":
    use_model = UseModel()
    while True:
        use_model.increment_counter()
        if use_model.frame_counter % (use_model.skip_frames + 1) == 0:
            use_model.classified_gesture()

            key = waitKey(1)
            if (
                key & 0xFF == ord("q") or key == 27
            ):  # 27 is the ASCII value for Escape key
                break

    use_model.cap.release()
    destroyAllWindows()
