from typing import List
from entity import Entity

class InfectedEntity(Entity):
    def __init__(self, position: List[int]) -> None:
        super().__init__(position=position, is_infected=True, is_immune=False)


    def infect_neighbors(self) -> None:
        # TODO: Not yet implemented.
        pass
