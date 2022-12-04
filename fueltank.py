import os
from random import randint
import sys

import sprites
from core import App, Commands

args = dict(zip(sys.argv, sys.argv[1:]))

BG_COLOR = (0, 0, 0)
FG_COLOR = [(x + 128) % 256 for x in BG_COLOR]
SCREEN_SIZE = (1980, 1020)
BOARD_SIZE = SCREEN_SIZE
FPS = int(args.get("--fps", 0))
STAR_COUNT = int(args.get("--stars", 100))
FUEL_COUNT = int(args.get("--fuel", 20))
ROCKS_COUNT = int(args.get("--rocks", 10))

app = App("fuel tanker", fps=FPS)

from components import *


@app.setup
def setup(commands: Commands):

    for _ in range(STAR_COUNT):
        commands.spawn().insert(
            sprites.Star(randint(0, BOARD_SIZE[0] - 1), randint(0, BOARD_SIZE[1] - 1))
        )

    for _ in range(FUEL_COUNT):
        commands.spawn().insert(
            sprites.Fuel(randint(0, BOARD_SIZE[0] - 1), randint(0, BOARD_SIZE[1] - 1)),
            Velocity(randint(-10, 10), randint(-10, 10)),
            Fuel(randint(10, 20)),
        )

    rocks = []
    for _ in range(ROCKS_COUNT):
        rock = sprites.Rock(
            randint(0, BOARD_SIZE[0] - 1),
            randint(0, BOARD_SIZE[1] - 1),
            scale=randint(1, 2),
        )
        for rock2 in rocks:
            if pygame.sprite.collide_mask(rock, rock2):
                continue
        rocks.append(rock)
        commands.spawn().insert(
            rock,
            Velocity(randint(-10, 10), randint(-10, 10)),
            Spin(randint(-10, 10)),
        )

    commands.spawn().insert(GameState(FUEL_COUNT, Scene.PLAYING))

    # spawn the spaceship
    commands.spawn().insert(
        Starship(100),
        Velocity(0, 0),
        Engine(100, 100, 100, 10, False),
        sprites.Ship(BOARD_SIZE[0] // 2, BOARD_SIZE[1] // 2),
    )


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    app.run()
