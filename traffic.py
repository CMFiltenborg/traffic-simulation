#Computational science project
#Lukas, Martijn, Lennard, Max
#10783687,,,

import numpy as np

grid = np.full((3,10),  -1, dtype=np.int32)
step = 100
auto = 1

'''
grid[2][3] = 3
grid[2][2] = 2
print(np.where(grid != -1))
'''

for i in range(step):
    coordinates = np.where(grid != -1)
    for j in range(len(coordinates[0])):
        if incentive:
        
        else:
            #nagel-schreckenberg
    #generate auto
    for j in range(auto):
        x = np.random.randint(0, 3)
        y = np.random.randint(0, 10)
        v = np.random.randint(1, 6)
        grid[x][y] = v
