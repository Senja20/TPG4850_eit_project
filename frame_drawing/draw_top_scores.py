import cv2


def draw_top_scores(frame, top_scores, class_labels):
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
