from .commands import Commands

commands = Commands()


class Query:
    def __init__(self, *search_for):
        self.search_for = tuple(search_for)

    def __call__(self):
        return self

    def __iter__(self):
        def gen():
            for entity in commands.get_all_entities():
                y = []
                for s in self.search_for:
                    for component in entity:
                        if isinstance(
                            component, s
                        ):  # TODO optimize filter with maps of entities and set intersections
                            y.append(component)
                if len(y) == len(self.search_for):
                    yield y

        return gen()

    def __getitem__(self, n):
        for components in self:
            return components[n]
        raise IndexError()

    def __len__(self):
        return len(list(self.__iter__()))

    def first(self):
        for components in self:
            return components
