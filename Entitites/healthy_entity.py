from typing import List
from entity import Entity


class HealthyEntity(Entity):
    def __init__(self, position: List[int], is_immune: bool) -> None:
        super().__init__(position=position, is_infected=False, is_immune=is_immune)


    def get_infected(self) -> None:
        """Turn this entity into a infected entity if it's not immune."""
        if not self.is_immune:
            self.is_infected = True
            self.symbol = 'O'
