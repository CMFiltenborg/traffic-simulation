"""
Simple animation of the highway

"""

import matplotlib

from simulationBackup import Simulation

matplotlib.use('TKAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic import simulate, print_grid
from RoadSection import RoadSection
import pylab as pl


r1 = RoadSection(2, 100)
r2 = RoadSection(5, 100, True)

outputMap = {
    0: 3,  # Lane 1 corresponds with lane 5.
    1: 4   # Lane 2 corresponds with lane 5.
}

r1.set_output_mapping(r2, outputMap)

simulation = Simulation(r1, [r2], 100, True)
result = simulation.run()

# config = {
#     'rows': 5,
#     'columns': 100,
#     'step': 100,
# }
# states = simulate(config)

sections = next(result)
number_of_roads = 2
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True)

row_heights = {}
row_heights = {
    0: np.linspace(0.7, 0.4, 5)[3:5],
    1: np.linspace(0.7, 0.4, 5)
}
for i in sections:
    grid, cars = sections[i]
    ax = axes[i]
    # Create lines for every row in the grid, the 'highways'
    # row_heights[i] = np.linspace(0.7, 0.3, grid.shape[0])
    for row_height in row_heights[i]:
        l, = ax.plot([0, 1], [row_height, row_height], color='black')

    # Scale to plot 0 - 1
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('Position')
    plt.title('Highway simulation')


def plot_grid(sections):

    markers = []
    #print_grid(grid)
    for i in sections:
        grid, cars = sections[i]
        ax = axes[i]
        print_grid(sections[i])
        for j in range(grid.shape[0]):
            row = grid[j]

            # Determines y placement
            row_height = row_heights[i][j]
            column_coordinates, = np.where(row != -1)

            # For every car we plot it as a marker with its own color
            for column in column_coordinates:
                car_index = row[column]
                x_placement = column / row.shape[0]  # Scale from 0 - 1
                marker, = ax.plot(x_placement, row_height, color=cars[car_index].color, marker='o')
                text = ax.text(x_placement, row_height, str(cars[car_index].index), color="red", fontsize=12)
                markers.append(marker)
                markers.append(text)
    
    return (*markers),  # Unpack all the new markers

line_ani = animation.FuncAnimation(fig, plot_grid, result, fargs=(),
                                   interval=1000, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
