import pygame


def write(text, x, screen, cache={}):
    font = cache.setdefault("font", pygame.font.SysFont("Verdana", 24))

    w = screen.get_width()
    screen.blit(font.render(text, 0, (255, 255, 255)), (w // 4 * x + 1, 1))
    screen.blit(font.render(text, 0, (120, 120, 120)), (w // 4 * x, 0))


def gameover(screen, text="GAME OVER", cache={}):
    gameover_font = cache.setdefault("font", pygame.font.SysFont("Verdana", 48))

    w = screen.get_width()
    h = screen.get_height()
    size = gameover_font.size(text)
    screen.blit(
        gameover_font.render(text, 0, (255, 255, 255)),
        ((w - size[0]) // 2 + 1, (h - size[1]) // 2 + 1),
    )
    screen.blit(
        gameover_font.render(text, 0, (120, 120, 120)),
        ((w - size[0]) // 2, (h - size[1]) // 2),
    )
