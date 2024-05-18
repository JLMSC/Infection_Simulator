"""File responsible for everything related to an entity."""
import numpy as np


# pylint: disable=E0402
from .entity_type import EntityType


# TODO: Add variable to count the amount of steps alive.
class Entity:
    """Represents an entity, both healthy or infected."""

    def __init__(self, position: tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Initializes an entity at a specified position.

        Parameters
        ----------
        position : tuple[int, int]
            The position where the entity spawned.
        is_infected : bool
            Defines if the entity is healthy or infected.
        is_immune : bool
            Declares if the entity is immune (will always be healthy).
        """
        self.position: tuple[int, int] = position
        self.is_infected: bool = is_infected
        self.is_immune: bool = is_immune if not is_infected else False
        self.entity_type: EntityType = self.define_entity_type()
        self.get_symptoms()

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
            self.entity_type = EntityType.INFECTED
        else:
            self.entity_type = EntityType.HEALTHY

    def move_randomly(self, world_size: int) -> None:
        """Randomly move this entity to an adjacent position."""
        adjacent_offsets = ((1, 0), (-1, 0), (0, -1), (0, 1))
        selected_offset = adjacent_offsets[int(np.random.randint(low=0, high=len(adjacent_offsets)))]
        next_position_x = (selected_offset[0] + self.position[0] + world_size) % world_size
        next_position_y = (selected_offset[1] + self.position[1] + world_size) % world_size
        self.update_position(new_position=(next_position_x, next_position_y))

    def update_position(self, new_position: tuple[int, int]) -> None:
        """Updates the entity's position.

        Parameters
        ----------
        new_position : tuple[int, int]
            The new entity's position.
        """
        self.position = new_position

    def get_symptoms(self) -> None:
        """Defines the symptoms for an infected entity."""
        if self.is_infected:
            symptoms = ['SINTOMATICO', 'ASSINTOMATICO', 'GRAVE', 'MORTE']
            probabilities = [0.20, 0.20, 0.02, 0.0119]
            # Normalize the probabilities, making the sum up to 1 (or 100%).
            probs_normalized = [prob / sum(probabilities) for prob in probabilities]
            self.symptom = np.random.choice(a=symptoms, p=probs_normalized)

    def get_infected(self) -> None:
        """Turn this entity into a infected entity if it's neither immune nor infected."""
        if not (self.is_immune or self.is_infected):
            self.is_infected = True
            self.change_entity_type()
            self.get_symptoms()
