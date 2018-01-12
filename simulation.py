from RoadSection import RoadSection
import numpy as np
from traffic import calcGap, lane_change, nasch, generate_cars, remove_old_cars, get_car_updates, update_cars
import copy

# TODO: remove
# Global vars
speed_changes = {}
auto = 1
vmax = 5
pv = 0.2
vback = -1
pc = 1


class Simulation:
    def __init__(self, start_road, rest_roads, step):
        self.start_road = start_road
        self.roads = [start_road, *rest_roads] # Pack into one list
        self.step = step

    def run(self):
        for i in range(self.step):
            roads_steps = {}

            for j in range(len(self.roads)):
                road_section = self.roads[j]
                grid = road_section.grid
                cars = road_section.cars
                updates = {}
                grid_temp = copy.deepcopy(grid)

                # Generates the updates for all cars
                get_car_updates(cars, grid, grid_temp, updates)

                # Update cars
                update_cars(cars, updates)

                # Generate auto only works for 1 car
                # Only generate cars in the start section
                if j == 0:
                    generate_cars(cars, grid)

                if i % 100 == 0 and i > 0:
                    remove_old_cars(cars, grid)

                # If we want to animate the simulation, yield the grid for every step
                roads_steps[j] = (grid, cars)

            yield roads_steps


def simulate(config):
    rows = config['rows']
    columns = config['columns']
    step = config['step']

    grid = np.full((rows, columns),  -1, dtype=np.int32)
    cars = {}
    # cars = {
    # 0 : Car(5, 1, 1, (0,2)),
    # 1 : Car(5, 1, 1, (2,2)),
    # 2 : Car(2, 1, 1, (0,4)),
    # 3 : Car(2, 1, 1, (2,4))
    # }
    # grid = np.array([[-1,-1,0,-1,2,-1,-1,-1,-1,-1],
    #         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    #         [-1,-1,1,-1,3,-1,-1,-1,-1,-1]])

    for i in range(step):
        updates = {}
        gridTemp = copy.deepcopy(grid)

        get_car_updates(cars, grid, gridTemp, updates)

        # Update cars
        update_cars(cars, updates)

        # Generate auto only works for 1 car
        generate_cars(cars, grid)

        if i % 100 == 0 and i > 0:
            remove_old_cars(cars, grid)

        # If we want to animate the simulation, yield the grid for every step
        yield grid, cars


r1 = RoadSection(2, 10)
r2 = RoadSection(5, 10)

outputMap = {
    1: 5  # Lane 1 corresponds with lane 5.
}

r1.set_output_mapping(r2, outputMap)

simulation = Simulation(r1, [r2], 100)
result = simulation.run()
[print(r) for r in result]
