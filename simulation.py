from RoadSection import RoadSection
import numpy as np

from car import Car
from traffic import calc_gap, remove_old_cars, print_grid
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
        self.generated_cars = 0

    def run(self):
        for i in range(self.step):
            roads_steps = {}

            for j in range(len(self.roads)):
                road_section = self.roads[j]
                grid = road_section.grid
                cars = road_section.cars

                # grid_temp = copy.deepcopy(grid)
                road_section.set_temp_grid()
                road_section.updates = {}

                # Generates the updates for all cars
                get_car_updates(road_section)

                # Update cars
                update_cars(road_section)
                road_section.add_new_cars()

                # Generate auto only works for 1 car
                # Only generate cars in the start section
                if j == 0:
                    self.generate_cars(cars, grid)

                if i % 100 == 0 and i > 0:
                    remove_old_cars(cars, grid)

                # If we want to animate the simulation, yield the grid for every step
                print_grid((grid, cars))
                roads_steps[j] = (grid, cars)

            yield roads_steps

    def generate_cars(self, cars, grid):
        rows = grid.shape[0]
        for i in range(rows):
            if i == 4:
                if np.random.random() < 0.5:
                    v = np.random.randint(3, 5)
                    new_car_index = self.generated_cars
                    self.generated_cars += 1
                    d = np.random.randint(2,4)
                    if d == 3:
                        color = 'black'
                    else:
                        color = 'r'
                    cars[new_car_index] = Car(new_car_index, v, color, d, (i,0))
                    grid[i][0] = new_car_index
                break

            #ps = 1 / float(rows+2) * (i + 1)
            ps = 1
            if np.random.random() < ps:
                if i == 0:
                    v = 5
                elif i == 1:
                    if np.random.random() < 0.75:
                        v = 5
                    else:
                        v = 4
                elif i == 2:
                    if np.random.random() < 0.65:
                        v = 5
                    else:
                        v = 4
                elif i == 3:
                    if np.random.random() < 0.55:
                        v = 5
                    else:
                        v = 4
                new_car_index = self.generated_cars
                self.generated_cars += 1
                d = np.random.randint(2,4)
                if d == 3:
                    color = 'black'
                else:
                    color = 'r'
                cars[new_car_index] = Car(new_car_index, v, color, d, (i,0))
                grid[i][0] = new_car_index



def update_cars(road_section):
    cars = road_section.cars
    for x, y in road_section.updates.items():
        cars[x].set_speed(y[0])
        cars[x].set_position(y[1])


def get_car_updates(road_section):
    coordinates = road_section.get_car_coordinates()
    cars = road_section.cars
    for j in range(len(coordinates[0])):
        row = coordinates[0][j]
        column = coordinates[1][j]
        car = cars[road_section.grid_temp[row][column]]

        move_car(car, road_section)


def move_car(car, road_section):
    cars = road_section.cars
    grid_temp = road_section.grid_temp

    gap = calc_gap(car.position[0], car.position[1], grid_temp, 1, cars)
    do_lane_change = (car.direction == 2 and car.position[0] > 2) or (car.direction == 3 and car.position[0] < 3)

    if not do_lane_change:
        nasch(car, gap, road_section)
        return

    lane_change(car, gap, road_section)


def nasch(car, gap, road_section):
    grid = road_section.grid
    grid_temp = road_section.grid_temp
    updates = road_section.updates

    r = car.position[0]
    c = car.position[1]
    v = car.speed
    index = grid_temp[r][c]
    grid[r][c] = -1

    # acceleration
    v = min(v+1, vmax)
    # braking
    v = min(v, gap)
    # randomness
    if np.random.random() < pv:
        v = max(v-1, 0)
    # update
    if c+v < grid.shape[1]:
        grid[r][c+v] = index
        updates[index] = (v, (r, c+v))
        return

    if c + v >= grid.shape[1]:
        road_section.output_car(car, v)


generated_cars = 0


def lane_change(car, gap, road_section):
    cars = road_section.cars
    grid = road_section.grid
    grid_temp = road_section.grid_temp
    updates = road_section.updates

    r = car.position[0]
    c = car.position[1]
    v = car.speed
    vh = car.get_vh()
    p = 1
    d = car.direction

    vback = -1
    index = grid_temp[r][c]
    columns = grid.shape[1]
    rows = grid.shape[0]

    #When car isn't in the right lane after 80% of the track the change
    #to change lane is 1.
    if c > 80 and ((d == 2 and r > 2) or (d == 3 and r < 3)):
        p = 1

    #When the car is in the most left lane.
    if r == 0 or (d == 3 and r < 3):
        change_posistion(1, p, car, gap, road_section)
    #Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows - 1 or (d == 2 and r > 2):
        change_posistion(r-1, p, car, gap, road_section)
    #Als de auto zich in de vierde rijstrook bevind en ter hoogte van de oprit.
    elif r == 3 and c < 10:
        change_posistion(2, p, car, gap, road_section)
    #Als de auto in een van de middelste rijstroken bevind.
    else:
        gapoL = calc_gap(r-1, c, grid_temp, 1, cars)
        gapoBackL = calc_gap(r-1, c+gap, grid_temp, -1, cars)
        if gapoL >= v and gapoBackL > vback and np.random.random() < p and c+vh < columns:
            change_posistion(r-1, p, car, gap, road_section)
        else:
            change_posistion(r+1, p, car, gap, road_section)


#r is the lane the car wants to go to
def change_posistion(r, p, car, gap, road_section):
    cars = road_section.cars
    grid = road_section.grid
    grid_temp = road_section.grid_temp
    updates = road_section.updates
    c = car.position[1]
    v = car.speed
    vh = car.get_vh()
    index = grid_temp[car.position[0]][c]

    columns = grid.shape[1]
    gapo = calc_gap(r, c, grid_temp, 1, cars)
    gapoBack = calc_gap(r, c+gap, grid_temp, -1, cars)

    #If the car can change his lane.
    if gapo >= v and gapoBack > vback and np.random.random() < p and c+vh < columns:
        if grid[r][c+vh] == -1:
            grid[r][c+vh] = index
            updates[index] = (vh, (r, c+vh))
        else:
            if cars[grid[r][c+vh]].position[1] < c:
                car2 = cars[grid[r][c+vh]]
                gap2 = calc_gap(car2.position[0], car2.position[1], grid_temp, 1, cars)
                nasch(car2, gap2, road_section)
                grid[r][c+vh] = index
                updates[index] = (vh, (r, c+vh))
            else:
                nasch(car, gap, road_section)

    else:
        nasch(car, gap, road_section)
    grid[car.position[0]][c] = -1


# def simulate(config):
#     rows = config['rows']
#     columns = config['columns']
#     step = config['step']
#
#     grid = np.full((rows, columns),  -1, dtype=np.int32)
#     cars = {}
#     # cars = {
#     # 0 : Car(5, 1, 1, (0,2)),
#     # 1 : Car(5, 1, 1, (2,2)),
#     # 2 : Car(2, 1, 1, (0,4)),
#     # 3 : Car(2, 1, 1, (2,4))
#     # }
#     # grid = np.array([[-1,-1,0,-1,2,-1,-1,-1,-1,-1],
#     #         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#     #         [-1,-1,1,-1,3,-1,-1,-1,-1,-1]])
#
#     for i in range(step):
#         updates = {}
#         gridTemp = copy.deepcopy(grid)
#
#         get_car_updates(cars, grid, gridTemp, updates)
#
#         # Update cars
#         update_cars(cars, updates)
#
#         # Generate auto only works for 1 car
#         generate_cars(cars, grid)
#
#         if i % 100 == 0 and i > 0:
#             remove_old_cars(cars, grid)
#
#         # If we want to animate the simulation, yield the grid for every step
#         yield grid, cars


r1 = RoadSection(2, 10)
r2 = RoadSection(5, 10, True)

outputMap = {
    0: 3,  # Lane 1 corresponds with lane 5.
    1: 4   # Lane 2 corresponds with lane 5.
}

r1.set_output_mapping(r2, outputMap)

simulation = Simulation(r1, [r2], 100)
result = simulation.run()
[r for r in result]
