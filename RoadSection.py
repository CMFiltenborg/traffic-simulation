import numpy as np
import copy

from car import Car


class RoadSection:
    def __init__(self, rows, columns, is_end_road=False, name=None):
        """
        Rows is the amount of lanes
        Columns is the length of the road
        """
        self.name = name
        self.rows = rows
        self.columns = columns
        self.grid = np.full((rows, columns),  -1, dtype=np.int32)
        self.grid_temp = None
        self.average_speed  = 0

        self.input_road = None
        self.input_map = None
        self.output_map = None
        self.cars = {}
        self.updates = {}
        self.new_car_updates = {}

        self.is_end_road = is_end_road

        self.finished_cars = 0

    def set_output_mapping(self, output_map):
        self.output_map = output_map
    
    def set_input_mapping(self, input_road):
        self.input_road = input_road
        self.input_map = {v: k for k, v in self.input_road.output_map.items()}

    def output_car(self, car, v):
        self.finished_cars += 1

        del self.cars[car.index]
        if self.is_end_road:
            return

        output_road, output_row = self.output_map[car.position[0]]
        output_column = car.position[1] + v - self.grid.shape[1]

        car.direction = np.random.randint(0, output_road.rows)

        #print('Output car', (output_row, output_column))
        output_road.add_car(car, output_row, output_column, v)

    def set_temp_grid(self):
        self.grid_temp = copy.deepcopy(self.grid)

    def get_car_coordinates(self):
        return np.where(self.grid != -1)

    def add_car(self, car, row, column, v):

        self.new_car_updates[car.index] = (car, v, (row, column))

        # self.cars[car.index] = car

    def add_new_cars(self):
        for index, y in self.new_car_updates.items():
            self.cars[index] = y[0]
            self.cars[index].set_speed(y[1])
            self.cars[index].set_position(y[2])

            row, column = y[2]
            self.grid[row][column] = index

        self.new_car_updates = {}




