# pylint: disable=invalid-name
"""
This file is used to load the model and use it for inference
This file use the use_model.py file to load the model and use it for inference
"""
from atexit import register
from os import getenv

from cv2 import destroyAllWindows
from djitellopy import tello
from dotenv import load_dotenv
from pygame import display

from drone import KeyboardTelloModule as kp
from use_model import UseModel
from utils import connect_to_wifi

if __name__ == "__main__":
    load_dotenv()

    drone_on = False  # Define and assign a boolean value to the variable 'drone_on'
    use_model = UseModel()
    running = True
    frame_width, frame_height = int(getenv("FRAME_WIDTH")), int(getenv("FRAME_HEIGHT"))
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

            # give command to the, drone, based on the output_scores
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

                load_dotenv()

                match use_model.swapped_label_map[float(predicted_class)]:
                    case "UP":
                        print("UP")
                        if drone_on:
                            Drone.send_rc_control(0, 0, int(getenv("LIFT_SPEED")), 0)

                    case "DOWN":
                        print("DOWN")
                        if drone_on:
                            Drone.send_rc_control(0, 0, -int(getenv("LIFT_SPEED")), 0)

                    case "LEFT":
                        print("LEFT")
                        if drone_on:
                            Drone.send_rc_control(-int(getenv("SPEED")), 0, 0, 0)

                    case "RIGHT":
                        print("RIGHT")
                        if drone_on:
                            Drone.send_rc_control(int(getenv("SPEED")), 0, 0, 0)

                    case "FRONT":
                        print("FRONT")
                        if drone_on:
                            Drone.send_rc_control(0, int(getenv("MOVE_SPEED")), 0, 0)

                    case "BACK":
                        print("BACK")
                        if drone_on:
                            Drone.send_rc_control(0, -int(getenv("MOVE_SPEED")), 0, 0)

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
