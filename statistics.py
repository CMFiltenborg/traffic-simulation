#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.
#use: python statistics.py type ammount

import sys
from simulation import Simulation
from RoadSection import RoadSection

type, ammount = int(sys.argv[1]), int(sys.argv[2])

#original road
if type == 0:
    r1 = RoadSection(2, 100, name='R1')
    r2 = RoadSection(5, 100, is_end_road=True, name='R2', spawn=True)

    outputMap = {
        0: 3,  # Lane 1 corresponds with lane 5.
        1: 4   # Lane 2 corresponds with lane 5.
    }

    r1.set_output_mapping(outputMap)

    simulation = Simulation(r2, [], ammount, 1)
    result = simulation.run()
    
    [0 for r in result]
    
    print("Average speed R2", r2.average_speed/ammount)
    print("Ammount of cars finished R2", r2.finished_cars)
    print("Flow of system", r2.finished_cars/ammount)
    print("Density of system", "probabilty of cars generated")
#print([r[i].average_speed for r in result for i in r])
#self-made road
else:
    r1 = RoadSection(4, 20, name='R1', spawn=True)
    r2 = RoadSection(2, 40, name='R2')
    r3 = RoadSection(2, 100, name='R3')
    r4 = RoadSection(2, 40, name='R4', spawn=True)
    r5 = RoadSection(1, 20, name='R5')
    r6 = RoadSection(1, 120, name='R6')
    r7 = RoadSection(3, 80, is_end_road=True, name='R7')
    r8 = RoadSection(3, 40, is_end_road=True, name='R8')


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

    simulation = Simulation(r1, [r2, r3, r7, r4, r5, r6, r8], ammount, 1)
    result = simulation.run()

    [0 for r in result]

    average_speed_r1 = r1.average_speed/ammount
    average_speed_r2 = r2.average_speed/ammount
    average_speed_r3 = r3.average_speed/ammount
    average_speed_r4 = r4.average_speed/ammount
    average_speed_r5 = r5.average_speed/ammount
    average_speed_r6 = r6.average_speed/ammount
    average_speed_r7 = r7.average_speed/ammount
    average_speed_r8 = r8.average_speed/ammount
    
    average_speed = (r1.average_speed/ammount + r2.average_speed/ammount +
                    r3.average_speed/ammount + r4.average_speed/ammount +
                    r5.average_speed/ammount + r6.average_speed/ammount +
                    r7.average_speed/ammount + r8.average_speed/ammount) / 8
    

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
    print("Flow of system", (r7.finished_cars + r8.finished_cars)/ammount)
    print("Density of system", "probabilty of cars generated")
























