import environment
import numpy as np

# NOTE FOR MY BOYS (to be deleted):
# When the robot goes over any (environment[x][y] == 0) we should convert
# it to = 2 so it is easier for the fitness function to compute.
# The simulation for an individual should end as soon as there is a 
# colision or when the time limit is reached.

# @author: Paco Francés
def fitness(environment):
    covered_count = 0
    non_obstacles = 0

    for i in range(environment.dimx):
        for j in range(environment.dimy):
            if (environment[i][j] == 2):
                covered_count += 1
                non_obstacles += 1
            elif (environment[i][j] == 0):
                non_obstacles += 1

    return covered_count / non_obstacles


# NOTE: WEIGHTS FOR Δt ARE NOT IMPLEMENTED YET!!!
#       CURRENTLY WORKS FOR A NN WITH 12 INPUTS AND 2 OUTPUTS (NO HIDDEN LAYER)
#       This will be changed as soon as the NN is ready.

# @author: Paco Francés
def generate_genome():
    w1 = np.random.random_sample((12,2))
    return w1