import os
import pygame


def graphic_loader(path, mask_color):
    image = pygame.image.load(os.path.abspath(path))
    image.set_colorkey(mask_color)
    return image.convert()


def graphic_resizer(image, percentage):
    scale_factor = percentage / 100

    width = image.get_width()
    height = image.get_height()

    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))


def graphic_hz_flip(image):
    return pygame.transform.flip(image, True, False)


def graphic_vert_flip(image):
    return pygame.transform.flip(image, False, True)
