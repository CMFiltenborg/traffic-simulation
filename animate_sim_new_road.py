# Computational science project - traffic flow
# Lukas, Martijn, Lennart, Max
# 10783687, 11922419, 10432973, 11042729

# This file shows a simulation of the new road created in CreateRoads.

import matplotlib

from CreateRoads import CreateRoads
from simulation import Simulation

# fix for blit issue mac
matplotlib.use('TKAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RoadSection import RoadSection
import pylab as pl

simulation = CreateRoads.new_road(100)
result = simulation.run()

sections = next(result)


dotted_lines = [
    #1-5
    (30, 140, 110, 110, 'r'),
    (30, 140, 100, 100, 'r'),
    (30, 140, 90, 90, 'r'),
                
    #1-9
    (30, 120, 90, 60, 'r'),
    (30, 120, 80, 50, 'r'),
    (30, 120, 70, 40, 'r'),
                
    #2-6
    (10, 30, 20, 20, 'r'),
    (10, 30, 10, 10, 'r'),
                
    #6-8
    (60, 130, 20, 20, 'r'),
    (60, 130, 10, 10, 'r'),
                
    #8-10
    (160, 180, 20, 20, 'r'),
    (160, 180, 10, 10, 'r'),
                
    #9-10
    (160, 180, 60, 40, 'r'),
    (160, 180, 50, 30, 'r'),
    (160, 180, 40, 20, 'r'),
                
    #6-7
    (60, 120, 30, 80, 'g'),
    (60, 120, 20, 70, 'g'),
    (120, 150, 80, 90, 'g'),
    (120, 150, 70, 80, 'g'),
]

arrows = [
    (191, 195, 13, 17, 'c'),
    (192, 195, 17, 17, 'c'),
    (195, 195, 15, 17, 'c'),
]

placements = {
    'R1': ([0, 30], [110, 100, 90, 80, 70]),
    'R2': ([0, 10], [20, 10]),
    'R5': ([140, 210], [110, 100, 90]),
    'R6': ([30, 60], [30, 20, 10]),
    'R7': ([150, 210], [90, 80]),
    'R8': ([130, 160], [20, 10]),
    'R9': ([120, 160], [60, 50, 40]),
    'R10': ([180, 210], [40, 30, 20, 10]),
}


fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True)


def plot_lines(sections):
    for position in dotted_lines:
        
        x1, x2, y1, y2, color = position
        style = color + '--'
        ax.plot([x1, x2], [y1, y2], style)

    for position in arrows:
        
        x1, x2, y1, y2, color = position
        style = color
        ax.plot([x1, x2], [y1, y2], style)

    lines = []
    for i in sections:
        road_section = sections[i]
        if road_section.name not in placements:
            continue
        
        placement = placements[road_section.name]
        x, ys = placement
        for y in ys:
            l, = ax.plot(x, [y, y], color='black')
            lines.append(l)

    return lines

plt.title('Highway simulation')


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
                x_placement = road_section_x_placement + column
                marker, = ax.plot(x_placement, y_height, color=cars[car_index].color, marker='o')
                text = ax.text(x_placement, y_height, str(cars[car_index].index), color="red", fontsize=12)
                markers.append(marker)
                markers.append(text)

    return (*markers),  # Unpack all the new markers

plot_lines(sections)
line_ani = animation.FuncAnimation(fig, plot_grid, result, fargs=(),
                                   interval=1000 / 20, blit=True)

# To save the animation, use the command: line_ani.save('lines.mp4')

plt.show()

