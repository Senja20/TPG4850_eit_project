"""This module is used to capture keyboard inputs using PyGame."""

from os import getenv
from time import sleep

from djitellopy import tello
from dotenv import load_dotenv
from pygame import constants, display
from pygame import event as event_list
from pygame import init as pygame_init
from pygame import key as pygame_key
from pygame import quit as pygame_quit

load_dotenv()


def init(width=int(getenv("DISPLAY_WIDTH")), height=int(getenv("DISPLAY_HEIGHT"))):
    """Initialize Pygame Library and Set Control Display from .env ."""
    # initialize pygame library
    pygame_init()
    # Set Control Display as 400x400 pixel

    display.set_caption("Drone Control with Gesture Recognition")

    return display.set_mode((width, height))


def get_key(KeyName):
    """Return True if the Key is Pressed, False Otherwise."""

    # * Due to limitations with the library, this for-loop is required to retrieve keyboard inputs
    for _ in event_list.get():
        pass

    ans = False
    KeyInput = pygame_key.get_pressed()
    mykey = getattr(constants, "K_" + KeyName)

    if KeyInput[mykey]:
        ans = True

    display.update()
    return ans


def get_keyboard_input(Drone_instance: tello.Tello) -> tuple[list[int], bool]:
    """
    This function is used to get the keyboard input and return the values
    :param Drone_instance: tello.Tello
    :return: list[int]
    """

    load_dotenv()

    # LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = int(getenv("SPEED"))
    liftSpeed = int(getenv("LIFT_SPEED"))
    moveSpeed = int(getenv("MOVE_SPEED"))
    rotationSpeed = int(getenv("ROTATION_SPEED"))
    keep_running = True

    if get_key("LEFT"):
        lr = -speed  # Controlling The Left And Right Movement
    elif get_key("RIGHT"):
        lr = speed

    if get_key("UP"):
        fb = moveSpeed  # Controlling The Front And Back Movement
    elif get_key("DOWN"):
        fb = -moveSpeed

    if get_key("w"):
        ud = liftSpeed  # Controlling The Up And Down Movemnt:
    elif get_key("s"):
        ud = -liftSpeed

    if get_key("d"):
        yv = rotationSpeed  # Controlling the Rotation:
    elif get_key("a"):
        yv = -rotationSpeed

    if get_key("q") and Drone_instance.is_flying:
        Drone_instance.land()  # Landing The Drone
        sleep(3)
    elif get_key("e") and not Drone_instance.is_flying:
        Drone_instance.takeoff()  # Take Off The Drone

    if get_key("ESCAPE"):
        pygame_quit()
        print("Quitting")
        keep_running = False

    return [lr, fb, ud, yv], keep_running  # Return The Given Value


def main():
    """Print the Key Pressed."""
    while get_key("LEFT"):
        print("Left key pressed")

    if get_key("RIGHT"):
        print("Right key pressed")


if __name__ == "__main__":
    init()
    while True:
        main()
