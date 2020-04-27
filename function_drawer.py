import cv2
import sys
import os
import config

import numpy as np
from math import *


def calculate(_function: str, x: [int, float]) -> float:
    try:
        return eval(_function.replace("x", str(x)))
    except ZeroDivisionError:
        return eval(_function.replace("x", str(x + 0.1)))
    except SyntaxError:
        return 0


def prepare_surface(*args, **kwargs) -> np.ndarray:
    surface: np.ndarray = np.zeros(
        (config.img_width, config.img_height, 3), np.uint8)
    surface[np.where(surface == 0)] = 255

    x_offset = int(config.img_width / 2)
    y_offset = int(config.img_height / 2)

    for y in range(surface.shape[0]):
        valueY: float = (y - y_offset) / config.img_unit
        if valueY % 1.0 == 0.0:
            surface = cv2.line(surface, (0, y), (config.img_width, y), (200, 200, 200), 1)
            surface = cv2.line(surface, (x_offset - 5, y), (x_offset + 5, y), (0, 0, 0), 1)
            surface = cv2.putText(surface, str(int(-valueY)), (x_offset + 10, y), 1, 1, (0, 0, 0))

    for x in range(surface.shape[1]):
        valueX: float = (x - x_offset) / config.img_unit
        if valueX % 1.0 == 0.0:
            surface = cv2.line(surface, (x, 0), (x, config.img_height), (200, 200, 200), 1)
            surface = cv2.line(surface, (x, y_offset - 5), (x, y_offset + 5), (0, 0, 0), 1)
            surface = cv2.putText(surface, str(int(valueX)), (x, y_offset + 20), 1, 1, (0, 0, 0))

    surface = cv2.line(surface, (x_offset, 0), (x_offset, config.img_height), (0, 0, 0), 1)
    surface = cv2.line(surface, (0, y_offset), (config.img_width, y_offset), (0, 0, 0), 1)

    return surface


def draw_function(function: str, surface: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_offset = int(config.img_width / 2)
    y_offset = int(config.img_height / 2)

    color = config.color(*args, **kwargs)

    x_pos_prev = None
    y_pos_prev = None

    for x in range(surface.shape[1]):
        x_value = (x - x_offset) / config.img_unit
        y_value = calculate(function, x_value)

        x_pos = int(x_value * config.img_unit + x_offset)
        y_pos = int(-y_value * config.img_unit + y_offset)

        if x_pos_prev is None:
            x_pos_prev = x_pos

        if y_pos_prev is None:
            y_pos_prev = y_pos

        surface = cv2.circle(surface, (x_pos, y_pos), 1, color, -1)
        surface = cv2.line(surface, (x_pos_prev, y_pos_prev), (x_pos, y_pos), color, 1)

        y_pos_prev = y_pos
        x_pos_prev = x_pos

    return surface


def make_image_of_functions(functions: str, *args, **kwargs) -> np.ndarray:
    functions: list = functions.split(";")
    surface: np.ndarray = prepare_surface()

    for function in functions:
        surface = draw_function(function, surface)

    return surface


def save_img(img: np.ndarray, name: str, *args, **kwargs) -> None:
    if not os.path.exists(config.imgs_path):
        os.mkdir(config.imgs_path)
    cv2.imwrite(f"{config.imgs_path}/{name}", img)


if __name__ == '__main__':
    pass
