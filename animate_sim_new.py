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


spawn_r1 = [
    {0:0.5, 1:0.2, 2:0.2, 3:0.2,},
    {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
]
spawn_r4 = [
    {0:0.2, 1:0.2,},
    {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
]
r1 = RoadSection(4, 20, name='R1', spawn_probabilities=spawn_r1)
r2 = RoadSection(2, 40, name='R2')
r3 = RoadSection(2, 100, name='R3')
r4 = RoadSection(2, 40, name='R4', spawn_probabilities=spawn_r4)
r5 = RoadSection(1, 20, name='R5')
r6 = RoadSection(1, 120, name='R6')
r7 = RoadSection(3, 80, is_end_road=True, name='R7', rightLane=2)
r8 = RoadSection(3, 40, is_end_road=True, name='R8', rightLane=2)

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


simulation = Simulation(r1, [r2, r3, r7, r4, r5, r6, r8], 1000, 1)
result = simulation.run()

sections = next(result)

row_heights = {
    'R1': [0.7, 0.6, 0.5, 0.4],
    'R2': [0.5, 0.4],
    'R3': [0.7, 0.6],
    'R4': [0.6, 0.5],
    'R5': [0.6],
    'R6': [0.5],
    'R7': [0.7, 0.6, 0.5],
    'R8': [0.7, 0.6, 0.5],
}

fig, axes = plt.subplots(nrows=2, ncols=4, sharey=True)
axes = np.array(axes).flatten()


def plot_lines(sections):
    lines = []
    for i in sections:
        # more_axes = axes[i]
        # for j in more_axes:
        ax = axes[i]

        road_section = sections[i]
        grid = road_section.grid
        cars = road_section.cars

        title = '{}: {}'.format(road_section.name, road_section.columns)
        ax.title.set_text(title)
        # Create lines for every row in the grid, the 'highways'
        # row_heights[i] = np.linspace(0.7, 0.3, grid.shape[0])
        for row_height in row_heights[road_section.name]:
            l, = ax.plot([0, 1], [row_height, row_height], color='black')
            lines.append(l)

    return lines

# Scale to plot 0 - 1
plt.xlim(0, 1)
plt.ylim(0, 1)
# plt.xlabel('Position')
# plt.title('Highway simulation')


def plot_grid(sections):
    lines = plot_lines(sections)

    markers = lines
    for i in sections:
        road_section = sections[i]
        grid = road_section.grid
        cars = road_section.cars
        ax = axes[i]
        # print_grid(sections[i])
        for j in range(grid.shape[0]):
            row = grid[j]

            # Determines y placement
            row_height = row_heights[road_section.name][j]
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

plot_lines(sections)
line_ani = animation.FuncAnimation(fig, plot_grid, result, fargs=(),
                                   interval=1000 / 4, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
