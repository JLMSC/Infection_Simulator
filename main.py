import matplotlib.pyplot as plt

from Entity.entity import Entity
from World.world import World

world = World(shape=500)

step = 0
target_entity_type = Entity(position=(-1, -1), is_infected=True, is_immune=False).entity_type
while len(world.get_matching_entity_type_positions(target_entity_type=target_entity_type)) >= 1:
    # Shows, in real-time, at every iteration the world state.
    # world.show_current_iteration_world_state()
    world.next_iteration()

    print(f'Step # {step} done.')
    step += 1

# Assures that the last plot will not be closed automatically.
plt.show()

pass