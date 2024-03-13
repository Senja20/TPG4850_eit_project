"""This module is used to capture keyboard inputs using PyGame."""

from time import sleep

from djitellopy import tello
from pygame import KEYDOWN, constants, display
from pygame import event as pygame_event
from pygame import init as pygame_init
from pygame import quit as pygame_quit


def init(width=400, height=400):
    """Initialize Pygame Library and Set Control Display as 400x400 pixel."""
    # initialize pygame library
    pygame_init()
    # Set Control Display as 400x400 pixel

    display.set_caption("Drone Control with Gesture Recognition")

    return display.set_mode((width, height))


def get_key_pressed() -> int:
    """
    Return the key pressed.
    :return: int
    """
    for event in pygame_event.get():
        if event.type == KEYDOWN:
            return event.key
    return None


def get_keyboard_input(Drone_instance: tello.Tello) -> tuple[list[int], bool]:
    """
    This function is used to get the keyboard input and return the values
    :param Drone_instance: tello.Tello
    :return: list[int], bool
    """
    # LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100
    keep_running = True

    match get_key_pressed():
        case constants.K_LEFT:
            lr = -speed  # Controlling The Left And Right Movement
        case constants.K_RIGHT:
            lr = speed
        case constants.K_UP:
            fb = moveSpeed  # Controlling The Front And Back Movement
        case constants.K_DOWN:
            fb = -moveSpeed
        case constants.K_w:
            ud = liftSpeed  # Controlling The Up And Down Movemnt:
        case constants.K_s:
            ud = -liftSpeed
        case constants.K_d:
            yv = rotationSpeed  # Controlling the Rotation:
        case constants.K_a:
            yv = -rotationSpeed
        case constants.K_q:
            if Drone_instance.is_flying:
                Drone_instance.land()
            sleep(3)  # Landing The Drone
        case constants.K_e:
            if not Drone_instance.is_flying:
                Drone_instance.takeoff()  # Take Off The Drone
        case constants.K_ESCAPE:
            pygame_quit()
            print("Quitting")
            keep_running = False

    return [lr, fb, ud, yv], keep_running  # Return The Given Value


def main():
    """Print the Key Pressed."""

    if get_key_pressed() is not None:
        print("Key Pressed: ", get_key_pressed())


if __name__ == "__main__":
    init()
    while True:
        main()
