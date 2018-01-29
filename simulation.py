from RoadSection import RoadSection
import numpy as np

from car import Car
from traffic import remove_old_cars, print_grid
import copy

# Global vars
speed_changes = {}
auto = 1
vmax = 5
pv = 0.2
pc = 1


class Simulation:
    def __init__(self, start_road, rest_roads, step, avSpeed=False):
        self.start_road = start_road
        self.roads = [start_road, *rest_roads] # Pack into one list
        self.step = step
        self.generated_cars = 0  # Ensures unique ids/indices
        self.avSpeed = avSpeed
        self.densities = []

    def run(self):
        for i in range(self.step):
            roads_steps = {}
            # update cars
            for j in range(len(self.roads)):
                road_section = self.roads[j]
                road_section.set_temp_grid()

                # Generates the updates for all cars
                get_car_updates(road_section)

                # Update cars
                update_cars(road_section)

                # Add new cars added from 'previous' road_section
                road_section.add_new_cars()

                # Only generates cars in the road_sections that are starting sections
                if road_section.spawn:
                    self.generate_cars(road_section)

                # If we want to animate the simulation, yield the grid for every step
                roads_steps[j] = road_section

                # Calculate the average speed in the middle of the section.
                if self.avSpeed:
                    grid = road_section.grid
                    cars = road_section.cars
                    averageSpeed = self.speedaverage(grid, cars, road_section,i)
                    #self.avSpeed = averageSpeed

            # Every 10 steps we add a the current density
            if i % 10 == 0:
                self.add_density()

            yield roads_steps

    # This function spawns new cars on the road. It will check for each lane if a car must spawn.
    def generate_cars(self, road_section):
        cars = road_section.cars
        grid = road_section.grid
        rows = grid.shape[0]
        right_lane = road_section.right_lane
        spawn_probabilities = road_section.spawn_probabilities[0]
        speed_probabilities = road_section.spawn_probabilities[1]
        direction_probabilities = road_section.spawn_probabilities[2]
        for i in range(rows):
            # Cannot spawn a car if the spot is already occupied
            if grid[i][0] != -1:
                continue

            if i not in spawn_probabilities:
                continue

            # Determine if we want to spawn a car based on P
            p = spawn_probabilities[i]
            if np.random.random() > p:
                continue

            # Speed probabilities where the value is the lower/upper bound tuple of the probability
            n = np.random.random()
            v_start = 1
            for v in speed_probabilities:
                lower_bound, upper_bound = speed_probabilities[v]
                if lower_bound < n <= upper_bound:
                    v_start = v
                    break

            new_car_index = self.generated_cars
            self.generated_cars += 1
            d = np.random.randint(0, right_lane)

            # Direction probabilities where the value is the lower/upper bound tuple of the probability
            if len(direction_probabilities) != 0:
                n = np.random.random()
                d = 0
                for direction in direction_probabilities:
                    lower_bound, upper_bound = direction_probabilities[direction]
                    if lower_bound < n <= upper_bound:
                        d = direction
                        break
            color = road_section.output_colors[d]
            cars[new_car_index] = Car(new_car_index, v_start, color, d, (i,0))
            grid[i][0] = new_car_index

    # This function calculates the average speed on a road section and adds it to the total. The average speeds is each
    # time step calculated by going through all the cars.
    def speedaverage(self, grid, cars, road_section, i):
        totalSpeed = 0
        coordinates = np.where(road_section.grid > -1)
        # If no car has driven on the section at the last time step, average_speed_steps is set to 1 to prevent dividing by zero.
        if i == self.step - 1:
            road_section.average_speed_steps = max(road_section.average_speed_steps, 1)

        if (len(coordinates[0])) > 0:
            for j in range(len(coordinates[0])):
                row = coordinates[0][j]
                column = coordinates[1][j]
                car = road_section.cars[road_section.grid[row][column]]
                totalSpeed += car.speed
            averageSpeed = totalSpeed/(len(coordinates[0]))
            road_section.average_speed += averageSpeed
            road_section.average_speed_steps += 1
            return averageSpeed
        return 0

    # This function calculates the density. It goes through the sections and adds the density to the total.
    # The density is calculated by the amount of cars on a road section divided by the length of the road section.
    def add_density(self):
        cars = 0
        surface = 0
        for i in range(len(self.roads)):
            road = self.roads[i]
            surface += road.grid.shape[0] * road.grid.shape[1]
            coords = road.get_car_coordinates()
            cars += len(coords[0])

        density = np.divide(cars, surface)
        self.densities.append(density)


# Applies the updates made in get_car_updates()
def update_cars(road_section):
    cars = road_section.cars
    for x, y in road_section.updates.items():
        cars[x].set_speed(y[0])
        cars[x].set_position(y[1])

    road_section.updates = {}


# This function goes through all cars and moves them to their new location.
def get_car_updates(road_section):
    coordinates = road_section.get_car_coordinates()
    cars = road_section.cars
    for j in range(len(coordinates[0])):
        row = coordinates[0][j]
        column = coordinates[1][j]
        car = cars[road_section.grid_temp[row][column]]

        if (row, column) != car.position:
            continue

        move_car(car, road_section)


# This function checks if the car wants to change lane. It will change lane if the car in front of him drives slower
# or when the car is not on the right lane.
def move_car(car, road_section):
    cars = road_section.cars
    grid_temp = road_section.grid_temp

    # Roadblocks are represented by numbers < -1. These can't move.
    if car.index < -1:
        return

    # If the gap in front of the car is too small, it will attempt to change lane.
    gap, _ = calc_gap(car.position[0], car.position[1], grid_temp, 1, road_section)
    do_lane_change = ((car.speed > gap and car.position[1] < (road_section.columns*0.8) and road_section.right_lane != 1) 
                    or (car.position[0] != car.direction))

    # If the car can't change lane, it will move forward on the same lane and possibily slow down.
    if not do_lane_change:
        nasch(car, gap, road_section)
        return

    lane_change(car, gap, road_section)


# This function moves the car on the same lane forward. It will brake the car when there's
# a car in front of him with not enouph space between them. Otherwise the car will try to accelerate.
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
        if grid[r, c+v] != -1:
            print('Occupied', road_section.name, (r, c), (r, c+v),  gap)
        grid[r, c+v] = index
        updates[index] = (v, (r, c+v))
        return

    # Car goes out of the grid
    if c + v >= grid.shape[1]:
        road_section.output_car(car, v)


# This function calculates in which direction a lane changing car wants to go to.
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

    columns = grid.shape[1]
    right_lane = road_section.right_lane

    # When car isn't in the right lane after 80% of the track the chanse
    # to change lane is 1.
    if c > (0.8) * columns and ((d <= 2 and r > 2) or (d >= 3 and r < 3)):
        p = 1

    # When the car is in the most left lane or wants to go right.
    if r + 1 < right_lane and (r == 0 or (r < d)):
        change_position(r+1, p, car, gap, road_section)
        return
    # When the car is in the most right lane or wants to go left.
    elif r-1 >= 0 and (r == right_lane - 1 or (r > d)):
        change_position(r - 1, p, car, gap, road_section)
        return
    # When the car is in one of the middle lanes.
    elif r + 1 < right_lane and r - 1 >= 0:
        gapoL, _ = calc_gap(r - 1, c, grid_temp, 1, road_section)
        gapoBackL, vback = calc_gap(r - 1, c + gap, grid_temp, -1, road_section)
        # If the car can go left, it will go left, otherwise it goes right.
        if gapoL >= v and gapoBackL > vback and np.random.random() < p and c+vh < columns:
            change_position(r - 1, p, car, gap, road_section)
        else:
            change_position(r + 1, p, car, gap, road_section)
        return
    nasch(car, gap, road_section)


# This function calculates if the car change position to the new lane. If it can it will also
# move the car to the new lane.
# r is the lane the car wants to go to
def change_position(r, p, car, gap, road_section):
    grid = road_section.grid
    grid_temp = road_section.grid_temp
    c = car.position[1]
    v = car.speed
    vh = car.get_vh()
    index = grid_temp[car.position[0], c]
    gapo, _ = calc_gap(r, c, grid_temp, 1, road_section)
    gapoBack, vback = calc_gap(r, c + vh, grid_temp, -1, road_section)

    # Checks if the car will drive out of the grid. When it does, it will change the column
    # to the column on the new grid. Also the new grid will be set as the current road.
    if c + vh >= grid.shape[1]:
        if not road_section.is_end_road:
            current_road, row_index = road_section.output_map[r]
            car.direction = np.random.randint(0, current_road.right_lane)
            col_index = c+vh - grid.shape[1]
        else:
            nasch(car, gap, road_section)
            grid[car.position[0], c] = -1
            return
    else:
        row_index = r
        col_index = c+vh
        current_road = road_section

    # If the car can change his lane.It will go to the row and column previously calculated.
    if gapo >= v and gapoBack > vback and np.random.random() < p and current_road.grid[row_index][col_index] == -1:
        current_road.grid[row_index][col_index] = index
        current_road.updates[index] = (vh, (row_index, col_index))
        current_road.cars[index] = car

        if current_road.name != road_section.name:
            del road_section.cars[index]

    # The car will slowdown when he can't change lane when he wants to.
    else:
        car.speed = max(car.speed-2, 1)
        nasch(car, gap, road_section)
        return

    grid[car.position[0], c] = -1


# This function calculates the gap infront of back from the place of (r,c).
# Whith a maximum gap of vmax and whith t=1 for in front and t=-1 for the back.
def calc_gap(r, c, grid_temp, t, road_section):
    array_check = []
    vback = -1
    prev_road = None
    next_road = None
    car = None

    for i in range(1, vmax+1):
        new_c = c + (i*t)
        if new_c >= 0 and new_c < grid_temp.shape[1]:
            array_check.append(grid_temp[r, new_c])
        elif new_c < 0:
            if not road_section.start_road and r in road_section.input_map:
                prev_road, prev_row = road_section.input_map[r]
                prev_col = new_c + prev_road.columns
                array_check.append(prev_road.grid_temp[prev_row][prev_col])
            else:
                array_check.append(-1)
        else:
            if not road_section.is_end_road:
                next_road, next_row = road_section.output_map[r]
                next_col = new_c - grid_temp.shape[1]
                array_check.append(next_road.grid[next_row][next_col])
            else:
                array_check.append(-1)

    array_check = np.array(array_check).flatten()
    next_car = np.where(array_check != -1)
    if len(next_car[0]) > 0:
        gap = next_car[0][0]
        car_index = array_check[gap]
        if car_index in road_section.cars:
            car = road_section.cars[car_index]
        elif prev_road and car_index in prev_road.cars:
            car = prev_road.cars[car_index]
        elif next_road and car_index in next_road.cars:
            car = next_road.cars[car_index]

        if car:
            vback = min(car.speed + 1, vmax)

        return gap, vback

    return vmax, vback
