import time
from math import cos, pi, sin
from random import randint

import pygame


class Rock(pygame.sprite.Sprite):
    image = None
    rot_image = None
    v = None

    def __init__(self, x, y, vx, vy):
        super().__init__()

        self.image = pygame.Surface((64, 64), pygame.SRCALPHA, 32).convert_alpha()

        coords = []
        sections = randint(5, 8)
        for i in range(sections):
            d = randint(16, 31)
            teta = 2 * pi / sections * i
            coords.append((32 + cos(teta) * d, 32 + sin(teta) * d))
        pygame.draw.lines(self.image, (255, 255, 255), True, coords)
        stack = [(32, 32)]
        while stack:
            xx, yy = stack.pop()
            if self.image.get_at((xx, yy)) == (0, 0, 0, 0):
                self.image.set_at((xx, yy), (0, 0, 0))
                stack.append((xx + 1, yy))
                stack.append((xx - 1, yy))
                stack.append((xx, yy + 1))
                stack.append((xx, yy - 1))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.center = self.rect.center = (x, y)
        self.v = vx, vy
        self._tpre = time.monotonic()
        self.last_hit = time.monotonic()

    def update(self, state, screen_size=(1024, 768)):
        delta = time.monotonic() - self._tpre
        self._tpre = time.monotonic()

        for rock in state["sprites"]["rocks"].sprites():
            if (
                self is not rock
                and pygame.sprite.collide_mask(self, rock)
                and self.last_hit + 0.1 < time.monotonic()
            ):
                self.last_hit = time.monotonic()
                rock.last_hit = time.monotonic()
                rock.v = self.v = (self.v[0] + rock.v[0]) / 2, (self.v[1] + rock.v[1]) / 2

        self.center = [a + b * delta for a, b in zip(self.center, self.v)]

        if not (0 <= self.center[0] < screen_size[0]):
            self.center = self.center[0] % screen_size[0], self.center[1]
        if not (0 <= self.center[1] < screen_size[1]):
            self.center = self.center[0], self.center[1] % screen_size[1]

        self.rect.center = tuple(map(int, self.center))
