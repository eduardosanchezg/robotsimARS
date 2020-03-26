import math

import pygame
import pygame.locals
import environment, robot, ea, ai

env_width = 1000
env_height = 1000

environment = environment.Environment(env_width, env_height, "trapezoid")
robot = robot.Robot(environment,250,-250,0.,25)
#genome = ea.do_ea()
#genome = ai.Genome()
#robot = genome.robot
#environment = genome.environment
robot.environment = environment
robot.init_belief_map()

pygame.init()
pygame.display.set_caption("ARS Robot Simulation")
screen = pygame.display.set_mode((env_width, env_height))
screen.fill((255, 255, 255))

run = True


while run:

    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.accLeft(1)
            if event.key == pygame.K_s:
                robot.accLeft(-1)
            if event.key == pygame.K_o:
                robot.accRight(1)
            if event.key == pygame.K_l:
                robot.accRight(-1)
            if event.key == pygame.K_x:
                robot.stop()
            if event.key == pygame.K_t:
                robot.accLeft(1)
                robot.accRight(1)
            if event.key == pygame.K_g:
                robot.accLeft(-1)
                robot.accRight(-1)

    #next_simulation_step
    #ai.time_step(genome)
    #robot.accLeft(moves[0])
    #robot.accLeft(moves[1])
    robot.time_step(1)
    screen.fill((255,255,255))
    # for i in range(0, env_height):
    #     for j in range(0, env_height):
    #         if environment.grid[i][j] == 1:
    #             pygame.draw.rect(screen,(0,0,0),[i,j,1,1],0)
    for line in environment.lines:
        pygame.draw.line(screen, (0,0,0), (line[0], -line[1]), (line[2], -line[3]))
    pygame.draw.circle(screen,(100,100,100), (int(robot.pos[0]),-int(robot.pos[1])),robot.radius)
    x = robot.pos[0] + math.cos(robot.pos[2]) * robot.radius
    y = -robot.pos[1] - math.sin(robot.pos[2]) * robot.radius
    pygame.draw.line(screen,(0,255,255),(robot.pos[0],-robot.pos[1]),(x,y),5)


    font = pygame.font.SysFont('Sans', 10)
    sensor_labels = []
    for i in range(0,12):
        sensor_labels.append(font.render(str(int(robot.sensors[i][0])), True, (0, 150, 0)))
        x = robot.pos[0] + math.cos(robot.pos[2]+(math.pi/6.) * i) * (robot.radius + (math.pi/6.))
        y = robot.pos[1] + math.sin(robot.pos[2]+(math.pi/6.) * i) * (robot.radius + (math.pi/6.))
        screen.blit(sensor_labels[i], (x, -y))

        x_ = robot.pos[0] + math.cos(robot.pos[2] + (math.pi/6.) * i) * (robot.radius)
        y_ = robot.pos[1] + math.sin(robot.pos[2] + (math.pi/6.) * i) * (robot.radius)
        pygame.draw.line(screen, (255, 0, 0), (x_, -y_), (robot.sensors[i][1],-robot.sensors[i][2]), 1)


    pygame.display.update()
