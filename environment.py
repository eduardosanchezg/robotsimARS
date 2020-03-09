

class Environment:
    grid = [] #binary 2d array
    dimx = 0
    dimy = 0

    def __init__(self, dimx, dimy):
        self.dimx = dimx
        self.dimy = dimy
        self.lines = []
        self.grid = [[0 for y in range(dimy)] for x in range(dimx)]
        self.dimx = dimx
        self.dimy = dimy
        self.add_line(0,0,dimx-1,0)
        self.add_line(0,0,0,-dimy+1)
        self.add_line(dimx-1,0,dimx-1,-dimy+1)
        self.add_line(0,-dimy+1,dimx-1,-dimy+1)

    def reset(self):
        for x in range(self.dimx):
            for y in range(self.dimy):
                self.grid[x][y] = 0
        for line in self.lines:
            x0 = line[0]
            y0 = line[1]
            x1 = line[2]
            y1 = line[3]
            self.plot_line(x0, -y0, x1, -y1)


    # @author: Tobias Bauer
    def add_line(self, x0, y0, x1, y1):
        self.lines.append([x0,y0,x1,y1])
        self.plot_line(x0, -y0, x1, -y1)
        
    def plot_line(self, x0, y0, x1, y1):
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
            if x < 0 or x > len(self.grid) or y < 0 or y > len(self.grid):
                pass
            else:
                self.grid[x][y] = 1
            if D > 0:
                   y = y + yi
                   D = D - 2*dx
            D = D + 2*dy

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
            if x < 0 or x > len(self.grid) or y < 0 or y > len(self.grid):
                pass
            else:
                self.grid[x][y] = 1
            if D > 0:
                   x = x + xi
                   D = D - 2*dy
            D = D + 2*dx