from enum import Enum
import random

import pygame

from src.game.constants import FISH_SIZES, FISH_VELOCITY


class FishType(Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3


class Fish:
    def __init__(self, x, y, fish_type, image):
        self.type = fish_type
        self.health = self.type.value

        width, height = FISH_SIZES[self.type.value]
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image

        if random.random() > 0.5:
            self.image = pygame.transform.flip(self.image, True, False)

        self.image_rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.y += FISH_VELOCITY
        self.image_rect.center = self.rect.center
