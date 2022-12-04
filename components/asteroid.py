from dataclasses import dataclass

import pygame
from __main__ import app


import sprites
from core import Query, Time, Commands, Entity

from . import GameState, Scene


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
def asteroid_collision(
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
