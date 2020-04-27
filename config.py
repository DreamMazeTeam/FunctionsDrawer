from random import randint as rand

imgs_path = "imgs/new.jpg"
img_width = 900
img_height = 900
img_unit = 50


def color(*args, **kwargs) -> tuple:
    return rand(0, 255), rand(0, 255), rand(0, 255)
