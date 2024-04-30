"""Module responsible for manipulating world entity,
such as it's dimension and living entities."""
from typing import Tuple, List
import numpy as np
from functools import reduce
from operator import mul
from math import ceil

from Entitites.healthy_entity import HealthyEntity
from Entitites.infected_entity import InfectedEntity


class World:
    """Represents a world with NxN dimensions and
    random living entities."""

    def __init__(self, shape: Tuple[int, int]) -> None:
        # TODO: Change shape to N because it's NxN.
        self.shape = shape
        # Tilde '~' are treated as empty tiles.
        self.tiles = np.chararray(shape=self.shape)
        self.tiles[:] = '~'
        # Every living entity in the world, infected, healthy and immune.
        self.infected_entities = []
        self.healthy_entities = []


    # TODO: Preciso ter algo assim pros infectados pegar os adjacentes.
    # def get_entity_at_tile(self, position) -> Entity:
    #     return entity at position


    def add_infected_entity(self) -> None:
        """Add one infected entity in the world
        at a random tile."""
        quantity = 1

        # TODO: Implement this.
        pass


    def add_healthy_entities(self) -> None:
        """Add one or multiple healthy entities in the
        world at random tiles."""
        # Change world format to 1xN^2 (its easier to manipulate it.)
        self.tiles = self.tiles.flatten(order='C')
        # The amount of empty tiles.
        population = self.tiles.shape[0]
        # Only 5% of the population should be immune.
        quantity_of_immune_entities = ceil(population * 0.5)
        # And the remaining ones are healthy, but at least one should be infected.
        quantity_of_healthy_entities = (population - quantity_of_immune_entities) - 1
        self.tiles[:quantity_of_healthy_entities] = '*'

        self.healthy_entities



