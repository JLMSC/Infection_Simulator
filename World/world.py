"""Module responsible for manipulating world entity,
such as it's dimension and living entities."""
from functools import reduce
import numpy as np


from Entity.entity import Entity


class World:
    """Represents a world with random living entities."""

    iteration_step: int = 0

    def __init__(self, shape: int) -> None:
        self.shape: tuple[int, int] = (shape, shape)
        self.tiles: np.ndarray = np.empty(shape=self.shape, dtype=object)
        self.add_immune_entities()
        self.add_infected_entity()
        self.add_healthy_entities()
        self.create_data_file()

    def next_iteration(self) -> None:
        """Step into the next world iteration."""
        self.save_state()
        target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
        infected_entities_positions = self.get_matching_entity_type_positions(target_entity_type=target_entity_type)
        del target_entity_type
        for position in infected_entities_positions:
            infected_entity = self.get_tile(position=position)
            infected_entity.increase_life_span()
            self.infect_neighbors(infected_entity=infected_entity)
            self.move_infected_entity(infected_entity=infected_entity)
            del infected_entity
        del infected_entities_positions
        self.iteration_step += 1

    def create_data_file(self) -> None:
        """Creates an .csv data file for this world with only the headers."""
        with open(file='world_data.csv', mode='w', encoding='utf-8') as file:
            # 'Iteration' -> The iteration number.
            # 'Infected' -> The amount of infected entities.
            # 'Healed' -> The amount of healed entities.
            # 'Immune' -> The amount of immune entities.
            # 'Healthy' -> The amount of healthy entities.
            # 'Symptomatic' -> The amount of symptomatic entities.
            # 'Asymptomatic' -> The amount of asymptomatic entities.
            # 'Severe' -> The amount of severe mortality status.
            # 'Normal' -> The amount of normal mortality status.
            # 'Dead' -> The amount of dead entities.
            file.write('Iteration,Infected,Healed,Immune,Healthy,Symptomatic,Asymptomatic,Severe,Normal,Dead\n')
            file.close()

    def save_state(self) -> None:
        """Saves the current world state in 'world_state.txt'."""
        with open(file='world_data.csv', mode='a', encoding='utf-8') as file:
            # Current iteration.
            file.write(f'{self.iteration_step},')
            # Infected entity count.
            infected_target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
            infected_count = len(self.get_matching_entity_type_positions(target_entity_type=infected_target_entity_type))
            file.write(f'{infected_count},')
            del infected_target_entity_type, infected_count
            # Healed entity count.
            healed_target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False)
            healed_target_entity_type.heal()
            healed_target_entity_type = healed_target_entity_type.entity_type
            healed_count = len(self.get_matching_entity_type_positions(target_entity_type=healed_target_entity_type))
            file.write(f'{healed_count},',)
            # Immune entity count.
            immune_target_entity_type = Entity(position=(-1, -1), is_infected=False, is_immune=True).entity_type
            immune_count = len(self.get_matching_entity_type_positions(target_entity_type=immune_target_entity_type))
            file.write(f'{immune_count+healed_count},')
            # Healthy entity count.
            healthy_target_entity_type = Entity(position=(-1, -1), is_infected=False, is_immune=False).entity_type
            healthy_count = len(self.get_matching_entity_type_positions(target_entity_type=healthy_target_entity_type))
            file.write(f'{healthy_count+immune_count+healed_count},')
            del healthy_target_entity_type, healthy_count, immune_target_entity_type, immune_count, healed_target_entity_type, healed_count
            # Symptomatic status count.
            file.write(f'{self.count_symptom_status(target_symptom_status="SINTOMÁTICO")},')
            # Asymptomatic status count.
            file.write(f'{self.count_symptom_status(target_symptom_status="ASSINTOMÁTICO")},')
            # Severe status count.
            file.write(f'{self.count_mortality_status(target_mortality_status="GRAVE")},')
            # Normal status count.
            file.write(f'{self.count_mortality_status(target_mortality_status="NORMAL")},')
            # Dead status count.
            dead_target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False)
            dead_target_entity_type.die()
            dead_target_entity_type = dead_target_entity_type.entity_type
            dead_count = len(self.get_matching_entity_type_positions(target_entity_type=dead_target_entity_type))
            file.write(f'{dead_count}\n')
            del dead_target_entity_type, dead_count
            # Close the file.
            file.close()

        # Use this code if you want to see the representation of the world every iteration. (creates a new file)
        # rows, cols = self.shape
        # with open(file='world_state.txt', mode='a', encoding='utf-8') as file:
        #     file.write('=' * 20 + '\n')
        #     for i in range(rows):
        #         for j in range(cols):
        #             entity_repr = self.get_tile(position=(i, j)).entity_type.value
        #             file.write(f'{entity_repr} ')
        #         file.write('\n')
        #     file.write('=' * 20 + '\n')
        #     file.write(f'Casos sintomáticos: {self.count_symptom_status(target_symptom_status="SINTOMÁTICO")}\n')
        #     file.write(f'Casos assintomáticos: {self.count_symptom_status(target_symptom_status="ASSINTOMÁTICO")}\n')
        #     file.write(f'Casos graves: {self.count_mortality_status(target_mortality_status="GRAVE")}\n')
        #     file.write(f'Mortes: {self.count_survival_status(target_survival_status="MORTE")}\n')
        #     # file.write(f'Curados: {self.count_heals()}\n')
        #     file.write('=' * 20 + '\n' * 3)
        #     file.close()

    def get_world_size(self) -> int:
        """Get the world size."""
        return np.random.choice(a=self.shape)

    def get_tile(self, position: tuple[int, int]) -> Entity:
        """Get the content at a specified tile by its position."""
        return self.tiles[position]

    def swap_tiles(self, old_pos: tuple[int, int], new_pos: tuple[int, int]) -> None:
        """Swap the information between two tiles in this world."""
        self.tiles[new_pos], self.tiles[old_pos] = self.tiles[old_pos], self.tiles[new_pos]

    def update_tile(self, position: tuple[int, int], is_infected: bool, is_immune: bool) -> None:
        """Spawn a new entity in a tile."""
        self.tiles[position] = Entity(position=position, is_infected=is_infected, is_immune=is_immune)

    def get_random_tile(self) -> tuple[int, int]:
        """Randomly select a tile and return its position."""
        rows, cols = self.shape
        tile_x = np.random.randint(low=0, high=rows)
        tile_y = np.random.randint(low=0, high=cols)
        del rows, cols
        return tile_x, tile_y

    def is_tile_empty(self, position: tuple[int, int]) -> bool:
        """Check if a tile at position is an empty tile."""
        return self.tiles[position] is None

    def count_symptom_status(self, target_symptom_status: str) -> int:
        """Count the amount of a target symptom status for every infected entity in the world."""
        mask = np.array(object=[[Entity.is_equal(entity_status=entity.current_symptom_status, target_status=target_symptom_status) and entity.is_infected for entity in row] for row in self.tiles])
        indexes = np.where(mask)
        count = len(tuple(zip(indexes[0], indexes[1])))
        del mask, indexes
        return count

    def count_mortality_status(self, target_mortality_status: str) -> int:
        """Count the amount of a target mortality status for every infected entity in the world."""
        mask = np.array(object=[[Entity.is_equal(entity_status=entity.current_mortality_status, target_status=target_mortality_status) and entity.is_infected for entity in row] for row in self.tiles])
        indexes = np.where(mask)
        count = len(tuple(zip(indexes[0], indexes[1])))
        del mask, indexes
        return count

    def count_survival_status(self, target_survival_status: str) -> int:
        """Count the amount of a target survival status for every infected entity in the world."""
        mask = np.array(object=[[Entity.is_equal(entity_status=entity.current_survival_status, target_status=target_survival_status) and entity.is_infected for entity in row] for row in self.tiles])
        indexes = np.where(mask)
        count = len(tuple(zip(indexes[0], indexes[1])))
        del mask, indexes
        return count

    def add_immune_entities(self) -> None:
        """Transform 5% of population into immune healthy entities."""
        immune_entities_amount = int(np.round((reduce(np.multiply, self.shape) - 1) * 0.05))
        while immune_entities_amount > 0:
            tile_x, tile_y = self.get_random_tile()
            if self.is_tile_empty(position=(tile_x, tile_y)):
                self.update_tile(position=(tile_x, tile_y), is_infected=False, is_immune=True)
                immune_entities_amount -= 1
            del tile_x, tile_y
        del immune_entities_amount

    def get_matching_entity_type_positions(self, target_entity_type: object) -> tuple[tuple[int, int], ...]:
        """Get the position of every matching entity type in this world."""
        mask = np.array(object=[[entity.entity_type == target_entity_type for entity in row] for row in self.tiles])
        indexes = np.where(mask)
        positions = tuple(zip(indexes[0], indexes[1]))
        del mask, indexes
        return positions

    def add_infected_entity(self) -> None:
        """Transform one random entity into a infected entity."""
        spawned_infected_entity = False
        while not spawned_infected_entity:
            tile_x, tile_y = self.get_random_tile()
            if self.is_tile_empty(position=(tile_x, tile_y)):
                self.update_tile(position=(tile_x, tile_y), is_infected=True, is_immune=False)
                spawned_infected_entity = True
            del tile_x, tile_y
        del spawned_infected_entity

    def move_infected_entity(self, infected_entity: Entity) -> None:
        """Randomly move an specified infected entity."""
        old_pos = infected_entity.position
        infected_entity.move_randomly(world_size=self.get_world_size())
        new_pos = infected_entity.position
        self.swap_tiles(old_pos=old_pos, new_pos=new_pos)
        del old_pos, new_pos

    def infect_neighbors(self, infected_entity: Entity) -> None:
        """Tries to infect every entity adjacent to a specified infected entity."""
        def calculate_position(entity_position: tuple[int, int], offset: tuple[int, int], world_size: int) -> tuple[int, int]:
            """Calculates the entity's position plus offest in a circular world."""
            position_x = (offset[0] + entity_position[0] + world_size) % world_size
            position_y = (offset[1] + entity_position[1] + world_size) % world_size
            return position_x, position_y

        # Infect every adjacent entity.
        adjacent_offsets = ((1, 0), (-1, 0), (0, -1), (0, 1))
        for offset in adjacent_offsets:
            adjacent_position = calculate_position(entity_position=infected_entity.position, offset=offset, world_size=self.get_world_size())
            adjacent_entity = self.get_tile(position=adjacent_position)
            adjacent_entity.get_infected()
            del adjacent_position, adjacent_entity
        del adjacent_offsets

    def add_healthy_entities(self) -> None:
        """Transform every other empty tile into a healthy entity."""
        row, col = self.shape
        for tile_x in range(0, row, 1):
            for tile_y in range(0, col, 1):
                if self.is_tile_empty(position=(tile_x, tile_y)):
                    self.update_tile(position=(tile_x, tile_y), is_infected=False, is_immune=False)
            del tile_x, tile_y
        del row, col
