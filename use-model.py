import torch
import cv2
import mediapipe as mp
from Classes.GestureClassifier import GestureClassifier


def load_model():
    loaded_model = torch.load("gesture_model.pth")
    loaded_model.eval()  # Set the model to evaluation mode
    return loaded_model


def process_frame(frame, model):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the BGR image to RGB
    return model.process(rgb_frame)


def classify_gesture(landmark_data, model, device):
    new_data = torch.tensor(landmark_data)
    new_data = new_data.to(
        device
    )  # Send data to the same device (cuda or cpu) as your model
    outputs = model(new_data)

    print("output", outputs)

    with torch.no_grad():
        if outputs.dim() > 1:
            _, predicted_class = torch.max(outputs, 1)
        else:
            _, predicted_class = torch.max(outputs, 0)

    predicted_class = predicted_class.item()

    return predicted_class


def draw_landmarks(frame, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
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


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    loaded_model = load_model()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    cap = cv2.VideoCapture(0)

    frame_counter = 0
    skip_frames = 4  # Skip processing for the next 4 frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        if frame_counter % (skip_frames + 1) == 0:
            results = process_frame(frame, hands)

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

                        # Add the coordinates of the landmark to the list
                        landmark_data.extend([landmark.x, landmark.y, landmark.z])

                    predicted_class = classify_gesture(
                        landmark_data, loaded_model, device
                    )

                    # Print or use the predicted class
                    if predicted_class == 1:
                        print("The predicted class is: Thumb Up")
                    else:
                        print("The predicted class is: Thumb Down")

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
