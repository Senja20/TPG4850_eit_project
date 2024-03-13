"""
Process a frame and return the results
"""

import cv2

def process_frame_landmarks(frame, model):
    """
    Process a frame and return the results
    :param frame: frame to process
    :param model: model to use for processing
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the BGR image to RGB
    return model.process(rgb_frame)
