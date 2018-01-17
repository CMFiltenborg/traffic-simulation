#This file wil run one of the two scrips a given ammount of times.
#Type 0 is the original road, type 1 is theself made road.

import sys
from simulation import Simulation
from RoadSection import RoadSection

type, ammount = sys.argv[1:]

#original road
if int(type) == 0:
    r1 = RoadSection(2, 100)
    r2 = RoadSection(5, 100, True)

    outputMap = {
        0: 3,  # Lane 1 corresponds with lane 5.
        1: 4   # Lane 2 corresponds with lane 5.
    }

    r1.set_output_mapping(outputMap)

    av_speed = 4
    simulation = Simulation(r2, [], ammount, av_speed)
    result = simulation.run()
#self-made road
else:
    r1 = RoadSection(4, 20, name='R1')
    r2 = RoadSection(2, 40, name='R2')
    r3 = RoadSection(2, 100, name='R3')
    r4 = RoadSection(2, 40, name='R4')
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
    # r7.set_output_mapping({
    #     0: (r7, 2),
    #     1: (r7, 2),
    # })

    av_speed = 4
    simulation = Simulation(r1, [r2, r3, r4, r5, r6, r7, r8], ammount, av_speed)
    result = simulation.run()