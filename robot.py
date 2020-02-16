import numpy as np
import math

class Robot:
    radius = 0
    max_sensor_range = radius + 200
    velocity = np.array([]) #len 2 vector
    environment = None
    pos = np.array([]) # vector saving position and orientation

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.pos = np.array([posX, posY, orientation])
        self.radius = radius
        self.velocity = np.array([0, 0])
        # Sensor format: [range, x, y]
        self.sensors = np.zeros((12, 3))
        self.refresh_sensors()

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
        self.refresh_sensors()
    
    def refresh_sensors(self):
        for i in range(12):
            x = max_sensor_range * np.cos(self.pos[2] + i*30) + self.pos[0]
            y = max_sensor_range * np.sin(self.pos[2] + i*30) + self.pos[1]
            sensor_data = plotLine(self.pos[0], self.pos[1], x, y)
            self.sensors[i][0] = sensor_data[0] - self.radius # range
            self.sensors[i][1] = sensor_data[1] # x
            self.sensors[i][2] = sensor_data[2] # y


    # CODE BASED ON BRESENHAM'S LINE ALGORITHM TO PLOT SENSOR LINE:
    # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#Algorithm
    def plotLine(x0,y0, x1,y1):
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                return plotLineLow(x1, y1, x0, y0)
            else:
                return plotLineLow(x0, y0, x1, y1)
        else:
            if y0 > y1:
                return plotLineHigh(x1, y1, x0, y0)
            else:
                return plotLineHigh(x0, y0, x1, y1)

    def plotLineLow(x0,y0, x1,y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy 
        D = 2*dy - dx
        y = y0
        for x in range (x0, x1):
            if environment[x,y] == 1:
                return (math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2), x, y)
            if D > 0:
                   y = y + yi
                   D = D - 2*dx
            D = D + 2*dy
        return (max_sensor_range, x1, y1)

    def plotLineHigh(x0,y0, x1,y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = 2*dx - dy
        x = x0
        for y in range (y0, y1):
            if environment[x,y] == 1:
                    return (math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2), x, y)
            if D > 0:
                   x = x + xi
                   D = D - 2*dy
            D = D + 2*dx
        return (max_sensor_range, x1, y1)