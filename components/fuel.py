from dataclasses import dataclass

import pygame
from __main__ import app

import sprites
from core import Query, Entity, Commands

from .ship import Engine


@dataclass
class Fuel:
    capacity: int


@app.system
def rotate_ship(
    commands: Commands,
    fuel_query: Query(sprites.Fuel, Fuel, Entity),
    ship_query: Query(sprites.Ship, Engine),
):
    for fuel_sprite, fuel, fuel_entity in fuel_query:
        for ship_sprite, engine in ship_query:
            if pygame.sprite.collide_mask(ship_sprite, fuel_sprite):
                engine.fuel += fuel.capacity
                if engine.fuel > 1000:  # TODO magic number
                    engine.fuel = 1000
                commands.kill(fuel_entity)

@app.system
def show_fuel(
    query: Query(Engine),
):
    fuel = query[0].fuel
    app.deferred_write(f"FUEL: {fuel:.02f}", 2)
