from random import randint
import time
import pygame


class Fuel(pygame.sprite.Sprite):
    image = None
    image_name = "assets/fuel.png"
    v = None
    capacity = 10

    def __init__(self, x, y, vx, vy):
        super().__init__()
        if Fuel.image is None:
            Fuel.image = pygame.image.load(self.image_name)
        self.rect = Fuel.image.get_rect()
        self.center = self.rect.center = (x, y)
        self.v = vx, vy
        self._tpre = time.monotonic()

    def update(self, state, screen_size=(1024, 768)):
        delta = time.monotonic() - self._tpre
        self._tpre = time.monotonic()

        self.center = [a + b * delta for a, b in zip(self.center, self.v)]

        if not (0 <= self.center[0] < screen_size[0]):
            self.center = self.center[0] % screen_size[0], self.center[1]
        if not (0 <= self.center[1] < screen_size[1]):
            self.center = self.center[0], self.center[1] % screen_size[1]

        self.rect.center = tuple(map(int, self.center))
