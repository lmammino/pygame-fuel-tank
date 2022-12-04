from math import pi, cos, sin
import pygame
import time

class Ship(pygame.sprite.Sprite):  # TODO have my own sprite class
    images = []
    image = None
    image_name = "assets/ship.png"
    image_idx = 0
    sprite_aspect = (2, 2)
    sprite_fps = 10
    # TODO move to a Transform Component
    rotation = 0
    center = (0, 0)

    def __init__(self, x, y):
        super().__init__()
        self._t0 = time.monotonic()

        if not Ship.images:
            image_map = pygame.image.load(Ship.image_name)
            w = image_map.get_width() // self.sprite_aspect[0]
            h = image_map.get_height() // self.sprite_aspect[1]
            for i in range(self.sprite_aspect[0]):
                for j in range(self.sprite_aspect[1]):
                    Ship.images.append(image_map.subsurface((w * i, h * j, w, h)))

        self.image = Ship.images[0]
        self.rect = self.image.get_rect()
        self.center = self.rect.center = x, y
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.images[self.image_idx], rotation)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def animate(self, on):
        if on:
            pre = self.image_idx
            self.image_idx = (
                1 + (int((time.monotonic() - self._t0) * self.sprite_fps)) % 3
            )  # TODO magic number
            if pre != self.image_idx:
                self.set_rotation(self.rotation)
        else:
            self.image_idx = 0
            self.set_rotation(self.rotation)
