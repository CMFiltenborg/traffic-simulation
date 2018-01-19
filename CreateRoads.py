from RoadSection import RoadSection
from simulation import Simulation


class CreateRoads:
    @staticmethod
    def original_road(steps=100):
        spawn_r2 = [
            {0:0.5, 1:0.2, 2:0.2, 3:0.2, 4:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
        ]

        r1 = RoadSection(2, 100, name='R1')
        r2 = RoadSection(5, 100, is_end_road=True, name='R2', spawn_probabilities=spawn_r2)

        outputMap = {
            0: 3,  # Lane 1 corresponds with lane 5.
            1: 4   # Lane 2 corresponds with lane 5.
        }

        r1.set_output_mapping(outputMap)
        simulation = Simulation(r2, [], steps, 1)

        return simulation

    @staticmethod
    def new_design_road(steps=100, calculate_average_speed=False):
        spawn_r1 = [
            {0:1, 1:0.2, 2:0.2, 3:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
        ]
        spawn_r4 = [
            {0:0.2, 1:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
        ]

        r1 = RoadSection(4, 20, name='R1', spawn_probabilities=spawn_r1, output_colors=['red', 'red', 'black', 'black'])
        r2 = RoadSection(2, 40, name='R2')
        r3 = RoadSection(2, 100, name='R3')
        r4 = RoadSection(2, 40, name='R4', spawn_probabilities=spawn_r4, output_colors=['black', 'red'])
        r5 = RoadSection(1, 20, name='R5')
        r6 = RoadSection(1, 120, name='R6')
        r7 = RoadSection(3, 80, is_end_road=True, name='R7', right_lane=2)
        r8 = RoadSection(3, 40, is_end_road=True, name='R8', right_lane=2)

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
        simulation = Simulation(r1, [r2, r3, r7, r4, r5, r6, r8], steps, calculate_average_speed)

        return simulation

    def acces_road(steps=100, calculate_average_speed=False):
        spawn_r1 = [
            {0:1,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
        ]

        spawn_r2 = [
            {0:1,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),}
        ]

        r1 = RoadSection(1, 10, is_end_road=False, name='R1', spawn_probabilities=spawn_r1)
        r2 = RoadSection(1, 10, is_end_road=False, name='R2', spawn_probabilities=spawn_r2)
        r3 = RoadSection(2, 10, is_end_road=True, name='R3', right_lane=1)

        r1.set_output_mapping({
            0: (r3, 0),
        })
        r2.set_output_mapping({
            0: (r3, 1),
        })

        simulation = Simulation(r1, [r2, r3], steps, 0)

        return simulation