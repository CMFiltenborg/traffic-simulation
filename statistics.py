#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.
#use: python statistics.py type steps times

import sys
import matplotlib.pyplot as plt
from simulation import Simulation
from RoadSection import RoadSection
from CreateRoads import CreateRoads

type, steps, times = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

def original_road(steps):
    simulation = CreateRoads.original_road(steps)
    result = simulation.run()
    
    [0 for r in result]

    return simulation.roads

def self_made_road(steps):
    simulation = CreateRoads.new_design_road(steps, True)
    result = simulation.run()

    [0 for r in result]

    return simulation.roads

def calculate_density(roads, places):
    ammount_cars = 0
    for i in range(len(roads)):
        ammount_cars += len(roads[i].cars)
    return ammount_cars/(places*5)

x, y = [], []
#original road
if type == 0:
    for i in range(times):
        roads = original_road(steps)
        flow = roads[0].finished_cars/steps
        density = calculate_density(roads, 100)
        if i == 0:
            print("Average speed R2", roads[0].average_speed/steps)
            print("Ammount of cars finished R2", roads[0].finished_cars)
            print("Flow of system", flow)
            print("Density of system (cars/meter)", density)
        x.append(density)
        y.append(flow)

#self-made road
else:
    for i in range(times):
        roads = self_made_road(steps)
        r1 = roads[0]
        r2 = roads[1]
        r3 = roads[2]
        r4 = roads[4]
        r5 = roads[5]
        r6 = roads[6]
        r7 = roads[3]
        r8 = roads[7]
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
plt.show()















