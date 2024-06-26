"""
This file is used to create a dataset of hand landmarks and labels (UP or DOWN).
"""

from csv import writer
from os import getenv

from cv2 import VideoCapture, destroyAllWindows, imshow, waitKey
from dotenv import load_dotenv

from frame_drawing import draw_landmarks, process_frame_landmarks
from utils import initialize_hands

hands = initialize_hands()

cap = VideoCapture(0)


# Open a CSV file for writing
def main():
    """
    Main function
    :return: None
    """
    load_dotenv()

    frame_counter = int(getenv("FRAME_COUNTER"))
    skip_frames = int(getenv("SKIP_FRAMES"))  # Skip processing for the next 4 frames
    added_item = 0

    with open(
        getenv("HAND_LANDMARKS_DATASET"), "a", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = writer(csv_file)

        while True:
            ret, frame = cap.read()

            # Break if there is no frame OR 500 samples have been added
            if not ret or added_item == 500:
                break

            frame_counter += 1

            if frame_counter % (skip_frames + 1) == 0:
                # Process the frame and get hand landmarks
                results = process_frame_landmarks(frame, hands)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmark_data, frame = draw_landmarks(hand_landmarks, frame)
                        landmark_data.append("BACK")
                        added_item += 1
                        csv_writer.writerow(landmark_data)

                imshow("Hand Landmarks", frame)

                if (
                    waitKey(1) & 0xFF == ord("q") or waitKey(1) == 27
                ):  # 27 is the ASCII value for Escape key
                    break

    cap.release()
    destroyAllWindows()


if "__main__" == __name__:
    main()
