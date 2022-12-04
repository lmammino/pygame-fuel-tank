from dataclasses import dataclass
from math import atan2, sin, cos, pi

import pygame
from __main__ import app

import sprites
from core import Commands, Entity, Query, Time

from . import GameState, Scene, Velocity


@dataclass
class Spin:
    roration_spin: int

    def __mul__(self, other):
        return self.roration_spin * other


@app.system
def rotation(
    time: Time,
    query: Query(sprites.Rock, Spin),
):
    delta = time.delta_seconds()
    for sprite, spin in query:
        sprite.relative_rotation(spin * delta)


@app.system
def asteroid_ship_collision(
    commands: Commands,
    rock_query: Query(sprites.Rock),
    ship_query: Query(sprites.Ship, Entity),
    game_state: Query(GameState),
):
    for (rock,) in rock_query:
        for ship_sprite, ship_entity in ship_query:
            if pygame.sprite.collide_mask(ship_sprite, rock):
                commands.kill(ship_entity)
                commands.spawn().insert(sprites.Explosion(*ship_sprite.center))
                game_state[0].scene = Scene.GAMEOVER


@app.system
def explosion_animation(
    commands: Commands,
    time: Time,
    query: Query(sprites.Explosion, Entity),
):
    delta = time.delta_seconds()
    for (sprite, entity) in query:
        sprite.push_time(delta)
        if sprite.first_loop_done:
            commands.kill(entity)
            sprite.kill()


@app.system
def asteroids_collision(
    time: Time, rock_query: Query(sprites.Rock, Velocity, Entity), collisions_cache: dict
):
    delta = time.delta_seconds()
    for k in collisions_cache:
        collisions_cache[k] -= delta
    rocks = list(rock_query)
    for i, (rock1, v1, entity1) in enumerate(rocks):
        for rock2, v2, entity2 in rocks[i + 1 :]:
            if collisions_cache.get((entity1.id, entity2.id), 0) > 0:
                continue
            if pygame.sprite.collide_mask(rock1, rock2):
                collisions_cache[(entity1.id, entity2.id)] = 1                
                teta = atan2(
                    rock1.center[1] - rock2.center[1], rock1.center[0] - rock2.center[0]
                )
                # TODO Optimize, precomputing math
                # TODO take the spin in account
                vel1 = (v1.vx**2 + v1.vy**2) ** 0.5
                teta1 = atan2(v1.vy, v1.vx)
                vel2 = (v2.vx**2 + v2.vy**2) ** 0.5
                teta2 = atan2(v2.vy, v2.vx)

                v1.vx = vel1 * cos(pi + 2 * teta - teta1)
                v1.vy = vel1 * sin(pi + 2 * teta - teta1)
                v2.vx = vel2 * cos(pi + 2 * teta - teta2)
                v2.vy = vel2 * sin(pi + 2 * teta - teta2)
