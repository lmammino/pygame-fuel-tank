import os
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

    # spawn the spaceship
    commands.spawn().insert(
        Starship(100),
        Velocity(0, 0),
        Engine(1000, 100, False),
        sprites.Ship(BOARD_SIZE[0] // 2, BOARD_SIZE[1] // 2),
    )


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    app.run()
