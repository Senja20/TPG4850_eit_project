"""
Initialize the hands module.
"""

import mediapipe as mp


def initialize_hands() -> mp.solutions.hands.Hands:
    """
    Initialize the hands module
    :return: hands module
    """

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    return hands
