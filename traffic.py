#Computational science project
#Lukas, Martijn, Lennart, Max
#10783687, , 10432973, 11042729,

import numpy as np
import copy
from car import Car



# TODO: remove
# Global vars
speed_changes = {}
auto = 1
vmax = 5
pv = 0.2
vback = -1
pc = 1

#nagel-scheckenberg
def nasch(r, c, v, gap, grid):
    index = grid[r][c]
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
        speed_changes[index] = v




#t is 1 dan vooruit gap en t is -1 achteruit gap
def calcGap(r, c, gridTemp, t, cars):
    gap = 0
    for k in range(1, vmax+1):
        if t == -1:
            if c-k >= 0:
                if gridTemp[r][c-k] == -1:
                    gap += 1
                else:
                    vback = cars[gridTemp[r][c-k]].speed
                    break
            else:
                gap = 10
        else:
            if c+k < gridTemp.shape[1]:
                if gridTemp[r][c+k] == -1:
                    gap += 1
                else:
                    break
            else:
                gap = 10
    return gap

def laneChange(r, c, v, gridTemp, gap, vh, cars, grid):
    vback = -1
    index = gridTemp[r][c]
    columns = grid.shape[1]
    rows = grid.shape[0]

    #Als de auto zich in de meest linker rijstrook bevind.
    if r == 0:
        gapo = calcGap(1, c, gridTemp, 1, cars)
        gapoBack = calcGap(1, c+gap, gridTemp, -1, cars)
        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < pc and c+vh < columns:
            grid[1][c+vh] = index
            speed_changes[index] = vh
        else:
            nasch(r, c, v, gap, grid)

    #Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows - 1:
        gapo = calcGap(r-1, c, gridTemp, 1, cars)
        gapoBack = calcGap(r-1, c+gap, gridTemp, -1, cars)
        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < pc and c+vh < columns:
            grid[r-1][c+vh] = index
            speed_changes[index] = vh
        else:
            nasch(r, c, v, gap, grid)

    #Als de auto in een van de middelste rijstroken bevind.
    else:
        gapoL = calcGap(r-1, c, gridTemp, 1, cars)
        gapoBackL = calcGap(r-1, c+gap, gridTemp, -1, cars)
        if gapoL >= v and gapoBackL > vback and np.random.random() < pc and c+vh < columns:
            grid[r-1][c+vh] = index
            speed_changes[index] = vh
        else:
            gapoR = calcGap(r+1, c, gridTemp, 1, cars)
            gapoBackR = calcGap(r+1, c+gap, gridTemp, -1, cars)
            if gapoR >= v and gapoBackR > vback and np.random.random() < pc and c+vh < columns:
                grid[r+1][c+vh] = index
                speed_changes[index] = vh
            else:
                nasch(r, c, v, gap, grid)

        grid[r][c] = -1


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
        generate_cars(cars, grid, rows)

        if i % 100 == 0 and i > 0:
            remove_old_cars(cars, grid)

        # If we want to animate the simulation, yield the grid for every step
        yield grid, cars


# Removes cars from the cars dict no longer in the grid
def remove_old_cars(cars, grid):
    active_cars = set(grid.flatten())
    remove = [k for k, car in cars.items() if car not in active_cars]

    for k in remove:
        del cars[k]


# Generates cars for every step
def generate_cars(cars, grid, rows):
    for i in range(rows):
        if i == 4:
            if np.random.random() < 0.7:
                v = np.random.randint(3, 5)
                new_car_index = len(cars)
                cars[new_car_index] = Car(v, np.random.random(3), np.random.randint(2))
                grid[i][0] = new_car_index
            break

        ps = 1 / float(rows + 2) * (i + 1)
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
            cars[new_car_index] = Car(v, np.random.random(3), np.random.randint(2))
            grid[i][0] = new_car_index


def print_grid(grid):
    print("---------------")
    print(grid)
    print("---------------")


if __name__ == '__main__':
    config = {
        'rows': 5,
        'columns': 10,
        'step': 10,
    }

    grids = simulate(config)
    [print_grid(grid) for grid in grids]













