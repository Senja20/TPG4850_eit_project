# pylint: disable=invalid-name
"""
This file is used to load the model and use it for inference
This file use the use_model.py file to load the model and use it for inference
"""


from atexit import register

from cv2 import destroyAllWindows
from djitellopy import tello
from pygame import display

from drone import KeyboardTelloModule as kp
from use_model import UseModel
from utils import connect_to_wifi

if __name__ == "__main__":
    drone_on = False  # Define and assign a boolean value to the variable 'drone_on'
    use_model = UseModel()
    running = True
    frame_width, frame_height = 640, 360
    screen = kp.init(frame_width, frame_height)

    # Start Connection With Drone
    if drone_on:
        connect_to_wifi()

        Drone = tello.Tello()
        Drone.connect()

        Drone.streamon()

    @register
    def exit_handler():
        """Function to handle the exit of the program"""
        print("Program Ended")
        if drone_on:
            Drone.land()
            Drone.end()
        use_model.cap.release()
        destroyAllWindows()

    while running:

        use_model.increment_counter()

        if use_model.frame_counter % (use_model.skip_frames + 1) == 0:
            output_scores, predicted_class, frame = use_model.classified_gesture()

            screen.blit(frame, (0, 0))

            display.update()

            keyValues, running = kp.get_keyboard_input(Drone if drone_on else use_model)

            # give command to the drone, based on the output_scores
            if (
                keyValues[0] == 0
                and keyValues[1] == 0
                and keyValues[2] == 0
                and keyValues[3] == 0
            ):

                if predicted_class is None:
                    if drone_on:
                        Drone.send_rc_control(0, 0, 0, 0)
                    continue

                match use_model.swapped_label_map[float(predicted_class)]:
                    case "UP":
                        print("UP")
                        if drone_on:
                            Drone.send_rc_control(0, 0, 80, 0)

                    case "DOWN":
                        print("DOWN")
                        if drone_on:
                            Drone.send_rc_control(0, 0, -80, 0)

                    case _:
                        print("NO MATCH")

                        if drone_on:
                            Drone.send_rc_control(0, 0, 0, 0)

            else:
                print("Using Keyboard Input")
                if drone_on:
                    Drone.send_rc_control(
                        keyValues[0], keyValues[1], keyValues[2], keyValues[3]
                    )
