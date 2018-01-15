import numpy as np
import copy


class RoadSection:
    def __init__(self, rows, columns):
        """
        Rows is the amount of lanes
        Columns is the length of the road
        """
        self.rows = rows
        self.columns = columns
        self.grid = np.full((rows, columns),  -1, dtype=np.int32)
        self.grid_temp = None

        self.output_road = None
        self.output_map = None
        self.cars = {}
        self.updates = {}

    def set_output_mapping(self, output_road, output_map):
        self.output_road = output_road
        self.output_map = output_map

    def set_temp_grid(self):
        self.grid_temp = copy.deepcopy(self.grid)

    def get_car_coordinates(self):
        return np.where(self.grid != -1)




