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
        self.velocity = np.array([0, 0])

    def accLeft(self, dl):
        self.velocity[0] += dl

    def accRight(self, dr):
        self.velocity[1] += dr

    def stop(self):
        self.velocity = np.array([0,0])

    def time_step(self, dt):
        print(self.pos)
        print(self.velocity)
        if self.velocity[0] == self.velocity[1]:
            self.pos += (self.velocity[0] + self.velocity[1]) * np.array([np.sin(self.pos[2]), np.cos(self.pos[2]), 0])
            return
        R = (self.radius) * (np.sum(self.velocity)) / (np.diff(self.velocity))
        w = np.diff(self.velocity)/(2 * self.radius)
        transform = np.array([[np.cos(w*dt), -np.sin(w*dt), 0], [np.sin(w*dt), np.cos(w*dt), 0], [0,0,1]])
        icc = np.array([self.pos[0] - R*np.sin(self.pos[2]), self.pos[1] + R*np.cos(self.pos[2]), 0])
        self.pos = np.dot(transform, (self.pos-icc))
        self.pos += icc + np.array([0,0,w*dt])
    #todo: sensors stuff