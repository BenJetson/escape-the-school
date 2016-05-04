import os
import pygame


def graphic_loader(path, width=None, height=None, colorKey=None):
    image = pygame.image.load(os.path.abspath(path))

    if colorKey:
        image = image.set_colorkey(colorKey)
        image = image.convert()

    if ((width and height) and
            (width.isnumeric() and height.isnumeric()) and
            (width > 0 and height > 0)):
        return pygame.transform.scale(image, width, height)

    return image


def graphic_resizer(image, percentage):
    scale_factor = percentage / 100

    width = image.get_width()
    height = image.get_height()

    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))


def graphic_absolute_resize(image, w=None, h=None):

    if w and not h:
        h = (image.get_height() * w) / image.get_width()
    elif h and not w:
        w = (image.get_width() * h) / image.get_height()
    else:
        w = image.get_width()
        h = image.get_height()

    return pygame.transform.scale(image, (int(w), int(h)))


def graphic_hz_flip(image):
    return pygame.transform.flip(image, True, False)


def graphic_vert_flip(image):
    return pygame.transform.flip(image, False, True)
