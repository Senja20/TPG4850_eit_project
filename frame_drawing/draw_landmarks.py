"""
Draw landmarks on a frame
"""

from cv2 import FILLED, circle, line

lines = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),
]


def draw_landmarks(hand_landmarks, frame) -> tuple:
    """
    Draw landmarks on a frame
    :param hand_landmarks: landmarks for a single hand
    :param frame: frame to draw on

    :return: landmark data, frame
    """

    height, width, _ = frame.shape
    landmark_data = []

    # Draw lines between landmarks
    for pair in lines:
        landmark_a = hand_landmarks.landmark[pair[0]]
        landmark_b = hand_landmarks.landmark[pair[1]]

        ax, ay = int(landmark_a.x * width), int(landmark_a.y * height)
        bx, by = int(landmark_b.x * width), int(landmark_b.y * height)

        line(frame, (ax, ay), (bx, by), (0, 255, 255), 2)

    # Iterate through each landmark
    for landmark in hand_landmarks.landmark:
        # Draw circle for each landmark
        cx, cy = int(landmark.x * width), int(landmark.y * height)
        circle(frame, (cx, cy), 5, (255, 0, 0), FILLED)

        # Add the coordinates of the landmark to the list
        landmark_data.extend([landmark.x, landmark.y, landmark.z])

    return landmark_data, frame
