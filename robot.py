import numpy as np
import math

class Robot:
    radius = 0
    max_sensor_range = 200
    velocity = np.array([]) #len 2 vector
    environment = None
    pos = np.array([]) # vector saving position and orientation

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.pos = np.array([posX, posY, orientation])
        self.radius = radius
        self.velocity = np.array([0, 0])
        self.sensors = np.full(12, max_sensor_range)

    def accLeft(self, dl):
        self.velocity[0] += dl

    def accRight(self, dr):
        self.velocity[1] += dr

    def stop(self):
        self.velocity = np.array([0,0])

    def time_step(self, dt):
        if self.velocity[0] == self.velocity[1]:
            return
        R = (self.radius) * (np.sum(self.velocity)) / (np.diff(self.velocity))
        w = np.diff(self.velocity)/(2 * self.radius)
        transform = np.array([[np.cos(w*dt), -np.sin(w*dt), 0], [np.sin(w*dt), np.cos(w*dt), 0], [0,0,1]])
        icc = np.array([self.pos[0] - R*np.sin(self.pos[2]), self.pos[1] + R*np.cos(self.pos[2]), 0])
        self.pos = np.dot(transform, (self.pos-icc))
        self.pos += icc + np.array([0,0,w*dt])
        self.refresh_sensors()
    
    def refresh_sensors(self):
        self.scan0()
        self.scan1()
        self.scan2()
        self.scan3()
        self.scan4()
        self.scan5()
        self.scan6()
        self.scan7()
        self.scan8()
        self.scan9()
        self.scan10()
        self.scan11()

    def scan0(self):
        x = max_sensor_range * np.cos(self.pos[2] + 0) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 0) + self.pos[1]
        self.sensors[0] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan1(self):
        x = max_sensor_range * np.cos(self.pos[2] + 30) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 30) + self.pos[1]
        self.sensors[1] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan2(self):
        x = max_sensor_range * np.cos(self.pos[2] + 60) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 60) + self.pos[1]
        self.sensors[2] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan3(self):
        x = max_sensor_range * np.cos(self.pos[2] + 90) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 90) + self.pos[1]
        self.sensors[3] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan4(self):
        x = max_sensor_range * np.cos(self.pos[2] + 120) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 120) + self.pos[1]
        self.sensors[4] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan5(self):
        x = max_sensor_range * np.cos(self.pos[2] + 150) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 150) + self.pos[1]
        self.sensors[5] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan6(self):
        x = max_sensor_range * np.cos(self.pos[2] + 180) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 180) + self.pos[1]
        self.sensors[6] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan7(self):
        x = max_sensor_range * np.cos(self.pos[2] + 210) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 210) + self.pos[1]
        self.sensors[7] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan8(self):
        x = max_sensor_range * np.cos(self.pos[2] + 240) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 240) + self.pos[1]
        self.sensors[8] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan9(self):
        x = max_sensor_range * np.cos(self.pos[2] + 270) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 270) + self.pos[1]
        self.sensors[9] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan10(self):
        x = max_sensor_range * np.cos(self.pos[2] + 300) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 0) + self.pos[1]
        self.sensors[10] = plotLine(self.pos[0], self.pos[1], x, y)

    def scan11(self):
        x = max_sensor_range * np.cos(self.pos[2] + 330) + self.pos[0]
        y = max_sensor_range * np.sin(self.pos[2] + 330) + self.pos[1]
        self.sensors[11] = plotLine(self.pos[0], self.pos[1], x, y)


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
                return math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2)
            if D > 0:
                   y = y + yi
                   D = D - 2*dx
            D = D + 2*dy
        return max_sensor_range

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
                    return math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2)
            if D > 0:
                   x = x + xi
                   D = D - 2*dy
            D = D + 2*dx
        return max_sensor_range