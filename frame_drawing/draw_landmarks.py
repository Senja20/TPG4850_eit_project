import cv2


def draw_landmarks(index, frame, landmark):
    height, width, _ = frame.shape
    cx, cy = int(landmark.x * width), int(landmark.y * height)
    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    cv2.putText(
        frame,
        str(index),
        (cx, cy),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        1,
    )

    return frame
