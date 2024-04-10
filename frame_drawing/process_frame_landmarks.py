"""
Process a frame and return the results
"""

from cv2 import COLOR_BGR2RGB, cvtColor


def process_frame_landmarks(frame, model):
    """
    Process a frame and return the results
    :param frame: frame to process
    :param model: model to use for processing
    """
    rgb_frame = cvtColor(frame, COLOR_BGR2RGB)  # Convert the BGR image to RGB
    return model.process(rgb_frame)
