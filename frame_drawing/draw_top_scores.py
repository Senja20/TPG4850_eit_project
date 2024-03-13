"""
Draws the top scores and their corresponding class labels on the frame.
"""

import cv2

x_offset = 60
y_offset = 20
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.5
font_color = (255, 255, 255)
font_thickness = 1

def draw_arrow(frame, class_label):
    """
    Draws an arrow to indicate the current drone command
    :param frame: frame to draw on
    :param class_labels: the top scoring class label, supported labels: UP, DOWN
    """

    height, width, _ = frame.shape

    height = int(height * 0.75) # Reported height is not accurate

    match class_label:
        case "UP":
            ax, ay = int(0.35 * width), int(0.15 * height)
            bx, by = int(0.65 * width), int(0.15 * height)
            cx, cy = width // 2, int(0.05 * height)
        case "DOWN":
            ax, ay = int(0.35 * width), int(0.85 * height)
            bx, by = int(0.65 * width), int(0.85 * height)
            cx, cy = width // 2, int(0.95 * height)
        case "LEFT":
            ax, ay = int(0.15 * width), int(0.35 * height)
            bx, by = int(0.15 * width), int(0.65 * height)
            cx, cy = int(0.05 * width), height // 2
        case "RIGHT":
            ax, ay = int(0.85 * width), int(0.35 * height)
            bx, by = int(0.85 * width), int(0.65 * height)
            cx, cy = int(0.95 * width), height // 2
        case _:
            return

    cv2.line(frame, (ax, ay), (cx, cy), (0, 0, 0), 8) 
    cv2.line(frame, (cx, cy), (bx, by), (0, 0, 0), 8) 
    cv2.line(frame, (ax, ay), (cx, cy), (255, 255, 255), 6) 
    cv2.line(frame, (cx, cy), (bx, by), (255, 255, 255), 6) 

def draw_top_scores(frame, top_scores, class_labels):
    """
    Draws the top scores and their corresponding class labels on the frame.
    :param frame: frame to draw on
    :param top_scores: top scores to draw
    :param class_labels: class labels to draw
    """
    
    draw_arrow(frame, class_labels[0])

    for i, (score, label) in enumerate(zip(top_scores, class_labels)):
        cv2.putText(
            frame,
            f"{label}:",
            (10, y_offset + i * 20),
            font,
            font_size,
            font_color,
            font_thickness,
        )

        cv2.putText(
            frame,
            f"{score:.2f}",
            (10 + x_offset, y_offset + i * 20),
            font,
            font_size,
            font_color,
            font_thickness,
        )
