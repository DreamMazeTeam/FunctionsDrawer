import os
import sys

try:
    import cv2
except ImportError:
    os.system("pip install opencv-python")
    import cv2

import numpy as np
from math import *

PI = Pi = P = p = pi
E = e

GLOBAL: dict = {
    "function": "x",
    "unit": 50,
    "help": False,
    "SAVE_TO_FILE": False,

    "color": {
        "background": (255, 255, 255),
        "lines": [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    },

    "size": {
        "height": 900,
        "width": 900,
    }
}


def mouseCallback(event, x, y, flag, param):
    if flag == cv2.EVENT_FLAG_CTRLKEY:
        GLOBAL["help"] = True
    else:
        GLOBAL["help"] = False

    # print(f"Event: {event}")
    # print(f"Flag: {flag}")


def parseArgs(args: list) -> None:
    for i, arg in enumerate(args):
        if arg in ("function", "-f", "--def"):
            GLOBAL["function"] = args[i + 1].split(";")
        elif arg in ("--save", "-s"):
            GLOBAL["SAVE_TO_FILE"] = True
        elif arg in ("unit", "--unit", "-u"):
            GLOBAL["unit"] = int(args[i + 1])


def calculate(_function: str, x: [int, float]) -> float:
    try:
        return eval(_function.replace("x", str(x)))
    except ZeroDivisionError:
        return eval(_function.replace("x", str(x + 0.1)))


def draw(surface, _function, options, xOffset, yOffset, color):
    first: bool = True

    xSide = "full" if "!+x" not in _function else "positive"
    ySide = "full" if "!+y" not in _function else "positive"

    for x in range(surface.shape[1]):
        valueX: float = (x - xOffset) / options['unit']
        valueY = calculate(_function, valueX)

        positionX: int = int(valueX * options['unit'] + xOffset)
        positionY: int = int(-valueY * options['unit'] + yOffset)

        if first:
            prevPosX = positionX
            prevPosY = positionY
            first = False

        # if not positionY > yOffset and not positionY < -yOffset:
        surface = cv2.circle(surface, (positionX, positionY), 1, color, -1)
        surface = cv2.line(surface, (prevPosX, prevPosY), (positionX, positionY), color, 1)

        prevPosX = positionX
        prevPosY = positionY

    return surface


def render(options: dict = None) -> None:
    options = GLOBAL if options is None else options

    windowName = f"F(x) = {options['function']}"
    windowWidth = options['size']['width']
    windowHeight = options['size']['height']

    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, mouseCallback, options)
    cv2.resizeWindow(windowName, windowWidth, windowHeight)

    surface: np.ndarray = np.zeros((windowWidth, windowHeight, 3), np.uint8)
    surface[np.where(surface == 0)] = 255

    xOffset = int(windowWidth / 2)
    yOffset = int(windowHeight / 2)

    pt1 = (xOffset, 0)
    pt2 = (xOffset, windowHeight)

    surface = cv2.line(surface, pt1, pt2, (0, 0, 0), 1)

    pt1 = (0, yOffset)
    pt2 = (windowWidth, yOffset)

    surface = cv2.line(surface, pt1, pt2, (0, 0, 0), 1)

    for y in range(surface.shape[0]):
        valueY: float = (y - yOffset) / options['unit']
        if valueY % 1.0 == 0.0:
            surface = cv2.line(surface, (0, y), (windowWidth, y), (200, 200, 200), 1)
            surface = cv2.line(surface, (xOffset - 5, y), (xOffset + 5, y), (0, 0, 0), 1)
            surface = cv2.putText(surface, str(int(-valueY)), (xOffset + 10, y), 1, 1, (0, 0, 0))

    for x in range(surface.shape[1]):
        valueX: float = (x - xOffset) / options['unit']
        if valueX % 1.0 == 0.0:
            surface = cv2.line(surface, (x, 0), (x, windowHeight), (200, 200, 200), 1)
            surface = cv2.line(surface, (x, yOffset - 5), (x, yOffset + 5), (0, 0, 0), 1)
            surface = cv2.putText(surface, str(int(valueX)), (x, yOffset + 20), 1, 1, (0, 0, 0))

    pt1 = (xOffset, 0)
    pt2 = (xOffset, windowHeight)

    surface = cv2.line(surface, pt1, pt2, (0, 0, 0), 1)

    pt1 = (0, yOffset)
    pt2 = (windowWidth, yOffset)

    surface = cv2.line(surface, pt1, pt2, (0, 0, 0), 1)

    for function, color in zip(options['function'], options['color']['lines']):
        surface = draw(surface, function, options, xOffset, yOffset, color)

    if GLOBAL["SAVE_TO_FILE"]:
        cv2.imwrite(f'function.png', surface)

    cv2.imshow(windowName, surface)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(args: list) -> None:
    parseArgs(args)
    render(GLOBAL)


if __name__ == '__main__':
    if "function" in sys.argv:
        main(sys.argv)
    else:
        func = input("\tВведите -1 в f(x) для выхода\nf(x) >> ")
        while func.strip() != "-1":
            main(["-s", "function", func])
            function = input("f(x) >> ")
