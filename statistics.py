#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.
#use: python statistics.py type steps times hour

import sys
import matplotlib.pyplot as plt
import os
import pandas as pd
import time

from CreateRoads import CreateRoads
from simulation import Simulation
from RoadSection import RoadSection
from car import Car
import numpy as np
from multiprocessing import Pool


def original_road(steps, hour):
    simulation = CreateRoads.original_road(steps)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

def new_road(steps, hour):
    simulation = CreateRoads.new_road(steps,calculate_average_speed=True)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

def self_made_road(steps, hour):
    simulation = CreateRoads.new_design_road(steps, True)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

x, y, z = [], [], []


def calculate_car_difference(simulation):
    generated_cars = simulation.generated_cars
    cars_still_on_roads = 0
    roads = simulation.roads
    finished_cars = sum([road.finished_cars for road in roads if road.is_end_road])

    for road in roads:
        coords = road.get_car_coordinates()
        cars_still_on_roads += len(coords[0])

    difference = generated_cars - (finished_cars + cars_still_on_roads)
    print('Cars generated:{} Car:{} difference between generated and finished/still on road'.format(generated_cars, difference))


def calculate_road_probabilities(road, hour):
    """
    Sets the road spawn probabilities
    :param road: RoadSection
    :param hour: hour 0-23
    """
    probabilities = road.spawn_probabilities

    if road.name == 'R1':
        text_file_directions = open("directions.csv", "r")
        text_file_spawn = open("spawn.csv", "r")
    else:
        text_file_directions = open("directions2.csv", "r")
        text_file_spawn = open("spawn2.csv", "r")
    # else:
    #     if road.name == 'R1':
    #         text_file_directions = open("directions.csv", "r")
    #         text_file_spawn = open("spawn.csv", "r")
    #     else:
    #         text_file_directions = open("directions2.csv", "r")
    #         text_file_spawn = open("spawn2.csv", "r")

    lines_direction = text_file_directions.readlines()
    directions = lines_direction[hour].rstrip().replace(" ","").split(';')
    for prob in directions:
        if (int)(prob[0]) < road.rows:
            (key, value) = prob.split(':')
            probabilities[2][int(key)] = tuple(map(float,value.split(',')))

    lines_spawn = text_file_spawn.readlines()
    spawns = lines_spawn[hour].rstrip().replace(" ","").split(';')
    for prob in spawns:
        (key, value) = prob.split(':')
        probabilities[0][int(key)] = float(value)
    text_file_directions.close()
    text_file_spawn.close()


def calculate_average_speed(simulation):
    number_roads_cars_driven = 0
    for road in simulation.roads:
        if road.average_speed > 0:
            number_roads_cars_driven += 1

    average_speeds = {'average_speed:{}'.format(road.name): road.average_speed / road.average_speed_steps for road in simulation.roads}
    average_speeds['total_average_speed'] = sum(average_speeds.values()) / number_roads_cars_driven

    return average_speeds


def create_result_table(simulations, type, run_number):
    """
    Create a result table from 24 simulations, and save it as a csv.
    :param simulations:
    :param type:
    :param run_number:
    """
    df = pd.DataFrame(columns=['total_output', 'density', 'generated_cars', 'flow'], index=simulations.keys())
    for hour, simulation in simulations.items():
        # Add total output of cars
        total_output = sum([r.finished_cars for r in simulation.roads if r.is_end_road])
        df.set_value(hour, 'total_output', total_output)

        # Calculates percentage of cars to Utrecht in road type = 2
        for r in simulation.roads:
            if r.name == 'R10':
                percentage_to_Utrecht = r.finished_cars / total_output
                df.set_value(hour, '%_to_Utrecht', percentage_to_Utrecht)

        # Add flow
        flow = total_output / simulation.step
        df.set_value(hour, 'flow', flow)

        # Add density
        density = np.average(simulation.densities)
        df.set_value(hour, 'density', density)

        # Add generated cars
        generated_cars = simulation.generated_cars
        df.set_value(hour, 'generated_cars', generated_cars)


        average_speeds = calculate_average_speed(simulation)
        for column, value in average_speeds.items():
            df.set_value(hour, column, value)

    dir = './results/type_{}/'.format(type)
    path = dir + 'results_{}.csv'.format(run_number)
    if not os.path.exists(dir):
        os.makedirs(dir)

    df['hour'] = df.index
    df.to_csv(path, index=False)


def run_simulation(i):
    t0 = time.time()
    simulations = {}
    for hour in range(0, 24):
        simulation = road_fn(steps, hour)
        simulations[hour] = simulation
        print('Simulation:{} Hour:{}'.format(i, hour))

    create_result_table(simulations, type=road_type, run_number=i)
    t1 = time.time()
    total = t1 - t0
    print('Simulation run: {} [0-24 hours], Time:{}'.format(i, total))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise Exception('Missing arguments {type} {steps} {times}')

    road_type = int(sys.argv[1])  # Type of road
    steps = int(sys.argv[2])  # Amount of steps to run per simulation
    times = int(sys.argv[3])  # Amount of times we want to run the simulations * 24
    print('Running road_type:{}, steps:{}, times:{}'.format(road_type, steps, times))

    # Determine the type of road we want to create
    road_fn = None
    if road_type == 0:
        road_fn = original_road
    if road_type == 2:
        road_fn = new_road

    if road_fn is None:
        raise Exception('No valid road type')

    # Run 24 simulations (24-hour) in parallel
    with Pool(4) as p:
        p.map(run_simulation, range(times+1))















