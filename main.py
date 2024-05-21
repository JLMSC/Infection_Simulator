from time import sleep


from World.world import World

world = World(shape=10)

step = 0
while len(world.get_infected_entities()) >= 1:
    # sleep(1)
    world.next_iteration()
    print(f'Step # {step} done.')
    step += 1

pass