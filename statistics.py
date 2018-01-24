#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.
#use: python statistics.py type steps times hour

import sys
import matplotlib.pyplot as plt
from simulation import Simulation
from RoadSection import RoadSection
from CreateRoads import CreateRoads
from car import Car

type, steps, times, hour = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), (int(sys.argv[4]) % 24)

def original_road(steps):
    simulation = CreateRoads.original_road(steps)
    for road in simulation.roads:
        if road.spawn != None:
            calculate_road_probabilities(road, hour)
    result = simulation.run()
    
    [0 for r in result]

    return simulation

def self_made_road(steps):
    simulation = CreateRoads.new_design_road(steps, True)
    result = simulation.run()

    [0 for r in result]

    return simulation

def calculate_density(roads, places):
    ammount_cars = 0
    for i in range(len(roads)):
        ammount_cars += len(roads[i].cars)
    return ammount_cars/(places*5)

x, y = [], []


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
    print("hour", hour)
    print(probabilities[2])
    directions = [0.33]
    text_file = open("directions.csv", "r")
    lines = text_file.readlines()
    directions = lines[hour].rstrip().replace(" ","").split(';')
    for prob in directions:
        (key, value) = prob.split(':')

        probabilities[2][int(key)] = tuple(map(float,value.split(',')))
        print(probabilities[2])
    print("------")
    text_file.close()


#original road
if type == 0:
    for i in range(times):
        simulation = original_road(steps)
        calculate_car_difference(simulation)
        roads = simulation.roads
        flow = roads[0].finished_cars/steps
        density = calculate_density(roads, 100)
        if i == 0:
            print("Average speed R2", roads[0].average_speed/steps)
            print("Ammount of cars finished R2", roads[0].finished_cars)
            print("Flow of system", flow)
            print("Density of system (cars/meter)", density)
        x.append(density)
        y.append(flow)
elif type == 2:
    road = RoadSection(3, 10)
    road.cars = {
        0: Car(0, 2, 1, 1, (0,3)),
        1: Car(1, 5, 1, 1, (1,1))
    }
    road.grid[0,3] = 0
    road.grid[1,1] = 1
    simulation = Simulation(road, [], 1)
    print(road.grid)
    print("----------")
    result = simulation.run()
    [0 for r in result]
    print("----------")
    print(road.grid)
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















