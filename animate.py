"""
Simple animation of the highway

"""

import matplotlib
matplotlib.use('TKAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic import simulate, print_grid




config = {
    'rows': 5,
    'columns': 100,
    'step': 100,
}

states = simulate(config)
grid, cars = next(states)

fig, ax = plt.subplots()
data = np.random.rand(2, 25)

# Create lines for every row in the grid, the 'highways'
row_heights = np.linspace(0.3, 0.7, grid.shape[0])
for row_height in row_heights:
    l, = ax.plot([0, 1], [row_height, row_height], color='black')

# Scale to plot 0 - 1
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('Position')
plt.title('Highway simulation')


def plot_grid(items):
    grid, cars = items
    markers = []
    #print_grid(grid)
    for i in range(grid.shape[0]):
        row = grid[i]

        # Determines y placement
        row_height = row_heights[i]
        column_coordinates, = np.where(row != -1)

        # For every car we plot it as a marker with its own color
        for column in column_coordinates:
            car_index = row[column]
            x_placement = column / row.shape[0]  # Scale from 0 - 1
            marker, = ax.plot(x_placement, row_height, color=cars[car_index].color, marker='o')
            markers.append(marker)
    
    return (*markers),  # Unpack all the new markers

line_ani = animation.FuncAnimation(fig, plot_grid, states, fargs=(),
                                   interval=250, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
