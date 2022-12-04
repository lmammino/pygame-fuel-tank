from dataclasses import dataclass

import pygame
from __main__ import app

import sprites
from core import Query, Entity, Commands

from . import GameState, Engine


@dataclass
class Fuel:
    capacity: int


@app.system
def fuel_collision(
    commands: Commands,
    fuel_query: Query(sprites.Fuel, Fuel, Entity),
    ship_query: Query(sprites.Ship, Engine),
    game_state: Query(GameState),
):
    for fuel_sprite, fuel, fuel_entity in fuel_query:
        for ship_sprite, engine in ship_query:
            if pygame.sprite.collide_mask(ship_sprite, fuel_sprite):
                engine.fuel += fuel.capacity
                if engine.fuel > engine.max_fuel:
                    engine.fuel = engine.max_fuel
                commands.kill(fuel_entity)
                game_state[0].fuel_left -= 1


@app.system
def show_fuel(
    query: Query(Engine),
):
    for (engine,) in query:
        app.deferred_write(f"FUEL: {engine.fuel:.02f}", 2)
