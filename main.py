from time import sleep


from Entity.entity import Entity
from World.world import World

world = World(shape=10)

step = 0
target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
while len(world.get_matching_entity_type_positions(target_entity_type=target_entity_type)) >= 1:
    # sleep(1)
    world.next_iteration()
    print(f'Step # {step} done.')
    step += 1

pass