import pygame


class Star(pygame.sprite.Sprite):
    image_map = None
    images = None
    image = None
    image_name = "assets/star.png"
    aspect = (2, 2)
    speed = 60

    def __init__(self, x, y):
        super().__init__()
        if Star.image_map is None:
            Star.image_map = pygame.image.load(self.image_name)
            w = Star.image_map.get_width() // self.aspect[0]
            h = Star.image_map.get_height() // self.aspect[1]
            Star.images = []
            for i in range(self.aspect[0]):
                for j in range(self.aspect[1]):
                    Star.images.append(Star.image_map.subsurface((w * i, h * j, w, h)))
        self.n = 0
        self.image = Star.images[self.n]
        self.rect = Star.images[0].get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        self.image = Star.images[(self.n // self.speed) % len(Star.images)]
        self.n += 1
        self.n %= 65535
        screen.blit(self.image, self.rect)
