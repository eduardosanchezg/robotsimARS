import random
import numpy as np
import environment, robot

population_size = 50
generations = 50
mutation_prob = 0.1
mutation_max_change = 0.1

# NOTE FOR MY BOYS (to be deleted):
# When the robot goes over any (environment[x][y] == 0) we should convert
# it to = 2 so it is easier for the fitness function to compute.
# The simulation for an individual should end as soon as there is a 
# colision or when the time limit is reached.

# @author: Paco Francés
def fitness(robot):
    covered_count = 0
    non_obstacles = 0
    for i in range(robot.environment.dimx):
        for j in range(robot.environment.dimy):
            if (robot.environment[i][j] == 2):
                covered_count += 1
                non_obstacles += 1
            elif (robot.environment[i][j] == 0):
                non_obstacles += 1
    return covered_count / non_obstacles


# NOTE: WEIGHTS FOR Δt ARE NOT IMPLEMENTED YET!!!
#       CURRENTLY WORKS FOR A NN WITH 12 INPUTS AND 2 OUTPUTS (NO HIDDEN LAYER)
#       This will be changed as soon as the NN is ready.
#       12 * 2 = 24 (Could be changed to read size of NN)       
#       In array form due to simplicity during crossover

# @author: Paco Francés
def generate_genome():
    genome = np.random.random_sample((24,))
    return genome

# List will be double the size to maintain the same population size
# This will most likely be changed to be more optimal
# @author: Paco Francés
def crossover(genome_list):
    offspring_list = []
    for i in range(len(genome_list)):
        offspring = crossover_pair(genome_list[i], genome_list[i+1])
        offspring_list.extend(offspring)
        if (len(offspring_list) >= population_size): break
        offspring = crossover_pair(genome_list[i], genome_list[i+2])
        offspring_list.extend(offspring)
        if (len(offspring_list) >= population_size): break
    return offspring_list

# Single-point crossover
# @author: Paco Francés
def crossover_pair(parent1, parent2):
    point = random.randint(1, parent1.size)
    child1 = np.zeros(parent1.size)
    child2 = np.zeros(parent1.size)
    for i in range(point):
        child1[i] = parent1[i]
        child2[i] = parent2[i]
    for i in range(point, parent1.size):
        child1[i] = parent2[i]
        child2[i] = parent1[i]
    return (child1, child2)

# @author: Paco Francés
def mutate(genome_list):
    for i in range(len(robot_list)):
        genome_list[i] = mutate_single(genome_list[i])
    return genome_list

# @author: Paco Francés
def mutate_single(genome):
    for i in range(genome.size):
        if (random.random() <= mutation_prob):
            genome[i] += random.uniform(-mutation_max_change, mutation_max_change)
    return genome

# Select top 50% of individuals for crossover (truncation selection)
# @author: Paco Francés
def select(robot_list):
    robot_list.sort(key=attrgetter('fitness'), reverse=True)
    return robot_list[:population_size/2]