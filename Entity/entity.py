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

    # If this entity is currently alive.
    is_alive: bool = True

    # How long this entity lasted.
    life_span: int = 0

    # The maximum span an entity will be infected.
    infection_duration: int = 20

    # Everything related to the survivability of this entity.
    all_survival_status: list = ['VIDA', 'MORTE']
    survival_probability: list = [0.9881, 0.0119] # 1,19% of 'MORTE' (death).
    current_survival_status: str = '' # The current survival status of this entity.

    # Everything related to the mortality status of this entity.
    all_mortalities_status: list = ['NORMAL', 'GRAVE']
    mortalities_probability: list = [0.98, 0.02] # 2% of 'GRAVE' (severe).
    current_mortality_status: str = '' # The current mortality status of this entity.

    # Everything related to the symptom status of this entity.
    all_symptoms_status: list = ['ASSINTOMÁTICO', 'SINTOMÁTICO']
    symptoms_probability: list = [0.8, 0.2] # 20% of 'SINTOMÁTICO'. (symptomatic)
    current_symptom_status: str = '' # The current symptom status of this entity.


    def __init__(self, position: tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Initializes an entity at a specified position.

        Parameters
        ----------
        position : tuple[int, int]
            The position where the entity is.
        is_infected : bool
            If this entity is infected or not.
        is_immune : bool
            If this entity is immune or not.
        """
        self.position: tuple[int, int] = position
        self.is_infected: bool = is_infected if not is_immune else False
        self.is_immune: bool = is_immune if not is_infected else False
        self.entity_type: EntityType = self.define_entity_type()
        self.define_infected_entity_status()

    @ensure_alive
    def define_entity_type(self) -> EntityType:
        """Define the current entity type based if it is infected or immune."""
        if self.is_immune:
            return EntityType.IMMUNE
        if not self.is_infected:
            return EntityType.HEALTHY
        return EntityType.INFECTED

    @ensure_alive
    def define_infected_entity_status(self) -> None:
        """Define the symptom status for an infected entity."""
        if self.is_infected:
            self.current_symptom_status = self.get_symptom_status()
            # If 'SINTOMÁTICO', check the mortality status of this entity.
            if Entity.is_equal(entity_status=self.current_symptom_status, target_status='SINTOMÁTICO'):
                self.current_mortality_status = self.get_mortality_status()
                # If 'GRAVE', check if this entity can live.
                if Entity.is_equal(entity_status=self.current_mortality_status, target_status='GRAVE'):
                    self.current_survival_status = self.get_survival_status()
                    # If 'MORTE', this entity dies.
                    if Entity.is_equal(entity_status=self.current_survival_status, target_status='MORTE'):
                        self.die()

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
        del adjacent_offsets, selected_offset
        self.update_position(new_position=(next_position_x, next_position_y))

    @ensure_alive
    def update_position(self, new_position: tuple[int, int]) -> None:
        """Updates the entity's position to a new position."""
        self.position = new_position

    @ensure_alive
    def get_symptom_status(self) -> str:
        """Randomly choose the symptom status for this entity."""
        return np.random.choice(a=self.all_symptoms_status, p=self.symptoms_probability)

    @ensure_alive
    def get_mortality_status(self) -> str:
        """Randomly choose the mortality status for this entity."""
        return np.random.choice(a=self.all_mortalities_status, p=self.mortalities_probability)

    @ensure_alive
    def get_survival_status(self) -> None:
        """Randomly choose the survival status for this entity."""
        return np.random.choice(a=self.all_survival_status, p=self.survival_probability)

    @ensure_alive
    def get_infected(self) -> None:
        """Turn this entity into a infected entity if it's neither immune nor infected nor dead."""
        if not (self.is_immune or self.is_infected):
            self.is_infected = True
            self.change_entity_type()
            self.define_infected_entity_status()

    @ensure_alive
    def increase_life_span(self) -> None:
        """Increase this entity life span, if alive for long enough it'll be healed and become immune."""
        if self.is_infected:
            if self.life_span >= self.infection_duration:
                self.heal()
            self.life_span += 1

    @ensure_alive
    def die(self) -> None:
        """This entity die."""
        self.is_alive = False
        self.entity_type = EntityType.DEAD

    def heal(self) -> None:
        """This entity heals and become immune."""
        self.is_infected = False
        self.is_immune = True
        self.entity_type = EntityType.HEALED

    @staticmethod
    def is_equal(entity_status: str, target_status: str) -> bool:
        """Check if any entity's status is equal to a specific status."""
        return entity_status == target_status
