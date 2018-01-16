"""
Simple animation of the highway

"""

import matplotlib

from simulation import Simulation

matplotlib.use('TKAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic import simulate, print_grid
from RoadSection import RoadSection
import pylab as pl


r1 = RoadSection(4, 20, name='R1')
r2 = RoadSection(2, 40, name='R2')
r3 = RoadSection(2, 100, name='R3')
r4 = RoadSection(2, 40, name='R4')
r5 = RoadSection(1, 20, name='R5')
r6 = RoadSection(1, 120, name='R6')
r7 = RoadSection(3, 80, is_end_road=True, name='R7')
r8 = RoadSection(3, 40, is_end_road=True, name='R8')


r1.set_output_mapping({
    0: (r3, 0),
    1: (r3, 1),
    2: (r2, 0),
    3: (r2, 1),
})
r2.set_output_mapping({
    0: (r8, 0),
    1: (r8, 1),
})
r3.set_output_mapping({
    0: (r7, 0),
    1: (r7, 1),
})
r4.set_output_mapping({
    0: (r5, 0),
    1: (r6, 0),
})
r5.set_output_mapping({
    0: (r8, 2),
})
r6.set_output_mapping({
    0: (r7, 2),
})
# r7.set_output_mapping({
#     0: (r7, 2),
#     1: (r7, 2),
# })


simulation = Simulation(r1, [r2, r3, r4, r5, r6, r7, r8], 100)
result = simulation.run()

# config = {
#     'rows': 5,
#     'columns': 100,
#     'step': 100,
# }
# states = simulate(config)

sections = next(result)
number_of_roads = 1
fig, axes = plt.subplots(nrows=1, ncols=8, sharey=True)
# axes = [axes]
# row_heights = {}
# row_heights = {
#     0: np.linspace(0.7, 0.4, 5)[3:5],
#     1: np.linspace(0.7, 0.4, 5)
# }
row_heights = {
    0: [0.4, 0.5],
    1: [0.4, 0.5],
    2: [0.4],
}
# print(axes)

axes = np.array(axes).flatten()
for i in sections:
    # more_axes = axes[i]
    # for j in more_axes:
    ax = axes[i]

    grid, cars = sections[i]
    # Create lines for every row in the grid, the 'highways'
    row_heights[i] = np.linspace(0.7, 0.3, grid.shape[0])
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
        # print_grid(sections[i])
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
                                   interval=1000 / 4, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
