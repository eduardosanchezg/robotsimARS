import numpy as np


def rosenbrock(X, Y, a=0, b=1):
    return (a-X)**2 + b*(Y-X**2)**2

def rastrigen(X, Y):
    return 20 + (X**2 - 10*np.cos(2*np.pi *X)) + (Y**2 - 10*np.cos(2*np.pi *Y))