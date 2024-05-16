"""Module responsible for manipulating world entity,
such as it's dimension and living entities."""
from functools import reduce
import numpy as np


from Entity.entity import Entity


class World:
    """Represents a world with random living entities."""

    def __init__(self, shape: int) -> None:
        self.shape: tuple[int, int] = (shape, shape)
        self.tiles: np.ndarray = np.empty(shape=self.shape, dtype=object)
        self.add_immune_entities()
        self.add_infected_entity()
        self.add_healthy_entities()
        # TODO: Move the infected entity to a random adjacent position. (they should not overlap, dead entities should not move.)
        # NOTE: "(i + 1 + N) % N" or "(i - 1 + N) % N" work for both rows and cols, just adjust the +1 or -1 if necessary.

        # TODO: New infected entities should inherit the property from the infected entity.
        # TODO: Entities heal after 20 steps if not dead (1 step per second) and turn into immune entities.
        # TODO: After every step, log the amount of sintomáticos, assintomáticos, curados e mortos.

    def update_tile(self, position: tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Spawn a new entity in a tile.

        Parameters
        ----------
        position : tuple[int, int]
            The tile where the entity will be spawned.
        is_infected : bool
            If the entity is infected.
        is_immune : bool
            If the entity is immune.
        """
        entity = Entity(position=position, is_infected=is_infected, is_immune=is_immune)
        self.tiles[position] = entity

    def get_random_tile(self) -> tuple[int, int]:
        """Randomly select a tile and return its position.

        Returns
        -------
        tuple[int, int]
            The random selected tile's position.
        """
        rows, cols = self.shape
        tile_x = np.random.randint(low=0, high=rows)
        tile_y = np.random.randint(low=0, high=cols)
        return tile_x, tile_y

    def is_tile_empty(self, position: tuple[int, int]) -> bool:
        """Check if a tile is an empty tile.

        Parameters
        ----------
        position : tuple[int, int]
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
        while immune_entities_amount > 0:
            tile_x, tile_y = self.get_random_tile()

            if self.is_tile_empty(position=(tile_x, tile_y)):
                self.update_tile(position=(tile_x, tile_y), is_infected=False, is_immune=True)
                immune_entities_amount -= 1

    def get_immune_entities(self) -> tuple:
        """Get the position of every infected entity.

        Returns
        -------
        tuple
            The position of every infected entity.
        """
        # Temporary dummy target to search for in world's tiles.
        dummy_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
        # Temporary array with same entity type as the dummy target.
        mask = np.array(object=[[entity.entity_type == dummy_entity_type for entity in row] for row in self.tiles])
        # Returns the location of those matching entities type.
        return np.where(mask)


    def add_infected_entity(self) -> None:
        """Transform one random entity into a infected entity."""
        spawned_infected_entity = False
        while not spawned_infected_entity:
            tile_x, tile_y = self.get_random_tile()

            if self.is_tile_empty(position=(tile_x, tile_y)):
                self.update_tile(position=(tile_x, tile_y), is_infected=True, is_immune=False)
                spawned_infected_entity = True

    def add_healthy_entities(self) -> None:
        """Transform every other empty tile into a healthy entity."""
        row, col = self.shape
        for tile_x in range(0, row, 1):
            for tile_y in range(0, col, 1):
                if self.is_tile_empty(position=(tile_x, tile_y)):
                    self.update_tile(position=(tile_x, tile_y), is_infected=False, is_immune=False)
