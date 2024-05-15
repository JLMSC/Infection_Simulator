"""Module responsible for manipulating world entity,
such as it's dimension and living entities."""
from typing import Tuple
from functools import reduce
import numpy as np


from Entity.entity import Entity


class World:
    """Represents a world with random living entities."""

    def __init__(self, shape: int) -> None:
        self.shape: Tuple[int, int] = (shape, shape)
        self.tiles: np.ndarray = np.empty(shape=self.shape, dtype=object)
        self.add_immune_entities()
        self.add_infected_entity()
        self.add_healthy_entities()
        # TODO: Search every infected entity, get its neighbors and infect them if they're not immune.
        # NOTE: np.where WILL do the job, trust me.
        # TODO: Move the infected entity to a random adjacent position. (they should not overlap, dead entities should not move.)
        # NOTE: "(i + 1 + N) % N" or "(i - 1 + N) % N" work for both rows and cols, just adjust the +1 or -1 if necessary.

        # TODO: New infected entities should inherit the property from the infected entity.
        # TODO: Entities heal after 20 steps if not dead (1 step per second) and turn into immune entities.
        # TODO: After every step, log the amount of sintomáticos, assintomáticos, curados e mortos.

    def update_tile(self, position: Tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Spawn a new entity in a tile.

        Parameters
        ----------
        position : Tuple[int, int]
            The tile where the entity will be spawned.
        is_infected : bool
            If the entity is infected.
        is_immune : bool
            If the entity is immune.
        """
        entity = Entity(position=position, is_infected=is_infected, is_immune=is_immune)
        self.tiles[position] = entity.entity_type

    def is_tile_empty(self, position: Tuple[int, int]) -> bool:
        """Check if a tile is an empty tile.

        Parameters
        ----------
        position : Tuple[int, int]
            The tile's position.

        Returns
        -------
        bool
            Whether or not the tile is empty.
        """
        return self.tiles[position] is None

    def add_immune_entities(self) -> None:
        """Transform 5% of population into immune healthy entities."""
        immune_entities_amount = int(np.round((reduce(np.multiply, self.shape) - 1) * 0.05))
        row, col = self.shape
        while immune_entities_amount > 0:
            i = np.random.randint(low=0, high=row)
            j = np.random.randint(low=0, high=col)

            if self.is_tile_empty(position=(i, j)):
                self.update_tile(position=(i, j), is_infected=False, is_immune=True)
                immune_entities_amount -= 1

    def add_infected_entity(self) -> None:
        """Transform one random entity into a infected entity."""
        spawned_infected_entity = False
        row, col = self.shape
        while not spawned_infected_entity:
            i = np.random.randint(low=0, high=row)
            j = np.random.randint(low=0, high=col)

            if self.is_tile_empty(position=(i, j)):
                self.update_tile(position=(i, j), is_infected=True, is_immune=False)
                spawned_infected_entity = True

    def add_healthy_entities(self) -> None:
        """Transform every other empty tile into a healthy entity."""
        row, col = self.shape
        for i in range(0, row, 1):
            for j in range(0, col, 1):
                if self.tiles[i][j] is None:
                    self.update_tile(position=(i, j), is_infected=False, is_immune=False)
