"""
Simple animation of the highway

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic import simulate


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,



grids = simulate(animate=True)
grid = next(grids)
fig, ax = plt.subplots()
x = np.arange(0, 100)
y = np.arange(0, 10)

data = np.random.rand(2, 25)

row_heights = [0.45, 0.5, 0.55]

for row_height in row_heights:
    l, = ax.plot([0, 1], [row_height, row_height])
    l, = ax.plot([0, 1], [row_height, row_height])
    l, = ax.plot([0, 1], [row_height, row_height])


# Scale to plot 0 - 1

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')


def plot_grid(grid):
    lines = []
    for i in range(grid.shape[0]):
        row = grid[i]
        row_height = row_heights[i]
        column_coordinates, = np.where(row != -1)
        column_coordinates = column_coordinates / row.shape[0]
        print(column_coordinates, np.full(column_coordinates.shape[0], row_height))
        line, = ax.plot(column_coordinates, np.full(column_coordinates.shape[0], row_height), 'bo')
        lines.append(line)

    return (*lines),

line_ani = animation.FuncAnimation(fig, plot_grid, grids, fargs=(),
                                   interval=500, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
