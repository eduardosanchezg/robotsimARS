

class Robot:
    radius = 0
    posX = 0
    posY = 0
    velocity = [] #len 2 vector
    orentation = [] #len 4 vector
    environment = None

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.posX = posX
        self.posY = posY
        self.orentation = orientation
        self.radius = radius
        self.velocity = [0,0]

    def accLeft(self):
        pass

    def accRight(self):
        pass

    def stop(self):
        pass

    #todo: sensors stuff