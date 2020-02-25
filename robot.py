import numpy as np
import math

class Robot:
    radius = 0
    max_sensor_range = radius + 200
    velocity = np.array([]) #len 2 vector
    environment = None
    pos = np.array([]) # vector saving position and orientation
    sensors = None

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.pos = np.array([posX, posY, orientation])
        self.radius = radius
        self.velocity = np.array([0, 0])
        self.sensors = np.zeros((12, 3)) # Sensor format: [range, x, y]
        self.refresh_sensors()

    def accLeft(self, dl):
        self.velocity[0] += dl

    def accRight(self, dr):
        self.velocity[1] += dr

    def stop(self):
        self.velocity = np.array([0,0])

    # @author: Tobias Bauer
    # Calculate movement of the robot in dt timesteps
    def time_step(self, dt):
        #print(self.pos)
        #print(self.velocity)
        if self.velocity[0] == self.velocity[1]:
            self.pos += (self.velocity[0] + self.velocity[1]) * np.array([math.cos(self.pos[2]), math.sin(self.pos[2]), 0])
            self.refresh_sensors()
            return
        R = (self.radius) * (np.sum(self.velocity)) / (np.diff(self.velocity))
        w = np.diff(self.velocity)/(2 * self.radius)
        transform = np.array([[math.cos(w*dt), -math.sin(w*dt), 0], 
                              [math.sin(w*dt), math.cos(w*dt), 0], 
                              [0,0,1]])
        icc = np.array([self.pos[0] - R*math.sin(self.pos[2]), self.pos[1] + R*math.cos(self.pos[2]), 0])
        #print(icc)
        self.pos = np.dot(transform, (self.pos-icc))
        self.pos += icc + np.array([0,0,w*dt])
        self.refresh_sensors()
    
    # @author: Paco Francés
    def refresh_sensors(self):
        for i in range(12):
            x = self.max_sensor_range * np.cos(self.pos[2] + (math.pi/6.) * i) + self.pos[0]
            y = self.max_sensor_range * np.sin(self.pos[2] + (math.pi/6.) * i) + self.pos[1]
            sensor_data = self.plotLine(self.pos[0], self.pos[1], x, y)
            if sensor_data is None:
                self.sensors[i][0] = self.max_sensor_range - self.radius # range
                self.sensors[i][1] = x # x
                self.sensors[i][2] = y # y
            else:
                self.sensors[i][0] = sensor_data[0] - self.radius # range
                self.sensors[i][1] = sensor_data[1] # x
                self.sensors[i][2] = sensor_data[2] # y


    # CODE BASED ON BRESENHAM'S LINE ALGORITHM TO PLOT SENSOR LINE:
    # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#Algorithm
    def plotLine(self, x0, y0, x1, y1):
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                return self.plotLineLow(x1, y1, x0, y0)
            else:
                return self.plotLineLow(x0, y0, x1, y1)
        else:
            if y0 > y1:
                return self.plotLineHigh(x1, y1, x0, y0)
            else:
                return self.plotLineHigh(x0, y0, x1, y1)

    def plotLineLow(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy 
        D = 2*dy - dx
        y = y0
        for x in range (int(x0), int(x1)):
            if x < 0 or x > len(self.environment.grid) or y > 0 or y < -len(self.environment.grid):
                pass
            elif self.environment.grid[int(x)][int(y)] == 1:
                return (math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2), x, y)
            if D > 0:
                   y = y + yi
                   D = D - 2*dx
            D = D + 2*dy
        return None#(self.max_sensor_range, x1, y1)

    def plotLineHigh(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = 2*dx - dy
        x = x0
        for y in range (int(y0), int(y1)):
            if x < 0 or x > len(self.environment.grid) or y > 0 or y < -len(self.environment.grid):
                pass
            elif self.environment.grid[int(x)][int(y)] == 1:
                    return (math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2), x, y)
            if D > 0:
                   x = x + xi
                   D = D - 2*dy
            D = D + 2*dx
        return None#(self.max_sensor_range, x1, y1)