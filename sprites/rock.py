from math import cos, pi, sin
from random import randint

import pygame


class Rock(pygame.sprite.Sprite):
    images = None
    image_idx = 0
    image = None
    # TODO move to a Transform Component
    rotation = 0
    center = (0, 0)

    def __init__(self, x, y, scale=1):
        super().__init__()
        self.image = pygame.Surface(
            (64 * scale, 64 * scale), pygame.SRCALPHA, 32
        ).convert_alpha()

        coords = []
        sections = randint(5, 8)
        for i in range(sections):
            d = randint(16, 31) * scale
            teta = 2 * pi / sections * i
            coords.append((32 * scale + cos(teta) * d, 32 * scale + sin(teta) * d))
        pygame.draw.lines(self.image, (255, 255, 255), True, coords, width=1)
        stack = [(32 * scale, 32 * scale)]
        while stack:
            xx, yy = stack.pop()
            if self.image.get_at((xx, yy)) == (0, 0, 0, 0):
                self.image.set_at((xx, yy), (0, 0, 0))
                stack.append((xx + 1, yy))
                stack.append((xx - 1, yy))
                stack.append((xx, yy + 1))
                stack.append((xx, yy - 1))

        self.images = [self.image]

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.center = self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.images[self.image_idx], rotation)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def relative_rotation(self, rotation):
        self.set_rotation(self.rotation + rotation)
