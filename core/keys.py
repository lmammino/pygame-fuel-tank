import pygame

key_up = set()
key_up_reset = set()


def add_up(k):
    key_up.add(k)


def update():
    for x in key_up_reset:
        key_up.remove(x)
    key_up_reset.clear()


class KeyPressed:
    def __getitem__(self, k):
        return pygame.key.get_pressed()[k]


class KeyUp:
    def __getitem__(self, k):
        if k in key_up:
            key_up_reset.add(k)
            return True
        return False
