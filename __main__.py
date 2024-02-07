# pylint: disable=invalid-name
"""
This file is used to load the model and use it for inference
This file use the use_model.py file to load the model and use it for inference
"""

import cv2

from use_model import UseModel

if __name__ == "__main__":

    use_model = UseModel()
    while True:
        use_model.increment_counter()
        if use_model.frame_counter % (use_model.skip_frames + 1) == 0:
            use_model.classified_gesture()

            key = cv2.waitKey(1)
            if (
                key & 0xFF == ord("q") or key == 27
            ):  # 27 is the ASCII value for Escape key
                break

    use_model.cap.release()
    cv2.destroyAllWindows()
