import pygame


def init():
    # initialize pygame library
    pygame.init()
    # Set Control Display as 400x400 pixel
    windows = pygame.display.set_mode((400, 400))


def getKey(KeyName):
    ans = False
    for ene in pygame.event.get():
        pass
    KeyInput = pygame.key.get_pressed()
    mykey = getattr(pygame, "K_{}".format(KeyName))

    if KeyInput[mykey]:
        ans = True

    pygame.display.update()
    return ans


def main():
    while getKey("LEFT"):
        print("Left key pressed")

    if getKey("RIGHT"):
        print("Right key pressed")


if __name__ == "__main__":
    init()
    while True:
        main()
