"""This module is used to capture keyboard inputs using PyGame."""

import pygame


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
