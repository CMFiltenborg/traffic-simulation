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
pv = 0.5


'''
grid[2][3] = 3
grid[2][2] = 2
print(np.where(grid != -1))
'''

def simulate(animate=False):
    print("hoi")
    for i in range(step):
        coordinates = np.where(grid != -1)
        for j in range(len(coordinates[0])):
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
                        if grid[r][c+k] == -1:
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
            r = np.random.randint(0, 3)
            v = np.random.randint(1, 6)
            grid[r][0] = v

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













