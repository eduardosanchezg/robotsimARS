import numpy as np

class Robot:
    radius = 0
    velocity = np.array([]) #len 2 vector
    environment = None
    pos = np.array([]) # vector saving position and orientation

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.pos = np.array([posX, posY, orientation])
        self.radius = radius
        self.velocity = np.array([16, 8])

    def accLeft(self, dl):
        pass

    def accRight(self, dr):
        pass

    def stop(self):
        pass

    def time_step(self, dt):
        if self.velocity[0] == self.velocity[1]:
            return
        R = (self.radius) * (np.sum(self.velocity)) / (np.diff(self.velocity))
        w = np.diff(self.velocity)/(2 * self.radius)
        transform = np.array([[np.cos(w*dt), -np.sin(w*dt), 0], [np.sin(w*dt), np.cos(w*dt), 0], [0,0,1]])
        icc = np.array([self.pos[0] - R*np.sin(self.pos[2]), self.pos[1] + R*np.cos(self.pos[2]), 0])
        self.pos = np.dot(transform, (self.pos-icc))
        self.pos += icc
        self.pos += np.array([0,0,w*dt])
    #todo: sensors stuff