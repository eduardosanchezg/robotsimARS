import pygame
import pygame.locals
import environment, robot


environment = environment.Environment()
robot = robot.Robot(environment,250,250,[1,0,0,0],50)

pygame.init()
pygame.display.set_caption("ARS Robot Simulation")
screen = pygame.display.set_mode((500,500))
screen.fill((0, 0, 0))

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #next_simulation_step
    pygame.draw.circle(screen,(100,100,100), (robot.posX,robot.posY),robot.radius)
    pygame.display.update()
