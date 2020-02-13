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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                robot.accLeft(1)
            if event.key == pygame.K_s:
                robot.accLeft(-1)
            if event.key == pygame.K_o:
                robot.accRight(1)
            if event.key == pygame.K_l:
                robot.accRight(1)
            if event.key == pygame.K_x:
                robot.stop()
            if event.key == pygame.K_t:
                robot.accLeft(1)
                robot.accRight(1)
            if event.key == pygame.K_g:
                robot.accLeft(-1)
                robot.accRight(-1)

    #next_simulation_step
    robot.time_step(1)
    pygame.draw.circle(screen,(100,100,100), (robot.pos[0],robot.pos[1]),robot.radius)
    pygame.display.update()
