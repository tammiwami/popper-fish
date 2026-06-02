from enum import Enum

import pygame

from src.game.constants import POWERUP_SIZES, POWERUP_VELOCITY


class PowerUpType(Enum):
    PEARL = "pearl"
    SHELL = "shell"
    SEAWEED = "seaweed"
    ALGAE = "algae"


class PowerUp:
    def __init__(self, x, y, powerup_type, image):
        self.type = powerup_type
        width, height = POWERUP_SIZES[self.type.value]
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.y += POWERUP_VELOCITY
        self.image_rect.center = self.rect.center
