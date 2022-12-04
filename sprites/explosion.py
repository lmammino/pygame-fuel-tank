import pygame


class Explosion(pygame.sprite.Sprite):
    image_map = None
    images = None
    image = None
    image_name = "assets/explosion.png"
    aspect = (6, 1)
    animation_fps = 6
    first_loop_done = False

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
        self.image_idx = 0
        self.image = Explosion.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._t0 = 0

    def push_time(self, delta_seconds):
        self._t0 += delta_seconds
        self.image_idx = int(self._t0 * self.animation_fps) % len(Explosion.images)
        self.image = Explosion.images[self.image_idx]
        if int(self._t0 * self.animation_fps) >= len(Explosion.images):
            self.first_loop_done = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
