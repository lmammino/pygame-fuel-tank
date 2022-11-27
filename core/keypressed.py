import pygame


class KeyPressed:
    def __init__(self):
        pass

    def __getitem__(self, k):
        return pygame.key.get_pressed()[k]
