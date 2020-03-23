import random
import numpy as np
import environment, robot
from PIL import Image
import numpy as np

population_size = 20
generations = 50
mutation_prob = 0.1
mutation_max_change = 0.1

env_width = 1000
env_height = 1000




def import_grid(file):
    image = Image.open(file)
    data = [image.getpixel((x, y)) for x in range(image.width) for y in range(image.height)]
    grid = []
    n = 0
    for i in range(0,image.width):
        line = []
        for j in range(0,image.height):
            if data[n][0] == 255:
                line.append(0)
            else:
                line.append(1)
            n=n+1
        grid.append(line)
    return grid

class Genome:

    def __init__(self):
        self.weights = generate_genome(56)
        #grid = import_grid("untitled.bmp")
        self.environment = environment.Environment(env_width, env_height, "trapezoid")
        # self.environment.add_line(500, -500, 500, -700)
        # self.environment.add_line(500, -700, 700, -700)
        # self.environment.add_line(700, -700, 700, -500)
        # self.environment.add_line(700, -500, 500, -500)

        # self.environment.add_line(400, -200, 300, -350)
        # self.environment.add_line(300, -350, 500, -350)
        # self.environment.add_line(500, -350, 400, -200)
        self.robot = robot.Robot(self.environment, 250, -250, 0., 60)
        self.nn = NN(self)

    def reset(self):
        self.environment.reset()
        self.robot.reset()
    


# @author: Paco Francés
class NN:
    def __init__(self, genome):
        self.input = np.zeros(12)
        self.hidden = np.zeros(4)
        self.output = np.zeros(2)
        self.w1 = np.zeros((self.input.size, self.hidden.size))
        self.w2 = np.zeros((self.hidden.size, self.output.size))

        # Assign genome to weights
        iterator = 0
        for i in range (self.input.size):
            for j in range(self.hidden.size):
                self.w1[i][j] = genome.weights[iterator]
                iterator += 1

        for i in range(self.hidden.size):
            for j in range(self.output.size):
                self.w2[i][j] = genome.weights[iterator]
                iterator += 1


# NOTE FOR MY BOYS (to be deleted):
# When the robot goes over any (environment[x][y] == 0) we should convert
# it to = 2 so it is easier for the fitness function to compute.
# The simulation for an individual should end as soon as there is a 
# colision or when the time limit is reached.

# @author: Paco Francés
def fitness(genome):
    environment = genome.environment
    covered_count = 0
    non_obstacles = 0
    for i in range(environment.dimx):
        for j in range(environment.dimy):
            if (environment.grid[i][j] == 2):
                covered_count += 1
                non_obstacles += 1
            elif (environment.grid[i][j] == 0):
                non_obstacles += 1
    print("Fitness: ", covered_count , non_obstacles)
    return covered_count


# NOTE: WEIGHTS FOR Δt ARE NOT IMPLEMENTED YET!!!
#       CURRENTLY WORKS FOR A NN WITH 12 INPUTS AND 2 OUTPUTS (1 HIDDEN LAYER; 4 NODES)
#       This will be changed as soon as the NN is ready.
#       12 * 4 = 48 (Could be changed to read size of NN)
#       + 4 * 2 = 56       
#       In array form due to simplicity during crossover

# @author: Paco Francés
def generate_genome(size):
    genome = np.random.randn(size,1)
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
    weights1 = parent1.weights
    weights2 = parent2.weights
    point = random.randint(1, weights1.size)
    child1 = np.zeros(weights1.size)
    child2 = np.zeros(weights1.size)
    for i in range(point):
        child1[i] = weights1[i]
        child2[i] = weights2[i]
    for i in range(point, weights1.size):
        child1[i] = weights2[i]
        child2[i] = weights1[i]
    genome1 = Genome()
    genome1.weights = child1
    genome2 = Genome()
    genome2.weights = child2
    return (genome1, genome2)

# @author: Paco Francés
def mutate(genome_list):
    for i in range(len(genome_list)):
        genome_list[i] = mutate_single(genome_list[i])
    return genome_list

# @author: Paco Francés
def mutate_single(genome):
    weights = genome.weights
    for i in range(weights.size):
        if (random.random() <= mutation_prob):
            weights[i] += random.uniform(-mutation_max_change, mutation_max_change)
    return genome

# Select top 50% of individuals for crossover (truncation selection)
# @author: Paco Francés
def select(genome_list):
    genome_list.sort(key=fitness, reverse=True)
    return genome_list[:int(population_size/2)]

# This is the NN's feedforward
# @author: Tobias Bauer & Paco Francés
def time_step(genome):
    robot = genome.robot
    #weights = np.reshape(genome.weights, (2,12))
    #tmp = weights.dot(robot.sensors.T[0])
    #moves = np.tanh(tmp)
    genome.nn.hidden = np.tanh(np.dot(genome.nn.input, genome.nn.w1))
    genome.nn.output = np.tanh(np.dot(genome.nn.hidden, genome.nn.w2))
    genome.nn.input = genome.robot.sensors.T[0]
    genome.robot.accLeft(genome.nn.output[0])
    genome.robot.accRight(genome.nn.output[1])


A = np.array([])
B = np.array([])
C = np.array([])
R = np.array([])
Q = np.array([])
I = np.array([])
# FIRST VERSION - TO BE COMPLETED! (we need to assign values to matrices)
# @author: Paco Francés
def kalman_filter(pose, covariance, action, sensors):
    # Prediction
    new_pose = A * pose + B * action
    new_covariance = A * covariance * A.T + R
    # Correction
    K = new_covariance * C.T * (1 / (C * new_covariance * C.T + Q))
    new_pose = new_pose + K * (sensors - C * action)
    new_covariance = (I - K * C) * new_covariance
    return (new_pose, new_covariance)