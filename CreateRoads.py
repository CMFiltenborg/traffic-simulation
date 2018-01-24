from RoadSection import RoadSection
from simulation import Simulation


class CreateRoads:
    @staticmethod
    def original_road(steps=100):
        spawn_r2 = [
            {0:0.5, 1:0.2, 2:0.2, 3:0.2, 4:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),},
            {0:(0,2/9.0), 1:(2/9.0, 4/9), 2:(4/9.0, 6/9.0), 3:(6/9.0, 7.5/9.0), 4:(7.5/9.0,1),}
        ]

        r = RoadSection(5, 100, is_end_road=True, name='R1', spawn_probabilities=spawn_r2, output_colors=['red', 'red', 'red', 'black', 'black'])

        simulation = Simulation(r, [], steps, 1)

        return simulation

    @staticmethod
    def new_road(steps=100, calculate_average_speed=False):
        spawn_r1 = [
            {0:0.5, 1:0.2, 2:0.2, 3:0.2,},
            {5:(0,0.2), 4:(0.2, 0.4), 3:(0.4, 1),},
            {0:(0,2/9.0), 1:(2/9.0, 4/9), 2:(4/9.0, 6/9.0), 3:(6/9.0, 7.5/9.0),}
        ]
        
        spawn_r2 = [
            {0:0.2,},
            {5:(0,0.2), 4:(0.2, 0.4), 3:(0.4, 1),},
            {4:(7.5/9.0,1),}
        ]
        
        r1 = RoadSection(4, 10, name='R1', spawn_probabilities=spawn_r1,
                         output_colors =['red', 'red', 'red', 'black', 'black'])
        r2 = RoadSection(1, 10, name='R2', spawn_probabilities=spawn_r2,
                         output_colors=['red', 'red', 'red', 'black', 'black'])
        r5 = RoadSection(2, 90, name='R5', is_end_road=True)
        r6 = RoadSection(2, 30, name='R6')
        r7 = RoadSection(1, 60, name='R7', is_end_road=True)
        r8 = RoadSection(1, 30, name='R8')
        r9 = RoadSection(2, 60, name='R9')
        r10 = RoadSection(3, 30, name='R10', is_end_road=True, right_lane=2)
    
        r1.set_output_mapping({
            0: (r5, 0),
            1: (r5, 1),
            2: (r9, 0),
            3: (r9, 1),
        })
    
        r2.set_output_mapping({
            0: (r6, 1),
        })
    
        r6.set_output_mapping({
            0: (r7, 0),
            1: (r8, 0),
        })
    
        r8.set_output_mapping({
            0: (r10, 2),
        })
    
        r9.set_output_mapping({
            0: (r10, 0),
            1: (r10, 1),
        })
        
        r5.set_input_mapping({
            0: (r1, 0),
            1: (r1, 1),
        })
        
        r6.set_input_mapping({
            1: (r2, 0),
        })
        
        r7.set_input_mapping({
            0: (r6, 0),
        })
        
        r8.set_input_mapping({
            0: (r6, 1),
        })
        
        r9.set_input_mapping({
            0: (r1, 2),
            1: (r1, 3),
        })
        
        r10.set_input_mapping({
            0: (r9, 0),
            1: (r9, 1),
            2: (r8, 0),
        })
        
        simulation = Simulation(r1, [r2, r5, r6, r7, r8, r9, r10], steps, calculate_average_speed)
        
        return simulation
        
    @staticmethod
    def new_design_road(steps=100, calculate_average_speed=False):
        spawn_r1 = [
            {0:1, 1:0.2, 2:0.2, 3:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),},
            {0:(0,2/6.0), 1:(2/6.0,4/6.0), 2:(4/6.0,5/6.0), 3:(5/6.0,1)}
        ]
        spawn_r4 = [
            {0:0.2, 1:0.2,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),},
            {0:(0,1/3.0), 1:(1/3.0,1)}
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
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),},
            {0:(1,1)}
        ]

        spawn_r2 = [
            {0:1,},
            {5:(0,0.2),4:(0.2,0.4),3:(0.4,1),},
            {0:(1,1)}
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