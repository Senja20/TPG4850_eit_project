"""
Draws the top scores and their corresponding class labels on the frame.
"""

import cv2


def draw_top_scores(frame, top_scores, class_labels):
    """
    Draws the top scores and their corresponding class labels on the frame.
    :param frame: frame to draw on
    :param top_scores: top scores to draw
    :param class_labels: class labels to draw
    """
    y_offset = 20

    for i, (score, label) in enumerate(zip(top_scores, class_labels)):
        text = f"{label}: {score:.2f}"
        cv2.putText(
            frame,
            text,
            (10, y_offset + i * 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
