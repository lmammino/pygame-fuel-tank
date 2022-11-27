from random import randint
import time
import pygame


class Fuel(pygame.sprite.Sprite):
    image = None
    image_name = "assets/fuel.png"

    def __init__(self, x, y):
        super().__init__()
        if Fuel.image is None:
            Fuel.image = pygame.image.load(Fuel.image_name)
        self.rect = Fuel.image.get_rect()
        self.center = self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(Fuel.image, self.rect)
