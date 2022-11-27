from dataclasses import dataclass

import pygame
from __main__ import app

from core import KeyPressed, Query, Time
from sprites import Ship

from . import Velocity
from math import sin,cos,pi


@dataclass
class Starship:
    rotation_speed: int


@dataclass
class Engine:
    fuel: float
    thrust: float
    is_on: bool


@app.system
def rotate_ship(
    time: Time,
    key_pressed: KeyPressed,
    query: Query(Ship, Starship),
):
    delta = time.delta_seconds()
    if key_pressed[pygame.K_RIGHT]:
        for ship_sprite, starship in query:
            # print("Right", time.delta_seconds())
            ship_sprite.set_rotation(
                (ship_sprite.rotation - starship.rotation_speed * delta) % 360
            )
    elif key_pressed[pygame.K_LEFT]:
        for ship_sprite, starship in query:
            # print("Left", time.delta_seconds())
            ship_sprite.set_rotation(
                (ship_sprite.rotation + starship.rotation_speed * delta) % 360
            )


@app.system
def rotate_ship(
    time: Time,
    key_pressed: KeyPressed,
    query: Query(Velocity, Ship, Engine),
):
    delta = time.delta_seconds()
    if key_pressed[pygame.K_UP]:
        teta = query[1].rotation * pi / 180
        query[0].vx -= sin(teta) * delta * 101
        query[0].vy -= cos(teta) * delta * 101
        