from dataclasses import dataclass
from enum import Enum, auto

import pygame
from __main__ import app

from core import Query, Time, Board


class Scene(Enum):
    PLAYING = auto()
    GAMEOVER = auto()
    MAINMENU = auto()


@dataclass
class GameState:
    fuel_left: int
    scene: Scene


@dataclass
class Velocity:
    vx: float
    vy: float


@app.system
def velocity(time: Time, query: Query(Velocity, pygame.sprite.Sprite), board: Board):
    delta = time.delta_seconds()
    for velocity, sprite in query:
        new_center = (
            sprite.center[0] + velocity.vx * delta,
            sprite.center[1] + velocity.vy * delta,
        )

        if not (0 <= new_center[0] < board[0]):  # screen_size[0]
            new_center = new_center[0] % board[0], new_center[1]
        if not (0 <= new_center[1] < board[1]):
            new_center = new_center[0], new_center[1] % board[1]

        sprite.center = new_center
        sprite.rect.center = tuple(map(int, new_center))


@app.system
def show_still_to_collect(
    query: Query(GameState),
):
    fuel_count = query[0].fuel_left
    app.deferred_write(f"FUEL LEFT: {fuel_count}", 3)


@app.system
def time_passed(
    time: Time,
):
    app.deferred_write(f"TIME: {time.elapsed_seconds():0.1f}", 1)
