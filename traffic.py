#Computational science project
#Lukas, Martijn, Lennard, Max
#10783687, , 11042729,

import numpy as np

rows = 3
collums = 10
grid = np.full((rows,collums),  -1, dtype=np.int32)
step = 10#0
auto = 1
vmax = 5
pv = 0.2
vback = -1
pc = 1


'''
grid[2][3] = 3
grid[2][2] = 2
print(np.where(grid != -1))
'''

def calcGapo(r,rn,c,v,gridTemp):
    gapo = 0
    for k in range(1, vmax+1):
        if c+k < collums-1:
            if gridTemp[rn][c+k] == -1:
                gapo += 1
            else:
                break
        else:
            gapo = 10
    return gapo

def calcGapoBack(r,rn,c,v, gridTemp):
    gapoBack = 0
    for k in range(1, vmax+1):
        if c-k >= 0:
            if gridTemp[rn][c-k] == -1:
                gapoBack += 1
            else:
                vback = gridTemp[rn][c-k]
                break
        else:
            gapoBack = 10
    return gapoBack

def laneChange(r, c, v, gridTemp, gap, vh):
    vback = -1
    #Als de auto zich in de meest linker rijstrook bevind.
    if r == 0:
        gapo = calcGapo(0, 1, c, v, gridTemp)
        gapoBack = calcGapoBack(0, 1, c+gap, v, gridTemp)
        grid[r][c] = -1
        if gapo > v and gapoBack > vback:
            if np.random.random() < pc:
                if c+vh < collums-1:
                    grid[1][c+vh] = vh

    #Als de auto zich in de meest rechter rijstrook bevind.
    elif r == rows-1:
        gapo = calcGapo(r, r-1, c, v, gridTemp)
        gapoBack = calcGapoBack(r, r-1, c+gap, v, gridTemp)
        grid[r][c] = -1
        if gapo > v and gapoBack > vback:
            if np.random.random() < pc:
                if c+vh < collums-1:
                    grid[r-1][c+vh] = vh

    #Als de auto in een van de middelste rijstroken bevind.
    else:
        gapoL = calcGapo(r, r-1, c, v, gridTemp)
        gapoBackL = calcGapoBack(r, r-1, c+gap, v, gridTemp)
        if gapoL > v and gapoBackL > vback:
            if np.random.random() < pc:
                if c+vh < collums-1:
                    grid[r-1][c+vh] = vh
        else:
            gapoR = calcGapo(r, r+1, c, v, gridTemp)
            gapoBackR = calcGapoBack(r, r+1, c+gap, v, gridTemp)
            if gapoR > v and gapoBackR > vback:
                if np.random.random() < pc:
                    if c+vh < collums-1:
                        grid[r+1][c+vh] = vh

        grid[r][c] = -1


def simulate(animate=False):
    print("hoi")
    for i in range(step):
        coordinates = np.where(grid != -1)
        gridTemp = grid
        for j in range(len(coordinates[0])):
            r = coordinates[0][j]
            c = coordinates[1][j]
            v = grid[r][c]
            vh = min(v+1, vmax)

            gap = 0
            for k in range(1, vmax+1):
                if c+k < collums-1:
                    if gridTemp[r][c+k] == -1:
                        gap += 1
                    else:
                        break
                else:
                    gap = 10

            
            '''
            if vh > gap:
                print("hoi")
                laneChange(r, c, v, gridTemp, gap, vh)
            '''
            if False:
                print("hoi")
            else:
                #nagel-schreckenberg
                r = coordinates[0][j]
                c = coordinates[1][j]
                v = grid[r][c]
                grid[r][c] = -1
                
                gap = 0
                for k in range(1, vmax+1):
                    if c+k < collums-1:
                        if gridTemp[r][c+k] == -1:
                            gap += 1
                        else:
                            break
                    else:
                        gap = 10

                #acceleration
                v = min(v+1, vmax)
                #braking
                v = min(v, gap)
                #randomness
                if np.random.random() < pv:
                    v = max(v-1, 0)
                #update
                if c+v < collums-1:
                    grid[r][c+v] = v

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

        print("---------------")
        print(grid)
        print("---------------")

        # If we want to animate the simulation, yield the grid for every step
        if animate:
            yield grid

grids = simulate(False)
def print_grid(grid):
    print("---------------")
    print(grid)
    print("---------------")

[print_grid(grid) for grid in grids]













