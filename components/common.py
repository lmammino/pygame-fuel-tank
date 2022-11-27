from dataclasses import dataclass

import pygame
from __main__ import app

from core import Query, Time, Board


@dataclass
class Velocity:
    vx: float
    vy: float


@app.system
def velocity(
    time: Time,
    query: Query(Velocity, pygame.sprite.Sprite),
    board: Board
):
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
