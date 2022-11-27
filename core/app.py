import inspect

import pygame

from . import board, keys
from .commands import Commands


class App:
    def __init__(
        self,
        title,
        screen_size=(1920, 1080),
        board_size=(1920, 1080),
        fps=0,
        bg_color=(0, 0, 0),
    ):
        self._screen_size = screen_size
        self._board_size = board.size = board_size
        self._fps = fps
        self._bg_color = bg_color
        self._title = title
        self._setup = []
        self._system = []
        self._deferred_writes = []

    def setup(self, original_fx):
        def fx():
            kv = {
                k: v.annotation()
                for k, v in inspect.signature(original_fx).parameters.items()
            }
            return original_fx(**kv)

        self._setup.append(fx)
        return fx

    def system(self, original_fx):
        kv = {
            k: v.annotation()
            for k, v in inspect.signature(original_fx).parameters.items()
        }

        def fx():
            return original_fx(**kv)

        self._system.append(fx)
        return fx


    def deferred_write(self, text, x):
        self._deferred_writes.append(lambda: self.write(text, x ))

    def write(self, text, x, cache={}):
        font = cache.setdefault("font", pygame.font.SysFont("Verdana", 24))

        w = self.screen.get_width()
        self.screen.blit(font.render(text, 0, (255, 255, 255)), (w // 4 * x + 1, 1))
        self.screen.blit(font.render(text, 0, (120, 120, 120)), (w // 4 * x, 0))

    def gameover(self, text="GAME OVER", cache={}):
        gameover_font = cache.setdefault("font", pygame.font.SysFont("Verdana", 48))

        w = self.screen.get_width()
        h = self.screen.get_height()
        size = gameover_font.size(text)
        self.screen.blit(
            gameover_font.render(text, 0, (255, 255, 255)),
            ((w - size[0]) // 2 + 1, (h - size[1]) // 2 + 1),
        )
        self.screen.blit(
            gameover_font.render(text, 0, (120, 120, 120)),
            ((w - size[0]) // 2, (h - size[1]) // 2),
        )

    def run(self):
        pygame.init()

        commands = Commands()

        self.screen = pygame.display.set_mode(self._screen_size)  # , pygame.FULLSCREEN)
        pygame.display.set_caption(self._title)
        board = pygame.Surface(self._board_size)
        clock = pygame.time.Clock()

        # setups
        for fx in self._setup:
            fx()

        running = True
        while running:
            clock.tick(self._fps)
            # quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    keys.add_up(event.key)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            if running:
                # recomputes
                for fx in self._system:
                    fx()

                keys.update()

                # draws
                board.fill(self._bg_color)
                for entity in commands.get_all_entities():
                    for component in entity:
                        if hasattr(component, "draw"):
                            component.draw(board)

            self.screen.blit(board, (0, 0))
            # fps
            self.write(f"{clock.get_fps():.02f} fps", 0)
            # deferred writes
            while self._deferred_writes:
                self._deferred_writes.pop()()

            pygame.display.flip()

        pygame.quit()
