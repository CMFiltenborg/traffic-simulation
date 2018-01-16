from RoadSection import RoadSection
import numpy as np

from car import Car
from traffic import remove_old_cars, print_grid
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
    def __init__(self, start_road, rest_roads, step, avSpeed):
        self.start_road = start_road
        self.roads = [start_road, *rest_roads] # Pack into one list
        self.step = step
        self.generated_cars = 0  # Ensures unique ids/indices
        self.avSpeed = avSpeed

    def speedaverage(self, grid, cars, road_section):
        totalSpeed = 0
        for car in cars:
            totalSpeed += cars[car].speed
        
        if len(cars) > 0:
            gemSpeed = totalSpeed/len(cars)
        return gemSpeed

    def run(self):
        for i in range(self.step):
            roads_steps = {}

            for j in range(len(self.roads)):
                road_section = self.roads[j]
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
                    self.generate_cars(road_section)

                # if i % 100 == 0 and i > 0:
                #     remove_old_cars(cars, grid)

                # If we want to animate the simulation, yield the grid for every step
                # print_grid((grid, cars))
                roads_steps[j] = (road_section.grid, road_section.cars)

                # Calculate the average speed in the middel of the section.
                if self.avSpeed:
                    grid = road_section.grid
                    cars = road_section.cars
                    gemSpeed = self.speedaverage(grid, cars, road_section)

            yield roads_steps

    def generate_cars(self, road_section):
        cars = road_section.cars
        grid = road_section.grid
        rows = grid.shape[0]
        for i in range(rows):
            if i == 4:
                if np.random.random() < 0.5:
                    v = np.random.randint(3, 5)
                    new_car_index = self.generated_cars
                    self.generated_cars += 1
                    d = np.random.randint(0,rows)
                    if d >= 3:
                        color = 'black'
                    else:
                        color = 'r'
                    cars[new_car_index] = Car(new_car_index, v, color, d, (i,0))
                    grid[i][0] = new_car_index
                break

            #ps = 1 / float(rows+2) * (i + 1)
            ps = 0.2
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
                d = np.random.randint(0,rows)
                if d >= 3:
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

    gap = calc_gap(car.position[0], car.position[1], grid_temp, 1, cars, road_section)
    do_lane_change = (car.speed > gap) or (car.position[0] != car.direction)

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
    # Update car
    if c+v < grid.shape[1]:
        grid[r][c+v] = index
        updates[index] = (v, (r, c+v))
        return

    # Car goes out of the grid
    if c + v >= grid.shape[1]:
        road_section.output_car(car, v)


generated_cars = 0


def lane_change(car, gap, road_section):
    cars = road_section.cars
    grid = road_section.grid
    grid_temp = road_section.grid_temp

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

    # When car isn't in the right lane after 80% of the track the chanse
    # to change lane is 1.
    if c > (0.8)*columns and ((d <= 2 and r > 2) or (d >= 3 and r < 3)):
        p = 1

    # When the car is in the most left lane.
    if r == 0 or (r < d):
        change_position(r+1, p, car, gap, road_section)
    # Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows - 1 or (r > d):
        change_position(r - 1, p, car, gap, road_section)
    # Als de auto zich in de vierde rijstrook bevind en ter hoogte van de oprit.
    elif r == 3 and c < 10:
        change_position(2, p, car, gap, road_section)
    # Als de auto zich in een van de middelste rijstroken bevind.
    else:
        gapoL = calc_gap(r-1, c, grid_temp, 1, cars, road_section)
        gapoBackL = calc_gap(r-1, c+gap, grid_temp, -1, cars, road_section)
        if gapoL >= v and gapoBackL > vback and np.random.random() < p and c+vh < columns:
            change_position(r - 1, p, car, gap, road_section)
        else:
            change_position(r + 1, p, car, gap, road_section)


# r is the lane the car wants to go to
def change_position(r, p, car, gap, road_section):
    cars = road_section.cars
    grid = road_section.grid
    grid_temp = road_section.grid_temp
    updates = road_section.updates
    c = car.position[1]
    v = car.speed
    vh = car.get_vh()
    index = grid_temp[car.position[0]][c]
    columns = grid.shape[1]
    gapo = calc_gap(r, c, grid_temp, 1, cars, road_section)
    gapoBack = calc_gap(r, c+gap, grid_temp, -1, cars, road_section)
    
    if c+vh >= columns:
        if road_section.output_road:
            row_index = road_section.output_map[r]
            col_index = c+vh - columns
            current_road = road_section.output_road
        else:
            nasch(car, gap, road_section)
            grid[car.position[0]][c] = -1
            return
    else:
        row_index = r
        col_index = c+vh
        current_road = road_section

    # If the car can change his lane.
    if gapo >= v and gapoBack > vback and np.random.random() < p and current_road.grid[row_index][col_index] == -1:
        current_road.grid[row_index][col_index] = index
        current_road.updates[index] = (vh, (row_index, col_index))
    else:
        nasch(car, gap, road_section)
    grid[car.position[0]][c] = -1

#This function calculates the gap infront of back from the place of (r,c).
#Whith a maximum gap of vmax and whith t=1 for in front and t=-1 for the back.
def calc_gap(r, c, grid_temp, t, cars, road_section):
    array_check = []

    for i in range(1, vmax+1):
        new_c = c + (i*t)
        if new_c >= 0 and new_c < grid_temp.shape[1]:
            array_check.append(grid_temp[r][new_c])
        elif new_c < 0:
            if road_section.input_road:
                prev_road = road_section.input_road
                prev_row = road_section.input_map[r]
                prev_col = c + prev_road.columns
                array_check.append(prev_road.grid_temp[prev_row][prev_col])
            else:
                array_check.append(-1)
        else:
            if road_section.output_road:
                next_road = road_section.output_road
                next_row = road_section.output_map[r]
                next_col = c - grid_temp.shape[1]
                array_check.append(next_road.grid[next_row][next_col])
            else:
                array_check.append(-1)

    array_check = np.array(array_check).flatten()
    next_car = np.where(array_check != -1)
    if len(next_car[0]) > 0:
        return next_car[0][0]
    else:
        return len(array_check)


if __name__ == '__main__':
    r1 = RoadSection(2, 10)
    r2 = RoadSection(5, 10, True)

    outputMap = {
        0: 3,  # Lane 1 corresponds with lane 5.
        1: 4   # Lane 2 corresponds with lane 5.
    }


    r1.set_output_mapping(r2, outputMap)
    r2.set_input_mapping(r1)

    simulation = Simulation(r1, [r2], 100)
    result = simulation.run()
    [r for r in result]
