Computational science project - traffic flow
Lukas Koedijk, Martijn van de Ree, Lennart Mettrop, Max Filtenborg
10783687, 11922419, 10432973, 11042729

With these files we can create roads, run simulations, save data from
simulations to csv files and use this data to perform statistical tets.
For our project we have implemented two roads. The first road is based
on a real road and the second road is a variation of the first road.
We wanted to compare these two roads with each other. If you only want
to look at the results run "process_statistics.py".

The file "car.py" can create a car object and has functions to return a
speed the car hopes to get and functions to change the cars speed and
position.

The file "RoadSection.py" can create a road section object and has function
to determine what happens when a car gets on this road section and what
happens when the car leaves this road section.

The file "CreateRoads.py" can create different roads using multiple road
sections from "RoadSection.py".

The file "simulation.py" can run a simmulation. In the simulation we first
look at all the cars on the road and calculate where the cars want to go to.
Then we update the grid to change the position of the cars. After this we
add cars from the previous road section. At last we generate new cars
on the grid if the road section is defined to be a start road. This file
also has some functions to keep track of some values we use in "statistics.py".

The file "animate_sim.py" creates a visual of the simulation for the first road.

The file "animate_sim_new_road.py" creates a visual of the simulation for
the second road.

The file "statistics.py" will run multiple simulations and save values from
these runs in csv files. These result files will be placed in the folder
results/type_0 or results/type_2, where type is 0 is the first road and
type is 2 is the second road. The csv files that are in these folders will
be overwritten we "statistics.py" is executed. To use this file u need
to run "python statistics.py type steps times". Here type is 0 for the
first road and 2 for the second road. Steps is the ammount of steps
1 simulation has. Times is the ammount of times a simulation of a hour
is run, thus if times is 1 every hour is run ones.

The file "process_statistics.py" reads data from the result map and uses
this to create csv files with averages. Using this data we create multiple
plots. The first plot shows the average speed compared to the density.
in one graph.
The second plot shows the average speed for the different road sections of
the second road. The third plot shows the difference in average speed
calculated by the second road minus the first road. Thus if the line is
above zero then the second road has a higher average speed. The forth plot
show the average speeds of the two roads in one graph. The last plot also shows
the average speed from our data in the previous plot.
