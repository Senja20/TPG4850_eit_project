"""
Initialize the hands module.
"""

from mediapipe import solutions as mp


def initialize_hands() -> mp.hands.Hands:
    """
    Initialize the hands module
    :return: hands module
    """

    return mp.hands.Hands(
        static_image_mode=False,
        model_complexity=0,
        max_num_hands=1,
        min_tracking_confidence=0.5,
        min_detection_confidence=0.5,
    )
