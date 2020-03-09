import ai, environment, robot
import numpy as np

def do_ea():

    pop_count = 10

    time_steps = 600

    evo_steps = 20

    genome_list = []

    for _ in range(pop_count):

        genome = ai.Genome()
        genome_list.append(genome)

    for _ in range(evo_steps):
        print("Calc Evo", _)

        for i in range(pop_count):

            print("Calc robo", i)
            
            genome = genome_list[i]
            robot = genome.robot

            genome.reset()

            for t in range(time_steps):
                ai.time_step(genome)
                robot.time_step(1)
                if 0 in robot.sensors.T[0]: break

        genome_list = ai.select(genome_list)

        print(genome_list[0].weights)

        genome_list = ai.crossover(genome_list)
        ai.mutate(genome_list)



    
    return genome_list[0]