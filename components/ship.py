from dataclasses import dataclass

import pygame
from __main__ import app

from core import KeyPressed, Query, Time, KeyUp
from sprites import Ship

from . import Velocity
from math import sin, cos, pi


@dataclass
class Starship:
    rotation_speed: int


@dataclass
class Engine:
    fuel: float
    thrust: float
    fuel_efficency: float
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
def engine_on(
    time: Time,
    key_pressed: KeyPressed,
    key_up: KeyUp,
    query: Query(Velocity, Ship, Engine),
):
    delta = time.delta_seconds()
    if key_pressed[pygame.K_UP]:
        vel, ship_sprite, engine = query.first()
        if engine.fuel > 0:
            teta = ship_sprite.rotation * pi / 180
            vel.vx -= sin(teta) * delta * engine.thrust
            vel.vy -= cos(teta) * delta * engine.thrust
            engine.is_on = True
            engine.fuel -= delta * engine.thrust / engine.fuel_efficency
            if engine.fuel < 0:
                engine.fuel = 0
        else:
            engine.is_on = False
            ship_sprite.animate(False)
    elif key_up[pygame.K_UP]:
        _, ship_sprite, engine = query.first()
        engine.is_on = False
        ship_sprite.animate(False)


@app.system
def animation(
    query: Query(Ship, Engine),
):
    ship_sprite, engine = query.first()
    if engine.is_on:
        ship_sprite.animate(True)
