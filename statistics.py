#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.
#use: python statistics.py type steps times hour

import sys
import matplotlib.pyplot as plt
import os
import pandas as pd
from simulation import Simulation
from RoadSection import RoadSection
from CreateRoads import CreateRoads
from car import Car

if len(sys.argv) < 5:
    raise Exception('Missing arguments {type} {steps} {times} {hour} {?sim_24hours}')

if int(sys.argv[5]) < 0 or int(sys.argv[5]) > 1:
    raise Exception('sim_ 24 only works with argument 0 or 1')

type = int(sys.argv[1])
steps = int(sys.argv[2])
times = int(sys.argv[3])
hour = int(sys.argv[4]) % 24

sim_24hours = False
if len(sys.argv) >= 6:
    sim_24hours = int(sys.argv[5])

def original_road(steps):
    simulation = CreateRoads.original_road(steps)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

def new_road(steps):
    simulation = CreateRoads.new_road(steps,calculate_average_speed=True)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

def self_made_road(steps):
    simulation = CreateRoads.new_design_road(steps, True)
    for road in simulation.roads:
        if road.spawn:
            calculate_road_probabilities(road, hour)
    result = simulation.run()

    [0 for r in result]

    return simulation

def calculate_density(roads, places):
    amount_cars = 0
    for i in range(len(roads)):
        amount_cars += len(roads[i].cars)
    return amount_cars/(places*5)

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
    probabilities = road.spawn_probabilities
    directions = [0.33]
    if road.name == 'R1':
        text_file_directions = open("directions.csv", "r")
        text_file_spawn = open("spawn.csv", "r")
    else:
        text_file_directions = open("directions2.csv", "r")
        text_file_spawn = open("spawn2.csv", "r")

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

def plot_multiple_runs(hour, z):
    average_speed_array = [0]*24
    if sim_24hours:
        for i in range(len(z)):
            average_speed_array[i%24] += z[i]
        print(times)
        average_speed_array[:] = [x / (times/24) for x in average_speed_array]
    else:
        average_speed_array = z
    average_speed_array[:] = [x * 20 for x in average_speed_array]
    print(average_speed_array)
    x = range(len(average_speed_array))
    plt.bar(x,average_speed_array, 0.93, color='blue')
    plt.ylim([0,100])
    x_range = times
    if sim_24hours:
        x_range = 24
    plt.xlim([0,x_range])
    plt.show()

if sim_24hours == 1:
    times *= 24


def calculate_average_speed(simulation):
    average_speeds = {'average_speed:{}'.format(road.name): road.average_speed / simulation.step for road in simulation.roads}
    average_speeds['total_average_speed'] = sum(average_speeds.values()) / len(simulation.roads)

    return average_speeds


def create_result_table(simulations):
    df = pd.DataFrame(columns=['total_output', 'density'], index=simulations.keys())
    for hour, simulation in simulations.items():
        total_output = sum([r.finished_cars for r in simulation.roads if r.is_end_road])
        df.set_value(hour, 'total_output', total_output)

        # TODO: Fix density calculation...
        density = calculate_density(simulation.roads, 100)
        df.set_value(hour, 'density', density)

        average_speeds = calculate_average_speed(simulation)
        for column, value in average_speeds.items():
            df.set_value(hour, column, value)

    print(df)
    dir = './results/'
    path = './results/results.csv'
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(path)


if type == 0:
    simulations = {}
    for i in range(times):
        if sim_24hours == 1:
            hour = i % 24
        simulation = original_road(steps)
        simulations[hour] = simulation
        #calculate_car_difference(simulation)
        roads = simulation.roads
        flow = roads[0].finished_cars/steps
        density = calculate_density(roads, 100)
        #print("Average speed R2", roads[0].average_speed/steps)
        #print(hour)
        if i == 0:
            print("Average speed R2", roads[0].average_speed/steps)
            print("Ammount of cars finished R2", roads[0].finished_cars)
            print("Flow of system", flow)
            print("Density of system (cars/meter)", density)
        x.append(density)
        y.append(flow)
        z.append(roads[0].average_speed/steps)

    create_result_table(simulations)
    plot_multiple_runs(hour, z)
elif type == 2:
    simulations = {}
    for i in range(times):
        if sim_24hours == 1:
            hour = i % 24
        simulation = new_road(steps)
        simulations[hour] = simulation
        roads = simulation.roads
        r1 = roads[0]
        r2 = roads[1]
        r5 = roads[2]
        r6 = roads[3]
        r7 = roads[4]
        r8 = roads[5]
        r9 = roads[6]
        r10 = roads[7]

        # Car difference
        calculate_car_difference(simulation)

        flow = (r5.finished_cars + r7.finished_cars + r10.finished_cars)/steps
        density = calculate_density(roads, 460)
        if i == 0:
            average_speed_r1 = r1.average_speed/steps
            average_speed_r2 = r2.average_speed/steps
            average_speed_r5 = r5.average_speed/steps
            average_speed_r6 = r6.average_speed/steps
            average_speed_r7 = r7.average_speed/steps
            average_speed_r8 = r8.average_speed/steps
            average_speed_r9 = r9.average_speed/steps
            average_speed_r10 = r10.average_speed/steps

            average_speed = (r1.average_speed/steps + r2.average_speed/steps +
                            r5.average_speed/steps + r6.average_speed/steps +
                            r7.average_speed/steps + r8.average_speed/steps +
                            r9.average_speed/steps + r10.average_speed/steps) / 8

            print("Average speed R1", average_speed_r1)
            print("Average speed R2", average_speed_r2)
            print("Average speed R5", average_speed_r5)
            print("Average speed R6", average_speed_r6)
            print("Average speed R7", average_speed_r7)
            print("Average speed R8", average_speed_r8)
            print("Average speed R9", average_speed_r9)
            print("Average speed R10", average_speed_r10)

            print("Total average speed", average_speed)
            print("Ammount of cars finished R5", r5.finished_cars)
            print("Ammount of cars finished R7", r7.finished_cars)
            print("Ammount of cars finished R10", r10.finished_cars)
            print("Flow of system", flow)
            print("Density of system (cars/meter)", density)
        x.append(density)
        y.append(flow)

    create_result_table(simulations)
elif type == 3:
    road1 = RoadSection(1, 10)
    road2 = RoadSection(2, 10, is_end_road=True)
    road1.cars = {
        55: Car(55, 5, 1, 1, (0, 8))
    }
    road2.cars = {
        33: Car(33, 2, 1, 1, (0,0)),
    }
    road2.grid[0,0] = 33
    road1.grid[0,8] = 55

    road1.set_output_mapping({
        0: (road2, 1)
    })

    road2.set_input_mapping({
        1: (road1, 0)
    })

    simulation = Simulation(road1, [road2], 1)
    print(road1.grid)
    print("----------")
    print(road2.grid)
    print("----------")
    result = simulation.run()
    [0 for r in result]
    print("----------")
#print(['{}, {}'.format(c.index, c.position) for k,c in road.cars.items()])
    print(road1.grid)
    print("----------")
    print(road2.grid)
#self-made road
else:
    for i in range(times):
        simulation = self_made_road(steps)
        roads = simulation.roads
        r1 = roads[0]
        r2 = roads[1]
        r3 = roads[2]
        r4 = roads[4]
        r5 = roads[5]
        r6 = roads[6]
        r7 = roads[3]
        r8 = roads[7]

        # Car difference
        calculate_car_difference(simulation)

        flow = (r7.finished_cars + r8.finished_cars)/steps
        density = calculate_density(roads, 460)
        if i == 0:
            average_speed_r1 = r1.average_speed/steps
            average_speed_r2 = r2.average_speed/steps
            average_speed_r3 = r3.average_speed/steps
            average_speed_r4 = r4.average_speed/steps
            average_speed_r5 = r5.average_speed/steps
            average_speed_r6 = r6.average_speed/steps
            average_speed_r7 = r7.average_speed/steps
            average_speed_r8 = r8.average_speed/steps

            average_speed = (r1.average_speed/steps + r2.average_speed/steps +
                            r3.average_speed/steps + r4.average_speed/steps +
                            r5.average_speed/steps + r6.average_speed/steps +
                            r7.average_speed/steps + r8.average_speed/steps) / 8

            print("Average speed R1", average_speed_r1)
            print("Average speed R2", average_speed_r2)
            print("Average speed R3", average_speed_r3)
            print("Average speed R4", average_speed_r4)
            print("Average speed R5", average_speed_r5)
            print("Average speed R6", average_speed_r6)
            print("Average speed R7", average_speed_r7)
            print("Average speed R8", average_speed_r8)

            print("Total average speed", average_speed)
            print("Ammount of cars finished R7", r7.finished_cars)
            print("Ammount of cars finished R8", r8.finished_cars)
            print("Flow of system", flow)
            print("Density of system (cars/meter)", density)
        x.append(density)
        y.append(flow)



plt.plot(x, y, "o")
plt.xlabel("Density (cars/meters)")
plt.ylabel("Flow (cars/step)")
#plt.show()















