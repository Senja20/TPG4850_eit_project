"""
This file is used to create a dataset of hand landmarks and labels (UP or DOWN).
"""
import csv
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

FRAME_COUNTER = 0
SKIP_FRAMES = 4  # Skip processing for the next 4 frames
ADDED_ITEM = 0

# Open a CSV file for writing
csv_file = open("hand_landmarks_dataset.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
header_row = (
    ["X" + str(i) for i in range(21)]
    + ["Y" + str(i) for i in range(21)]
    + ["Z" + str(i) for i in range(21)]
    + ["Label"]
)
csv_writer.writerow(header_row)


while True:
    ret, frame = cap.read()

    # Break if there is no frame OR 300 samples have been added
    if not ret or ADDED_ITEM == 300:
        break

    FRAME_COUNTER += 1

    if FRAME_COUNTER % (SKIP_FRAMES + 1) == 0:
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and get hand landmarks
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_data = []
                # Access hand landmarks (21 points)
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    height, width, _ = frame.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    cv2.putText(
                        frame,
                        str(idx),
                        (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                    )
                    landmark_data.extend([landmark.x, landmark.y, landmark.z])

                landmark_data.append("UP")
                ADDED_ITEM += 1
                csv_writer.writerow(landmark_data)

        cv2.imshow("Hand Landmarks", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q") or key == 27:  # 27 is the ASCII value for Escape key
            break

csv_file.close()

cap.release()
cv2.destroyAllWindows()
