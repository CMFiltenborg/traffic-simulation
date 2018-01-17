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


r1 = RoadSection(4, 20, name='R1', spawn=True)
r2 = RoadSection(2, 40, name='R2')
r3 = RoadSection(2, 100, name='R3')
r4 = RoadSection(2, 40, name='R4', spawn=True)
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



x1 = 10
x2 = 30
y1 = 110
y2 = 110

dotted_lines = [
    # 1 - 3
    (x1, x2, y1, y2, 'r'),
    (x1, x2, 100, 100, 'r'),
    (x1, x2, 90, 90, 'r'),

    # 1 - 2
    (x1, x2, 90, 70, 'r'),
    (x1, x2, 80, 60, 'r'),
    (x1, x2, 70, 50, 'r'),

    # 4 - 5
    (20, 40, 30, 40, 'r'),
    (20, 40, 20, 30, 'r'),

    # 4 - 6
    (20, 40, 20, 20, 'r'),
    (20, 40, 10, 10, 'r'),

    # 6 - 7
    (100, 140, 20, 90, 'g'),
    (100, 140, 10, 80, 'g'),

    # 3 - 7
    (80, 140, 110, 110, 'r'),
    (80, 140, 100, 100, 'r'),
    (80, 140, 90, 90, 'r'),

    # 2 - 8
    (50, 160, 70, 40, 'r'),
    (50, 160, 60, 30, 'r'),
    (50, 160, 50, 20, 'r'),

    # 5 - 8
    (50, 160, 40, 20, 'r'),
    (50, 160, 30, 10, 'r'),
]

placements = {
    # 'R1': ((0.5, 0.5), [0.7, 0.6, 0.5, 0.4]),
    'R1': ([0, 10], [110, 100, 90, 80, 70]),
    'R2': ([30, 50], [70, 60, 50]),
    'R3': ([30, 80], [110, 100, 90]),
    'R4': ([0, 20], [30, 20, 10]),
    'R5': ([40, 50], [40, 30]),
    'R6': ([40, 100], [20, 10]),
    'R7': ([140, 180], [110, 100, 90, 80]),
    'R8': ([160, 180], [40, 30, 20, 10]),
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
                x_placement = road_section_x_placement + column * 0.5
                marker, = ax.plot(x_placement, y_height, color=cars[car_index].color, marker='o')
                text = ax.text(x_placement, y_height, str(cars[car_index].index), color="red", fontsize=12)
                markers.append(marker)
                markers.append(text)

    return (*markers),  # Unpack all the new markers

plot_lines(sections)
line_ani = animation.FuncAnimation(fig, plot_grid, result, fargs=(),
                                   interval=1000 / 4, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()
