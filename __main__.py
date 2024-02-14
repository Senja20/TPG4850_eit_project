# pylint: disable=invalid-name
"""
This file is used to load the model and use it for inference
This file use the use_model.py file to load the model and use it for inference
"""

import time

import cv2
from djitellopy import tello

from drone import KeyboardTelloModule as kp
from use_model import UseModel


def getKeyboardInput(Drone):
    # LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"):
        lr = -speed  # Controlling The Left And Right Movement
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = moveSpeed  # Controlling The Front And Back Movement
    elif kp.getKey("DOWN"):
        fb = -moveSpeed

    if kp.getKey("w"):
        ud = liftSpeed  # Controlling The Up And Down Movemnt:
    elif kp.getKey("s"):
        ud = -liftSpeed

    if kp.getKey("d"):
        yv = rotationSpeed  # Controlling the Rotation:
    elif kp.getKey("a"):
        yv = -rotationSpeed

    if kp.getKey("q"):
        if Drone.is_flying:
            Drone.land()
        time.sleep(3)  # Landing The Drone
    elif kp.getKey("e"):
        if not Drone.is_flying:
            Drone.takeoff()  # Take Off The Drone

    if kp.getKey("z"):  # Screen Shot Image From The Camera Display
        # cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]  # Return The Given Value


if __name__ == "__main__":

    use_model = UseModel()
    kp.init()

    # Start Connection With Drone
    Drone = tello.Tello()
    Drone.connect()

    Drone.streamon()

    while True:

        try:

            keyValues = getKeyboardInput(Drone)

            use_model.increment_counter()

            if use_model.frame_counter % (use_model.skip_frames + 1) == 0:
                output_scores, predicted_class, ret = use_model.classified_gesture()

                # give command to the drone, based on the output_scores
                if (
                    keyValues[0] == 0
                    and keyValues[1] == 0
                    and keyValues[2] == 0
                    and keyValues[3] == 0
                ):

                    if predicted_class is None:
                        Drone.send_rc_control(0, 0, 0, 0)
                        continue

                    match use_model.swapped_label_map[float(predicted_class)]:
                        case "UP":
                            print("UP")
                            Drone.send_rc_control(0, 0, 80, 0)

                        case "DOWN":
                            print("DOWN")
                            Drone.send_rc_control(0, 0, -80, 0)

                        case _:
                            print("NO MATCH")

                            Drone.send_rc_control(0, 0, 0, 0)

                else:
                    print("Using Keyboard Input")
                    Drone.send_rc_control(
                        keyValues[0], keyValues[1], keyValues[2], keyValues[3]
                    )

                key = cv2.waitKey(1)
                if (
                    key & 0xFF == ord("q") or key == 27
                ):  # 27 is the ASCII value for Escape key
                    break
        except Exception as e:
            print(e)
            Drone.emergency()

    use_model.cap.release()
    cv2.destroyAllWindows()
