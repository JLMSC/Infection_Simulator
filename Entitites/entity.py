"""Base class for an entity, its properties, methods
and attributes should not be tampered with."""
from typing import List


class Entity:
    """Base class for an entity."""

    def __init__(self, position: List[int], is_infected: bool, is_immune: bool) -> None:
        self.position = position
        self.is_immune = is_immune
        self.is_infected = is_infected
        # It's representation in the world.
        self.symbol = 'O' if self.is_infected else '*'
        # TODO: Fazer algum sismeta pra ddizer se o infectado é sintomatico, assintomatico, grave e probabilidade de morte.


    def update_position(self, new_position: List[int]) -> None:
        """Update the current entity's position.

        Parameters
        ----------
        new_position : List[int]
            The new position."""
        self.position = new_position
