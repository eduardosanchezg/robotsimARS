import pygame
import pygame.locals
import environment, robot


environment = environment.Environment()
robot = robot.Robot(environment,250,250,0,50)

pygame.init()
pygame.display.set_caption("ARS Robot Simulation")
screen = pygame.display.set_mode((500,500))
screen.fill((255, 255, 255))

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #next_simulation_step
    robot.time_step(1)
    pygame.draw.circle(screen,(100,100,100), (robot.pos[0],robot.pos[1]),robot.radius)
    pygame.display.update()
