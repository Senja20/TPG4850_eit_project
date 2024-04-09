"""
Draws the top scores and their corresponding class labels on the frame.
"""

from typing import Literal

from cv2 import FILLED, FONT_HERSHEY_SIMPLEX, circle, line, putText

color_fill: tuple[Literal[255], Literal[255], Literal[255]] = (255, 255, 255)
color_stroke: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)


def draw_arrow(frame, a, b, c):
    """
    Draws an arrow to the frame
    :param frame: frame to draw on
    :param a: edge 1
    :param b: edge 2
    :param c: center

    :return: None
    """

    line(frame, a, c, color_stroke, 8)
    line(frame, b, c, color_stroke, 8)
    line(frame, a, c, color_fill, 6)
    line(frame, b, c, color_fill, 6)


def draw_command(frame, class_label: str) -> None:
    """
    Draws an indication of the current drone command
    :param frame: frame to draw on
    :param class_labels: the top scoring class label

    :return: None
    """

    height, width, _ = frame.shape

    height = int(height * 0.75)  # Reported height is not accurate

    match class_label:
        case "UP":
            a = (int(0.35 * width), int(0.15 * height))
            b = (int(0.65 * width), int(0.15 * height))
            c = (width // 2, int(0.05 * height))

            draw_arrow(frame, a, b, c)
        case "DOWN":
            a = (int(0.35 * width), int(0.85 * height))
            b = (int(0.65 * width), int(0.85 * height))
            c = (width // 2, int(0.95 * height))

            draw_arrow(frame, a, b, c)
        case "LEFT":
            a = (int(0.15 * width), int(0.35 * height))
            b = (int(0.15 * width), int(0.65 * height))
            c = (int(0.05 * width), height // 2)

            draw_arrow(frame, a, b, c)
        case "RIGHT":
            a = (int(0.85 * width), int(0.35 * height))
            b = (int(0.85 * width), int(0.65 * height))
            c = (int(0.95 * width), height // 2)

            draw_arrow(frame, a, b, c)
        case "FRONT":
            a = (int(0.45 * width), int(0.4 * height))
            b = (int(0.55 * width), int(0.6 * height))
            c = (int(0.45 * width), int(0.6 * height))
            d = (int(0.55 * width), int(0.4 * height))

            line(frame, a, b, color_stroke, 8)
            line(frame, c, d, color_stroke, 8)
            line(frame, a, b, color_fill, 6)
            line(frame, c, d, color_fill, 6)
        case "BACK":
            center = (int(0.5 * width), int(0.5 * height))

            circle(frame, center, 6, color_stroke, FILLED)
            circle(frame, center, 50, color_stroke, 7)
            circle(frame, center, 5, color_fill, FILLED)
            circle(frame, center, 50, color_fill, 5)
        case _:
            return


x_offset = 60
y_offset = 20
font = FONT_HERSHEY_SIMPLEX
font_size = 0.5
font_color: tuple[Literal[255], Literal[255], Literal[255]] = (255, 255, 255)
font_thickness = 1


def draw_top_scores(frame, top_scores, class_labels: list[str]) -> None:
    """
    Draws the top scores and their corresponding class labels on the frame.
    :param frame: frame to draw on
    :param top_scores: top scores to draw
    :param class_labels: class labels to draw
    """

    draw_command(frame=frame, class_label=class_labels[0])

    for i, (score, label) in enumerate(zip(top_scores, class_labels)):
        putText(
            frame,
            f"{label}:",
            (10, y_offset + i * 20),
            font,
            font_size,
            font_color,
            font_thickness,
        )

        putText(
            frame,
            f"{score:.2f}",
            (10 + x_offset, y_offset + i * 20),
            font,
            font_size,
            font_color,
            font_thickness,
        )
