"""This module is used to capture keyboard inputs using PyGame."""

import time

import pygame
from djitellopy import tello


def init(width=400, height=400):
    """Initialize Pygame Library and Set Control Display as 400x400 pixel."""
    # initialize pygame library
    pygame.init()
    # Set Control Display as 400x400 pixel

    pygame.display.set_caption("Drone Control with Gesture Recognition")

    return pygame.display.set_mode((width, height))


def getKey(KeyName):
    """Return True if the Key is Pressed, False Otherwise."""
    ans = False
    KeyInput = pygame.key.get_pressed()
    mykey = getattr(pygame, "K_" + KeyName)

    if KeyInput[mykey]:
        ans = True

    pygame.display.update()
    return ans


def getKeyboardInput(Drone_instance: tello.Tello) -> list[int]:
    """
    This function is used to get the keyboard input and return the values
    :param Drone_instance: tello.Tello
    :return: list[int]
    """
    # LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if getKey("LEFT"):
        lr = -speed  # Controlling The Left And Right Movement
    elif getKey("RIGHT"):
        lr = speed

    if getKey("UP"):
        fb = moveSpeed  # Controlling The Front And Back Movement
    elif getKey("DOWN"):
        fb = -moveSpeed

    if getKey("w"):
        ud = liftSpeed  # Controlling The Up And Down Movemnt:
    elif getKey("s"):
        ud = -liftSpeed

    if getKey("d"):
        yv = rotationSpeed  # Controlling the Rotation:
    elif getKey("a"):
        yv = -rotationSpeed

    if getKey("q"):
        if Drone_instance.is_flying:
            Drone_instance.land()
        time.sleep(3)  # Landing The Drone
    elif getKey("e"):
        if not Drone_instance.is_flying:
            Drone_instance.takeoff()  # Take Off The Drone

    return [lr, fb, ud, yv]  # Return The Given Value


def main():
    """Print the Key Pressed."""
    while getKey("LEFT"):
        print("Left key pressed")

    if getKey("RIGHT"):
        print("Right key pressed")


if __name__ == "__main__":
    init()
    while True:
        main()
