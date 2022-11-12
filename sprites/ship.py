from math import pi, cos, sin
import pygame
import time

from .explosion import Explosion


class Ship(pygame.sprite.Sprite):
    images = []
    image = None
    image_name = "assets/ship.png"
    image_idx = 0
    pre_image_idx = 0
    sprite_aspect = (2, 2)
    rotation = 0
    pre_rotation = 0
    acceleration = 100
    rotation_speed = 100
    fuel_efficency = 20
    v = (0, 0)
    center = (0, 0)

    def __init__(self, x, y, t0=None):
        super().__init__()
        if t0 is None:
            t0 = time.monotonic()
        self.t0 = t0
        self.n = 0

        image_map = pygame.image.load(Ship.image_name)
        w = image_map.get_width() // self.sprite_aspect[0]
        h = image_map.get_height() // self.sprite_aspect[1]
        for i in range(self.sprite_aspect[0]):
            for j in range(self.sprite_aspect[1]):
                self.images.append(image_map.subsurface((w * i, h * j, w, h)))
        self.image = self.images[0]

        self.rect = self.images[0].get_rect()
        self.center = self.rect.center = x, y
        self._tpre = time.monotonic()
        self.mask = pygame.mask.from_surface(self.images[0])

    def update(self, state, screen_size=(1024, 768)):
        delta = time.monotonic() - self._tpre
        self._tpre = time.monotonic()

        key_pressed = pygame.key.get_pressed()
        self.brain(key_pressed, delta, state)

        if self.pre_rotation != self.rotation or self.pre_image_idx != self.image_idx:
            self.pre_rotation = self.rotation
            self.pre_image_idx = self.image_idx
            self.image = pygame.transform.rotate(
                self.images[self.image_idx], self.rotation
            )
            self.mask = pygame.mask.from_surface(self.image)

        self.center = [a + b * delta for a, b in zip(self.center, self.v)]

        if not (0 <= self.center[0] < screen_size[0]):
            self.center = self.center[0] % screen_size[0], self.center[1]
        if not (0 <= self.center[1] < screen_size[1]):
            self.center = self.center[0], self.center[1] % screen_size[1]

        self.rect.center = tuple(map(int, self.center))
        rotation_correction = [
            b - a for a, b in zip(self.images[0].get_size(), self.image.get_size())
        ]
        self.rect.center = (
            self.rect.center[0] - rotation_correction[0] // 2,
            self.rect.center[1] - rotation_correction[1] // 2,
        )

        #        hits = pygame.sprite.spritecollide(self, state['sprites']['fuel'], True)
        for fuel in state["sprites"]["fuel"].sprites():
            if pygame.sprite.collide_mask(self, fuel):
                fuel.kill()
                state["fuel"] = min(state["max_fuel"], state["fuel"] + fuel.capacity)

        for rock in state["sprites"]["rocks"].sprites():
            if pygame.sprite.collide_mask(self, rock):
                state["sprites"]["player"].add(Explosion(*self.rect.center))
                self.kill()
                state["game"] = "over"

    def brain(self, key_pressed, delta, state):
        if key_pressed[pygame.K_RIGHT]:
            self.rotation -= self.rotation_speed * delta
            self.rotation %= 360
        elif key_pressed[pygame.K_LEFT]:
            self.rotation += self.rotation_speed * delta
            self.rotation %= 360
        if key_pressed[pygame.K_UP] and state["fuel"] > 0:
            self.image_idx += 1
            self.image_idx %= 4
            if self.image_idx == 0:
                self.image_idx += 1
            teta = self.rotation * pi / 180
            self.v = (
                self.v[0] - sin(teta) * delta * self.acceleration,
                self.v[1] - cos(teta) * delta * self.acceleration,
            )
            state["fuel"] = max(
                0, state["fuel"] - delta * self.acceleration / self.fuel_efficency
            )
        else:
            self.image_idx = 0
