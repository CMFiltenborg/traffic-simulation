# Computational science project - traffic flow
# Lukas, Martijn, Lennart, Max
# 10783687, 11922419, 10432973, 11042729

# This file shows a simulation of the original road created in CreateRoads.

import matplotlib

from CreateRoads import CreateRoads
from simulation import Simulation

matplotlib.use('TKAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RoadSection import RoadSection
import pylab as pl


simulation = CreateRoads.original_road(100)
result = simulation.run()

sections = next(result)
fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True)
row_heights = {
    0: np.linspace(0.7, 0.4, 6)
}

dotted_lines = [
    # Main-road
    (-0.15, 0, 0.7, 0.7, 'b'),
    (-0.15, 0, 0.64, 0.64, 'b'),
    (-0.15, 0, 0.58, 0.58, 'b'),
    (-0.15, 0, 0.52, 0.52, 'b'),
    (-0.15, 0, 0.46, 0.46, 'b'),

    # Oprid
    (-0.15, 0, 0.40, 0.46, 'b'),
    (-0.15, 0, 0.34, 0.4, 'b'),

    # Vervolg ring
    (1, 1.15, 0.7, 0.75, 'r'),
    (1, 1.15, 0.64, 0.69, 'r'),
    (1, 1.15, 0.58, 0.63, 'r'),
    (1, 1.15, 0.52, 0.57, 'r'),

    # Richting Utrecht
    (1, 1.15, 0.52, 0.47, 'k'),
    (1, 1.15, 0.46, 0.41, 'k'),
    (1, 1.15, 0.40, 0.35, 'k'),
]

for i in sections:
    road_section = sections[i]
    grid = road_section.grid
    cars = road_section.cars
    # Create lines for every row in the grid, the 'highways'
    for row_height in row_heights[i]:
        l, = ax.plot([0, 1], [row_height, row_height], color='black')

    # Scale to plot 0 - 1
    plt.xlim(-0.1, 1.1)
    plt.ylim(0, 1)
    plt.xlabel('Position')
    plt.title('Highway simulation')


def plot_grid(sections):

    for position in dotted_lines:

        x1, x2, y1, y2, color = position
        style = color + '--'
        ax.plot([x1, x2], [y1, y2], style)

    markers = []
    for i in sections:
        road_section = sections[i]
        grid = road_section.grid
        cars = road_section.cars
        for j in range(grid.shape[0]):
            row = grid[j]

            # Determines y placement
            row_height = (row_heights[i][j] + row_heights[i][j+1]) / 2
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
