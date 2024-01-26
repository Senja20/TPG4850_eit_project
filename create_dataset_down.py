import cv2
import csv
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

frame_counter = 0
skip_frames = 4  # Skip processing for the next 4 frames

# Open a CSV file for writing
csv_file = open("hand_landmarks_dataset.csv", "a", newline="")
csv_writer = csv.writer(csv_file)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1

    if frame_counter % (skip_frames + 1) == 0:
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

                    print(idx)
                    print(landmark)
                    print(landmark.visibility)
                landmark_data.append("DOWN")
                csv_writer.writerow(landmark_data)

        cv2.imshow("Hand Landmarks", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q") or key == 27:  # 27 is the ASCII value for Escape key
            break

csv_file.close()

cap.release()
cv2.destroyAllWindows()
