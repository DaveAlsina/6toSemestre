import numpy as np 
from matplotlib import pyplot as plt


def f(c: float, npoints: int) -> None:

    in_points = np.ones((1, npoints))*c 
    exponents = 1/np.arange(1, in_points.shape[0])

    vfun = np.vectorize()
    out  = vfun(in_points, exponents)

    plt.plot()




