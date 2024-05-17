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
        self.clear_state()
        self.add_immune_entities()
        self.add_infected_entity()
        self.add_healthy_entities()
        self.save_state()

        # TODO: Move the infected entity to a random adjacent position. (they should not overlap, dead entities should not move.)
        # NOTE: "(i + 1 + N) % N" or "(i - 1 + N) % N" work for both rows and cols, just adjust the +1 or -1 if necessary.

        # TODO: New infected entities should inherit the property from the infected entity.
        # TODO: Entities heal after 20 steps if not dead (1 step per second) and turn into immune entities.
        # TODO: After every step, log the amount of sintomáticos, assintomáticos, curados e mortos.

    def next_iteration(self) -> None:
        """Step into the next world iteration."""
        infected_entities_positions = self.get_infected_entities()
        for position in infected_entities_positions:
            infected_entity = self.get_tile(position=position)
            self.infect_neighbors(infected_entity)
        self.save_state()

    def save_state(self) -> None:
        """Saves the current world state in 'world_state.txt'."""
        rows, cols = self.shape
        with open(file='world_state.txt', mode='a', encoding='utf-8') as file:
            file.write('=' * 20 + '\n')
            for i in range(rows):
                for j in range(cols):
                    entity_repr = self.get_tile(position=(i, j)).entity_type.value
                    file.write(f'{entity_repr} ')
                file.write('\n')
            file.write('=' * 20 + '\n')
            file.write('\n' * 3)
            file.close()
            # TODO: Add more info at the end. (infected, healthy, immune count etc.)

    def clear_state(self) -> None:
        """Clears every info in 'world_state.txt'."""
        with open(file='world_state.txt', mode='w', encoding='utf-8') as file:
            file.close()

    def get_world_size(self) -> int:
        """Get the world size.

        Returns
        -------
        int
            The world size.
        """
        return np.random.choice(a=self.shape)

    def get_tile(self, position: tuple[int, int]) -> Entity:
        """Get the content at a specified tile by its position.

        Parameters
        ----------
        position : tuple[int, int]
            The tile's position.

        Returns
        -------
        Entity
            The content of the selected tile.
        """
        return self.tiles[position]

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

    def get_infected_entities(self) -> tuple[tuple[int, int], ...]:
        """Get the position of every infected entity.

        Returns
        -------
        tuple[tuple[int, int], ...]
            The position of every infected entity.
        """
        # Temporary dummy target to search for in world's tiles.
        dummy_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
        # Temporary array with same entity type as the dummy target.
        mask = np.array(object=[[entity.entity_type == dummy_entity_type for entity in row] for row in self.tiles])
        # Returns the location of those matching entities type.
        indexes = np.where(mask)
        return tuple(zip(indexes[0], indexes[1]))

    def add_infected_entity(self) -> None:
        """Transform one random entity into a infected entity."""
        spawned_infected_entity = False
        while not spawned_infected_entity:
            tile_x, tile_y = self.get_random_tile()

            if self.is_tile_empty(position=(tile_x, tile_y)):
                self.update_tile(position=(tile_x, tile_y), is_infected=True, is_immune=False)
                spawned_infected_entity = True

    def infect_neighbors(self, infected_entity: Entity) -> None:
        """Tries to infect every adjacent entity.

        Parameters
        ----------
        infected_entity : Entity
            The infected entity that'll try to infect its adjacents.
        """
        def calculate_position(entity_position: tuple[int, int], offset: tuple[int, int], world_size: int) -> tuple[int, int]:
            """Calculates the entity's position plus offest in a circular world.

            Parameters
            ----------
            entity_postion : tuple[int, int]
                The entity's position.
            offset : tuple[int, int]
                The position's offset.
            world_size : int
                The world size.

            Returns
            -------
            tuple[int, int]
                The entity's position plus the offset.
            """
            position_x = (offset[0] + entity_position[0] + world_size) % world_size
            position_y = (offset[1] + entity_position[1] + world_size) % world_size
            return position_x, position_y

        # Infect every adjacent entity.
        adjacent_offsets = ((1, 0), (-1, 0), (0, -1), (0, 1))
        for offset in adjacent_offsets:
            adjacent_position = calculate_position(entity_position=infected_entity.position, offset=offset, world_size=self.get_world_size())
            adjacent_entity = self.get_tile(position=adjacent_position)
            adjacent_entity.get_infected()

    def add_healthy_entities(self) -> None:
        """Transform every other empty tile into a healthy entity."""
        row, col = self.shape
        for tile_x in range(0, row, 1):
            for tile_y in range(0, col, 1):
                if self.is_tile_empty(position=(tile_x, tile_y)):
                    self.update_tile(position=(tile_x, tile_y), is_infected=False, is_immune=False)
