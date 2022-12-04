from dataclasses import dataclass
import uuid

class Entity:
    def __init__(self):
        self._components = []
        self.id = uuid.uuid4()

    def insert(self, *components):
        self._components.extend(components)
        return self

    def __iter__(self):
        def gen():
            yield self
            yield from self._components

        return gen()

_entities = []


def spawn() -> Entity:
    ret = Entity()
    _entities.append(ret)
    return ret


class Commands:
    def __init__(self):
        pass

    def spawn(self) -> Entity:
        return spawn()

    def kill(self, entity):
        _entities.remove(entity)

    def get_all_entities(self) -> list[Entity]:
        return _entities

