#Computational science project
#Lukas, Martijn, Lennart, Max
#10783687, , 10432973, 11042729,

import numpy as np
import copy
from car import Car



# TODO: remove
# Global vars
auto = 1
vmax = 5
pv = 0.2
vback = -1


#This function calculates the new position of the car using Nagel-Scheckenberg.
def nasch(car, gap, grid, grid_temp, updates):
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



#This function calculates the gap infront of back from the place of (r,c).
#Whith a maximum gap of vmax and whith t=1 for in front and t=-1 for the back.
def calc_gap(r, c, grid_temp, t, cars):
    gap = 0
    for k in range(1, vmax+1):
        #Looking for a gap backwards
        if t == -1:
            if c < grid_temp.shape[1]:
                #When ou of grid
                if c-k < 0:
                    gap = vmax
                    break
                #when no car
                elif grid_temp[r][c-k] == -1:
                    gap += 1
                #Found car
                else:
                    vback = cars[grid_temp[r][c-k]].speed
                    break
            else:
                gap = c - grid_temp.shape[1]
        #Looking for a gap infront
        else:
            #When out of grid
            if c+k >= grid_temp.shape[1]:
                gap += 1
            #When no car
            elif grid_temp[r][c+k] == -1:
                gap += 1
            #Found car
            else:
                break
    return gap

#t is 1 dan vooruit gap en t is -1 achteruit gap
# def calc_gap_car(car, gridTemp, t, cars):
#     r = car.position[0]
#     c = car.position[1]
#     gap = 0
#     for k in range(1, vmax+1):
#         if t == -1:
#             if c < gridTemp.shape[1]:
#                 if c-k >= 0:
#                     if gridTemp[r][c-k] == -1:
#                         gap += 1
#                     else:
#                         vback = cars[gridTemp[r][c-k]].speed
#                         break
#                 else:
#                     gap = 10
#             else:
#                 gap = 10
#         else:
#
#             if c + k < gridTemp.shape[1]:
#                 if gridTemp[r][c+k] != -1:
#                     return 10
#
#                 gap += 1
#
#             else:
#                 gap = 10
#     return gap


def lane_change(car, gridTemp, gap, cars, grid, updates):
    r = car.position[0]
    c = car.position[1]
    v = car.speed
    vh = car.get_vh()
    p = 1
    d = car.direction

    vback = -1
    index = gridTemp[r][c]
    columns = grid.shape[1]
    rows = grid.shape[0]

    #Als de auto zich in de meest linker rijstrook bevind.

    if c > 80 and ((d == 2 and r > 2) or (d == 3 and r < 3)):
        p = 1

    if r == 0 or (d == 3 and r < 3):
        gapo = calc_gap(1, c, gridTemp, 1, cars)
        gapoBack = calc_gap(1, c+gap, gridTemp, -1, cars)
        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < p and c+vh < columns:
            if grid[1][c+vh] == -1:
                grid[1][c+vh] = index
                updates[index] = (vh, (1, c+vh))
            else:
                if cars[grid[1][c+vh]].position[1] < c:
                    # r2, c2 = cars[grid[1][c+vh]].position
                    # v2 = cars[grid[1][c+vh]].speed
                    car2 = cars[grid[1][c+vh]]
                    gap2 = calc_gap(car2.position[0], car2.position[1], gridTemp, 1, cars)
                    nasch(car2, gap2, grid, gridTemp, updates)
                    grid[1][c+vh] = index
                    updates[index] = (vh, (1, c+vh))
                else:
                    nasch(car, gap, grid, gridTemp, updates)
    
        else:
            nasch(car, gap, grid, gridTemp, updates)
        # grid[r][c] = -1

    #Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows - 1 or (d == 2 and r > 2):
        gapo = calc_gap(r-1, c, gridTemp, 1, cars)
        gapoBack = calc_gap(r-1, c+gap, gridTemp, -1, cars)

        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < p and c+vh < columns:
            if grid[r-1][c+vh] == -1:
                grid[r-1][c+vh] = index
                updates[index] = (vh, (r-1, c+vh))
            else:
                if cars[grid[r-1][c+vh]].position[1] < c:
                    car2 = cars[grid[r-1][c+vh]]
                    gap2 = calc_gap(car2.position[0], car2.position[1], gridTemp, 1, cars)
                    nasch(car2, gap2, grid, gridTemp, updates)

                    # r2, c2 = cars[grid[r-1][c+vh]].position
                    # v2 = cars[grid[r-1][c+vh]].speed
                    # gap2 = calcGap(r2, c2, gridTemp, 1, cars)
                    # nasch(car, gap2, grid, gridTemp)
                    grid[r-1][c+vh] = index
                    updates[index] = (vh, (r-1, c+vh))
                else:
                    nasch(car, gap, grid, gridTemp, updates)
        else:
            nasch(car, gap, grid, gridTemp, updates)
        # grid[r][c] = -1

    #Als de auto zich in de vierde rijstrook bevind en ter hoogte van de oprit.
    elif r == 3 and c < 10:
        gapo = calc_gap(2, c, gridTemp, 1, cars)
        gapoBack = calc_gap(2, c+gap, gridTemp, -1, cars)
        if gapo >= v and gapoBack > vback and np.random.random() < p and c+vh < columns:
            car2 = cars[grid[2][c+vh]]
            gap2 = calc_gap(car2.position[0], car2.position[1], gridTemp, 1, cars)
            nasch(car2, gap2, grid, gridTemp, updates)

            grid[2][c+vh] = index
            updates[index] = (vh, (2, c+vh))
        else:
            nasch(car, gap, grid, gridTemp, updates)
        grid[3][c] = -1


    #Als de auto in een van de middelste rijstroken bevind.
    else:
        gapoL = calc_gap(r-1, c, gridTemp, 1, cars)
        gapoBackL = calc_gap(r-1, c+gap, gridTemp, -1, cars)
        if gapoL >= v and gapoBackL > vback and np.random.random() < p and c+vh < columns:
            if  grid[r-1][c+vh] == -1:
                grid[r-1][c+vh] = index
                updates[index] = (vh, (r-1, c+vh))
            else:
                if cars[grid[r-1][c+vh]].position[1] < c:
                    car2 = cars[grid[r-1][c+vh]]
                    gap2 = calc_gap(car2.position[0], car2.position[1], gridTemp, 1, cars)
                    nasch(car2, gap2, grid, gridTemp, updates)

                    # r2, c2 = cars[grid[r-1][c+vh]].position
                    # v2 = cars[grid[r-1][c+vh]].speed
                    # gap2 = calcGap(r2, c2, gridTemp, 1, cars)
                    # nasch(car, gap2, grid, gridTemp)
                    grid[r-1][c+vh] = index
                    updates[index] = (vh, (r-1, c+vh))
                else:
                    nasch(car, gap, grid, gridTemp, updates)
        else:
            gapoR = calc_gap(r+1, c, gridTemp, 1, cars)
            gapoBackR = calc_gap(r+1, c+gap, gridTemp, -1, cars)
            if gapoR >= v and gapoBackR > vback and np.random.random() < p and c+vh < columns:
                if  grid[r+1][c+vh] == -1:
                    grid[r+1][c+vh] = index
                    updates[index] = (vh, (r+1, c+vh))
                else:
                    if cars[grid[r+1][c+vh]].position[1] < c:
                        car2 = cars[grid[r+1][c+vh]]
                        gap2 = calc_gap(car2.position[0], car2.position[1], gridTemp, 1, cars)
                        nasch(car2, gap2, grid, gridTemp, updates)

                        # r2, c2 = cars[grid[r+1][c+vh]].position
                        # v2 = cars[grid[r+1][c+vh]].speed
                        # gap2 = calcGap(r2, c2, gridTemp, 1, cars)
                        # nasch(car, gap2, grid, gridTemp)
                        grid[r+1][c+vh] = index
                        updates[index] = (vh, (r+1, c+vh))
                    else:
                        nasch(car, gap, grid, gridTemp, updates)
            else:
                nasch(car, gap, grid, gridTemp, updates)

        # grid[r][c] = -1


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
        grid_temp = copy.deepcopy(grid)

        # Generates the updates for all cars
        get_car_updates(cars, grid, grid_temp, updates)

        # Update cars
        update_cars(cars, updates)

        # Generate auto only works for 1 car
        generate_cars(cars, grid)

        if i % 100 == 0 and i > 0:
            remove_old_cars(cars, grid)

        # If we want to animate the simulation, yield the grid for every step
        yield grid, cars


def get_car_updates(cars, grid, gridTemp, updates):
    coordinates = np.where(grid != -1)
    for j in range(len(coordinates[0])):
        row = coordinates[0][j]
        column = coordinates[1][j]
        car = cars[gridTemp[row][column]]

        move_car(car, cars, grid, gridTemp, updates)


def update_cars(cars, updates):
    for x, y in updates.items():
        cars[x].set_speed(y[0])
        cars[x].set_position(y[1])


def move_car(car, cars, grid, gridTemp, updates):
    gap = calc_gap(car.position[0], car.position[1], gridTemp, 1, cars)
    do_lane_change = (car.direction == 2 and car.position[0] > 2) or (car.direction == 3 and car.position[0] < 3)

    if not do_lane_change:
        nasch(car, gap, grid, gridTemp, updates)
        return

    lane_change(car, gridTemp, gap, cars, grid, updates)


# Removes cars from the cars dict no longer in the grid
def remove_old_cars(cars, grid):
    active_cars = set(grid.flatten())
    remove = [k for k, car in cars.items() if car not in active_cars]

    for k in remove:
        del cars[k]


# Generates cars for every step
def generate_cars(cars, grid):
    rows = grid.shape[0]
    for i in range(rows):
        if i == 4:
            if np.random.random() < 0.5:
                v = np.random.randint(3, 5)
                new_car_index = len(cars)
                d = np.random.randint(2,4)
                if d == 3:
                    color = 'black'
                else:
                    color = 'r'
                cars[new_car_index] = Car(v, color, d, (i,0))
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
            new_car_index = len(cars)
            d = np.random.randint(2,4)
            if d == 3:
                color = 'black'
            else:
                color = 'r'
            cars[new_car_index] = Car(v, color, d, (i,0))
            grid[i][0] = new_car_index


def print_grid(grid):
    grid, cars = grid
    print("---------------")
    print(grid)
    print(cars[1].position)
    print("---------------")


if __name__ == '__main__':
    config = {
        'rows': 5,
        'columns': 100,
        'step': 100,
    }

    grids = simulate(config)
    [print_grid(grid) for grid in grids]













