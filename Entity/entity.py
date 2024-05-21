"""File responsible for everything related to an entity."""
from typing import Callable, Any
import numpy as np


# pylint: disable=E0402
from .entity_type import EntityType


def ensure_alive(func) -> Callable[..., Any]:
    """Custom decorator to check if an entity is alive."""
    def wrapper(self, *args, **kwargs) -> Any:
        if getattr(self, '__is_alive', True):
            return func(self, *args, **kwargs)
    return wrapper


class Entity:
    """Represents an entity, both healthy or infected."""

    is_alive: bool = True
    life_span: int = 0

    # Available symptoms for this entity.
    __death: str = 'MORTE'
    __severe: str = 'GRAVE'
    __symptomatic: str = 'SINTOMÁTICO'
    __asymptomatic: str = 'ASSINTOMÁTICO'
    symptoms: list = [__symptomatic, __asymptomatic, __severe, __death]


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
        self.symptom: str = self.get_symptom()

    @ensure_alive
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

    @ensure_alive
    def change_entity_type(self) -> None:
        """Change the entity's type."""
        if self.entity_type == EntityType.HEALTHY:
            self.entity_type = EntityType.INFECTED
        else:
            self.entity_type = EntityType.HEALTHY

    @ensure_alive
    def move_randomly(self, world_size: int) -> None:
        """Randomly move this entity to an adjacent position."""
        adjacent_offsets = ((1, 0), (-1, 0), (0, -1), (0, 1))
        selected_offset = adjacent_offsets[int(np.random.randint(low=0, high=len(adjacent_offsets)))]
        next_position_x = (selected_offset[0] + self.position[0] + world_size) % world_size
        next_position_y = (selected_offset[1] + self.position[1] + world_size) % world_size
        self.update_position(new_position=(next_position_x, next_position_y))

    @ensure_alive
    def update_position(self, new_position: tuple[int, int]) -> None:
        """Updates the entity's position.

        Parameters
        ----------
        new_position : tuple[int, int]
            The new entity's position.
        """
        self.position = new_position

    @ensure_alive
    def get_symptom(self) -> str | None:
        """Defines the symptoms for an infected entity."""
        if self.is_infected:
            probabilities = [0.20, 0.20, 0.02, 0.0119]
            # Normalize the probabilities, making the sum up to 1 (or 100%).
            probs_normalized = [prob / sum(probabilities) for prob in probabilities]
            current_symptom = np.random.choice(a=self.symptoms, p=probs_normalized)
            if Entity.is_death(symptom=current_symptom):
                self.die()
            return current_symptom
        return None # This should not happen.

    @ensure_alive
    def get_infected(self) -> None:
        """Turn this entity into a infected entity if it's neither immune nor infected nor dead."""
        if not (self.is_immune or self.is_infected):
            self.is_infected = True
            self.change_entity_type()
            self.symptom = self.get_symptom()

    @ensure_alive
    def get_healed(self) -> None:
        """Heals this entity and make it immune."""
        if self.is_infected:
            self.entity_type = EntityType.HEALED
            self.is_immune = True

    @ensure_alive
    def can_live(self) -> None:
        """Checks if this entity can live to see another day."""
        if Entity.is_severe(symptom=self.symptom):
            if np.random.random() > 0.2: # 80% chance of death.
                self.die()

    @ensure_alive
    def increase_life_span(self) -> None:
        """Increase this entity's life span."""
        if self.is_infected:
            if self.life_span >= 20:
                self.get_healed()
            self.life_span += 1

    @ensure_alive
    def die(self) -> None:
        """Instant death."""
        self.is_alive = False
        self.entity_type = EntityType.DEAD

    @staticmethod
    def is_death(symptom: str) -> bool:
        """Check if a symptom is death."""
        return symptom == Entity.__death

    @staticmethod
    def is_severe(symptom: str) -> bool:
        """Check if a symptom is severe."""
        return symptom == Entity.__severe

    @staticmethod
    def is_symptomatic(symptom: str) -> bool:
        """Check if a symptom is symptomatic."""
        return symptom == Entity.__symptomatic

    @staticmethod
    def is_asymptomatic(symptom: str) -> bool:
        """Check if a symptom is asymptomatic."""
        return symptom == Entity.__asymptomatic
