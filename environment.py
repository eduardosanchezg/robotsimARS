

class Environment:
    grid = [] #binary 2d array

    def __init__(self, dimx, dimy):

        new = []
        for i in range(0, dimx):
            for j in range(0, dimy):
                new.append(0)
            self.grid.append(new)
            new = []

        for i in range(0, dimx):
            for j in range(0,dimy):
                if i == 0 or j == 0 or i == dimx-1 or j == dimy-1:
                    self.grid[i][j] = 1
