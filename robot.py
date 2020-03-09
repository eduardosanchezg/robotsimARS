import numpy as np
import math

class Robot:
    radius = 0
    max_sensor_range = radius + 200
    velocity = np.array([]) #len 2 vector
    environment = None
    pos = np.array([]) # vector saving position and orientation
    sensors = None
    fitness = 0
    genome = []

    def __init__(self,environment, posX, posY, orientation, radius):
        self.environment = environment
        self.pos = np.array([posX, posY, orientation])
        self.radius = radius
        self.velocity = np.array([0., 0.])
        # Sensor format: [range, x, y]
        self.sensors = np.zeros((12, 3))
        self.refresh_sensors()

    def reset(self):
        self.velocity = np.array([0., 0.])
        self.sensors = np.zeros((12, 3))
        self.pos = np.array([250, -250, 0.])

    def accLeft(self, dl):
        self.velocity[0] += dl

    def accRight(self, dr):
        self.velocity[1] += dr

    def stop(self):
        self.velocity = np.array([0,0])

    # @author: Tobias Bauer
    # Calculate movement of the robot in dt timesteps
    def time_step(self, dt):
        self.environment.grid[int(self.pos[0])][int(self.pos[1])] = 2
        collision_points = self.check_for_collision()
        if self.velocity[0] == self.velocity[1]:
            v = (self.velocity[0]) * np.array([math.cos(self.pos[2]), math.sin(self.pos[2]), 0])
        else:
            R = (self.radius) * (np.sum(self.velocity)) / float(np.diff(self.velocity))
            w = float(np.diff(self.velocity))/(2 * self.radius)
            transform = np.array([[math.cos(w*dt), -math.sin(w*dt), 0], 
                                [math.sin(w*dt), math.cos(w*dt), 0], 
                                [0,0,1]])
            icc = np.array([self.pos[0] - R*math.sin(self.pos[2]), self.pos[1] + R*math.cos(self.pos[2]), 0])
            pos_new = np.dot(transform, (self.pos-icc))
            pos_new += icc + np.array([0,0,w*dt])
            v = pos_new - self.pos

        for collision_point in collision_points[1]:
            if np.dot(v, np.append(collision_point[0],0)) >= 0:
                v1 = np.append(collision_point[1],0)
                v = np.dot(v,v1) / np.dot(v1,v1) * v1
        if not collision_points[0] and self.check_for_collision_moving(v):
            return
        self.pos += v
        self.refresh_sensors()

    def check_for_collision_moving(self, M):
        #print("check", self.pos, M)
        Q = self.pos[:2]
        r = float(self.radius)
        M = M[:2]
        collisions = []
        for line in self.environment.lines:
            P1 = np.array(line[:2])
            V = np.array(line[2:]) - P1
            # generate orthogonal vector O
            O = np.random.randn(2) 
            O -= O.dot(V)/(np.linalg.norm(V))**2 * V
            O /= np.linalg.norm(O)
            if np.dot(O, M) < 1e-3: # line is parallel to movement
                continue
            b1 = Q - P1 - r * O
            b2 = Q - P1 + r * O
            a = np.concatenate(([-M], [V])).T
            x1 = np.linalg.solve(a, b1)
            x2 = np.linalg.solve(a, b2)
            if (x1 >= 0).all() and (x1 <= 1).all():
                #print("Collision")
                #print(x1)
                return True
            if (x2 >= 0).all() and (x2 <= 1).all():
                #print("Collision")
                #print(x2)
                return True
        #print("no Collision")
        return False


    # @author: Tobias Bauer
    def check_for_collision(self):
        Q = self.pos[:2]
        r = float(self.radius)
        collisions = []
        for line in self.environment.lines:
            P1 = np.array(line[:2])
            V = np.array(line[2:]) - P1
            a = V.dot(V)
            b = 2 * V.dot(P1 - Q)
            c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2
            disc = b**2 - 4 * a * c
            if disc < 0:
                continue
            sqrt_disc = math.sqrt(disc)
            t1 = (-b + sqrt_disc) / (2 * a)
            t2 = (-b - sqrt_disc) / (2 * a)
            if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
                continue
            t = max(0, min(1, - b / (2 * a)))
            collisions.append(((P1 + t * V)-Q, V))
        return len(collisions) > 0, collisions

    
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
            if x < 0 or x >= self.environment.dimx or y > 0 or y <= -self.environment.dimy:
                pass
            elif self.environment.grid[int(x)][-int(y)] == 1:
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
            if x < 0 or x >= self.environment.dimx or y > 0 or y <= -self.environment.dimy:
                pass
            elif self.environment.grid[int(x)][-int(y)] == 1:
                    return (math.sqrt(((self.pos[0] - x)**2) + (self.pos[1] - y)**2), x, y)
            if D > 0:
                   x = x + xi
                   D = D - 2*dy
            D = D + 2*dx
        return None#(self.max_sensor_range, x1, y1)