import pygame

class Explosion(pygame.sprite.Sprite):
    image_map = None
    images = None
    image = None
    image_name = "assets/explosion.png"
    aspect = (6, 1)
    speed = 8

    def __init__(self, x, y):
        super().__init__()
        if Explosion.image_map is None:
            Explosion.image_map = pygame.image.load(self.image_name)
            w = Explosion.image_map.get_width() // self.aspect[0]
            h = Explosion.image_map.get_height() // self.aspect[1]
            Explosion.images = []
            for i in range(self.aspect[0]):
                for j in range(self.aspect[1]):
                    Explosion.images.append(
                        Explosion.image_map.subsurface((w * i, h * j, w, h))
                    )
        self.n = 0
        self.image = Explosion.images[self.n]
        self.rect = Explosion.images[0].get_rect()
        self.rect.center = (x, y)

    def update(self, state, screen_size=(1024, 768)):
        self.image = Explosion.images[self.n // self.speed]
        self.n += 1
        if self.n // self.speed >= len(Explosion.images):
            self.kill()

