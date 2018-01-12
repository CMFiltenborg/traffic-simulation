from RoadSection import RoadSection
import numpy as np
from traffic import calcGap, laneChange, nasch, generate_cars, remove_old_cars
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
                speed_changes = {}

                grid_temp = copy.deepcopy(grid)

                self.determine_car_updates(grid, grid_temp, cars)
                # Update car speeds
                for x, y in speed_changes.items():
                    cars[x].speed_changes(y)

                # Generate auto only works for 1 car
                # Only generate cars in the start section
                if j == 0:
                    generate_cars(cars, grid)

                if i % 100 == 0 and i > 0:
                    remove_old_cars(cars, grid)

                # If we want to animate the simulation, yield the grid for every step
                roads_steps[j] = (grid, cars)

            yield roads_steps

    @staticmethod
    def determine_car_updates(grid, grid_temp, cars):
        coordinates = np.where(grid != -1)
        for j in range(len(coordinates[0])):
            r = coordinates[0][j]
            c = coordinates[1][j]
            v = cars[grid[r][c]].speed
            vh = min(v + 1, vmax)

            gap = calcGap(r, c, grid_temp, 1, cars)

            if vh > gap:
                laneChange(r, c, v, grid_temp, gap, vh, cars, grid)
            else:
                nasch(r, c, v, gap, grid)


def simulate(config):
    rows = config['rows']
    columns = config['columns']
    step = config['step']

    grid = np.full((rows, columns),  -1, dtype=np.int32)
    cars = {}
    for i in range(step):
        speed_changes = {}
        coordinates = np.where(grid != -1)
        gridTemp = copy.deepcopy(grid)
        for j in range(len(coordinates[0])):
            r = coordinates[0][j]
            c = coordinates[1][j]
            v = cars[grid[r][c]].speed
            vh = min(v+1, vmax)

            gap = calcGap(r, c, gridTemp, 1, cars)

            if vh > gap:
                laneChange(r, c, v, gridTemp, gap, vh, cars, grid)
            else:
                nasch(r, c, v, gap, grid)

        # Update car speeds
        for x, y in speed_changes.items():
            cars[x].speed_changes(y)

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
