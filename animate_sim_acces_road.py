"""
Simple animation of the highway

"""

import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from CreateRoads import CreateRoads
from simulation import Simulation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic import simulate, print_grid
from RoadSection import RoadSection
import pylab as pl

simulation = CreateRoads.acces_road(100, calculate_average_speed=False)
result = simulation.run()

sections = next(result)


x1 = 10
x2 = 30
y1 = 110
y2 = 110


dotted_lines = [
    # 1 - 3
    (10, 15, 60, 60, 'r'),
    (10, 15, 50, 50, 'r'),

    # 2 - 3
    (10, 15, 40, 50, 'r'),
    (10, 15, 30, 40, 'r'),

    #arrow
    (17, 19, 43, 47, 'c'),
    (18, 19, 47, 47, 'c'),
    (19, 19, 45.5, 47, 'c'),

    #arrow
    (22, 24, 43, 47, 'c'),
    (23, 24, 47, 47, 'c'),
    (24, 24, 45.5, 47, 'c'),
]


placements = {
    # 'R1': ((0.5, 0.5), [0.7, 0.6, 0.5, 0.4]),
    'R1': ([0, 10], [60, 50]),
    'R2': ([0, 10], [40, 30]),
    'R3': ([15, 25], [60, 50, 40]),
}

fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True)


def plot_lines(sections):
    for position in dotted_lines:

        x1, x2, y1, y2, color = position
        style = color + '--'
        ax.plot([x1, x2], [y1, y2], style)

    lines = []
    for i in sections:
        # more_axes = axes[i]
        # for j in more_axes:

        road_section = sections[i]
        grid = road_section.grid
        cars = road_section.cars

        # title = '{}: {}'.format(road_section.name, road_section.columns)
        # ax.title.set_text(title)

        # Create lines for every row in the grid, the 'highways'
        # row_heights[i] = np.linspace(0.7, 0.3, grid.shape[0])
        if road_section.name not in placements:
            continue

        placement = placements[road_section.name]
        x, ys = placement
        for y in ys:
            l, = ax.plot(x, [y, y], color='black')
            lines.append(l)

    return lines

# Scale to plot 0 - 1
# plt.xlim(0, 200)
# plt.ylim(0, 100)
# plt.xlabel('Position')
# plt.title('Highway simulation')


def plot_grid(sections):
    lines = plot_lines(sections)

    markers = lines
    for i in sections:
        road_section = sections[i]
        grid = road_section.grid
        cars = road_section.cars
        # print_grid(sections[i])
        for j in range(grid.shape[0]):  
            row = grid[j]

            # Determines y placement
            placement = placements[road_section.name]
            y_height = (placement[1][j] + placement[1][j+1]) / 2
            road_section_x_placement = placements[road_section.name][0][0]

            # row_height = row_heights[road_section.name][j]
            column_coordinates, = np.where(row != -1)

            # For every car we plot it as a marker with its own color
            for column in column_coordinates:
                car_index = row[column]
                # x_placement = column / row.shape[0]  # Scale from 0 - 1
                x_placement = road_section_x_placement + column
                marker, = ax.plot(x_placement, y_height, color=cars[car_index].color, marker='o')
                text = ax.text(x_placement, y_height, str(cars[car_index].index), color="red", fontsize=12)
                markers.append(marker)
                markers.append(text)

    return (*markers),  # Unpack all the new markers

plot_lines(sections)
line_ani = animation.FuncAnimation(fig, plot_grid, result, fargs=(),
                                   interval=1000 / 1, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
