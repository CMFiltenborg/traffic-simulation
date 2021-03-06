# Computational science project - traffic flow
# Lukas, Martijn, Lennart, Max
# 10783687, 11922419, 10432973, 11042729

import numpy as np
import copy
import sys

from car import Car


class RoadSection:
    def __init__(self, rows, columns, is_end_road=False, name=None, right_lane=0, spawn_probabilities=None, output_colors=[]):
        """
        Rows is the amount of lanes
        Columns is the length of the road
        """
        if right_lane == 0:
            right_lane = rows
        if len(output_colors) == 0:
            output_colors = ['blue']*rows
        self.name = name
        self.rows = rows
        self.right_lane = right_lane
        self.columns = columns
        self.grid = np.full((rows, columns),  -1, dtype=np.int32)
        self.grid_temp = None
        self.average_speed = 0
        self.average_speed_steps = 0
        self.spawn_probabilities = spawn_probabilities
        self.spawn = spawn_probabilities is not None
        self.start_road = self.spawn

        self.input_map = None
        self.output_map = None
        self.cars = {}
        self.updates = {}
        self.new_car_updates = {}
        self.output_colors = output_colors
        self.is_end_road = is_end_road

        self.finished_cars = 0

        self.blocks = -2
        for i in range(right_lane,rows):
            new_car_index = self.blocks
            self.blocks -= 1
            self.cars[new_car_index] = Car(new_car_index, 0, 'white', i, (i,columns-1))
            self.grid[i][columns-1] = new_car_index

    def set_output_mapping(self, output_map):
        self.output_map = output_map

    def set_input_mapping(self, input_map):
        self.input_map = input_map

    def output_car(self, car, v):
        self.finished_cars += 1

        if self.is_end_road:
            return

        output_road, output_row = self.output_map[car.position[0]]
        output_column = car.position[1] + v - self.grid.shape[1]

        car.direction = np.random.randint(0, output_road.right_lane)

        output_road.add_car(car, output_row, output_column, v, self)

    def set_temp_grid(self):
        self.grid_temp = copy.deepcopy(self.grid)

    def get_car_coordinates(self):
        return np.where(self.grid > -1)

    def add_car(self, car, row, column, v, prev_road):
        self.new_car_updates[car.index] = (car, v, (row, column), prev_road)

    def add_new_cars(self):
        for index, y in self.new_car_updates.items():
            del y[3].cars[index]

            self.cars[index] = y[0]
            self.cars[index].set_speed(y[1])
            self.cars[index].set_position(y[2])

            row, column = y[2]
            if self.grid[row, column] != -1:
                print("Ocupied", row, column, y[0].index)
                print("-------------")
                print(self.grid)
                print("-------------")
                print(self.grid_temp)
                sys.exit("Dissapearing car")
            self.grid[row, column] = index

        self.new_car_updates = {}
