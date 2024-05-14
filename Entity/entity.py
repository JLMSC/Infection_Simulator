"""File responsible for everything related to an entity."""
from typing import Tuple

from .entity_type import EntityType # pylint: disable=E0402


class Entity:
    """Represents an entity, both healthy or infected."""

    def __init__(self, position: Tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Initializes an entity at a specified position.

        Parameters
        ----------
        position : Tuple[int, int]
            The position where the entity spawned.
        is_infected : bool
            Defines if the entity is healthy or infected.
        is_immune : bool
            Declares if the entity is immune (will always be healthy).
        """
        self.position: Tuple[int, int] = position
        self.is_infected: bool = is_infected
        self.is_immune: bool = is_immune if not is_infected else False
        self.entity_type: EntityType = self.define_entity_type()

    def define_entity_type(self) -> EntityType:
        """Define the entity's type.

        Returns
        -------
        EntityType
            The entity's type (healthy or infected).
        """
        if not self.is_infected or self.is_immune:
            return EntityType.HEALTHY
        return EntityType.INFECTED

    def change_entity_type(self) -> None:
        """Change the entity's type."""
        if self.entity_type == EntityType.HEALTHY:
            self.entity_type = EntityType.HEALTHY
        else:
            self.entity_type = EntityType.INFECTED

    def update_position(self, new_position: Tuple[int, int]) -> None:
        """Updates the entity's position.

        Parameters
        ----------
        new_position : Tuple[int, int]
            The new entity's position.
        """
        self.position = new_position

    def get_infected(self) -> None:
        """Turn this entity into a infected entity if it's neither immune nor infected."""
        if not (self.is_immune or self.is_infected):
            self.change_entity_type()

    def infect_neighbors(self) -> None:
        # TODO: Not yet implemented.
        print("TODO: Not yet implemented")