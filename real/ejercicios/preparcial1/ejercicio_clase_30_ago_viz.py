import numpy as np 
from matplotlib import pyplot as plt

def e(c: float, exponent: float) -> float:
    return np.power(c, exponent)

def f(c: float, npoints: int) -> None:

    in_points = np.ones((npoints, ))*c 
    exponents = 1/np.arange(1, in_points.shape[0]+1)

    print(in_points.shape, exponents.shape)

    vfun = np.vectorize(pyfunc = e,  otypes=[float])
    out  = vfun(in_points, exponents)

    plt.plot(out)
    plt.show()

f(c = 20, npoints = 1000)

