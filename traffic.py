#Computational science project
#Lukas, Martijn, Lennard, Max
#10783687, , 11042729,

import numpy as np
import copy

rows = 3
collums = 10
grid = np.full((rows,collums),  -1, dtype=np.int32)
#grid = np.array([[-1,-1,5,-1,-1,3,-1,-1,-1,-1],[-1,-1,-1,-1,2,-1,-1,-1,-1,-1],[-1,-1,2,-1,-1,3,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,3,-1,-1,-1],[-1,-1,-1,-1,2,-1,-1,-1,-1,-1]])
step = 10
auto = 1
vmax = 5
pv = 0.2
vback = -1
pc = 1


#nagel-scheckenberg
def nasch(r, c, v, gap):
    grid[r][c] = -1
    #acceleration
    v = min(v+1, vmax)
    #braking
    v = min(v, gap)
    #randomness
    if np.random.random() < pv:
        v = max(v-1, 0)
    #update
    if c+v < collums:
        grid[r][c+v] = v



#t is 1 dan vooruit gap en t is -1 achteruit gap
def calcGap(r, c, gridTemp, t):
    gap = 0
    for k in range(1, vmax+1):
        if t == -1:
            if c-k >= 0:
                if gridTemp[r][c-k] == -1:
                    gap += 1
                else:
                    vback = gridTemp[r][c-k]
                    break
            else:
                gap = 10
        else:
            if c+k < collums:
                if gridTemp[r][c+k] == -1:
                    gap += 1
                else:
                    break
            else:
                gap = 10
    return gap

def laneChange(r, c, v, gridTemp, gap, vh):
    vback = -1
    #Als de auto zich in de meest linker rijstrook bevind.
    if r == 0:
        gapo = calcGap(1, c, gridTemp, 1)
        gapoBack = calcGap(1, c+gap, gridTemp, -1)
        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < pc and c+vh < collums:
            grid[1][c+vh] = vh
        else:
            nasch(r, c, v, gap)

    #Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows-1:
        gapo = calcGap(r-1, c, gridTemp, 1)
        gapoBack = calcGap(r-1, c+gap, gridTemp, -1)
        grid[r][c] = -1
        if gapo >= v and gapoBack > vback and np.random.random() < pc and c+vh < collums:
            grid[r-1][c+vh] = vh
        else:
            nasch(r, c, v, gap)

    #Als de auto in een van de middelste rijstroken bevind.
    else:
        gapoL = calcGap(r-1, c, gridTemp, 1)
        gapoBackL = calcGap(r-1, c+gap, gridTemp, -1)
        if gapoL >= v and gapoBackL > vback and np.random.random() < pc and c+vh < collums:
            grid[r-1][c+vh] = vh
        else:
            gapoR = calcGap(r+1, c, gridTemp, 1)
            gapoBackR = calcGap(r+1, c+gap, gridTemp, -1)
            if gapoR >= v and gapoBackR > vback and np.random.random() < pc and c+vh < collums:
                grid[r+1][c+vh] = vh
            else:
                nasch(r, c, v, gap)

        grid[r][c] = -1


def simulate(animate=False):
    for i in range(step):
        coordinates = np.where(grid != -1)
        print(grid)
        gridTemp = copy.deepcopy(grid)
        for j in range(len(coordinates[0])):
            r = coordinates[0][j]
            c = coordinates[1][j]
            v = grid[r][c]
            vh = min(v+1, vmax)

            gap = calcGap(r, c, gridTemp, 1)


            if vh > gap:
                print("hoi")
                laneChange(r, c, v, gridTemp, gap, vh)
            else:
                nasch(r, c, v, gap)

        #generate auto only works for 1 car
        for l in range(auto):
            space = []
            for m in range(rows):
                if grid[m][0] == -1:
                    space.append(m)
            if len(space) < 1:
                break
            else:
                r = np.random.randint(0, len(space))
                v = np.random.randint(1, 6)
                grid[space[r]][0] = v

        # If we want to animate the simulation, yield the grid for every step
        if animate:
            yield grid


def print_grid(grid):
    print("---------------")
    print(grid)
    print("---------------")


if __name__ == '__main__':
    grids = simulate(False)
    [print_grid(grid) for grid in grids]













