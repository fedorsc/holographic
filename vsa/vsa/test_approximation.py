from hrr import HRR
import matplotlib.pyplot as plt
import numpy as np
from approximation import Approximation
#%matplotlib inline

def fn_square(x):
    return x * x

def fn_hyp_parab(x, y):
    return x * y

def fn_2dparab(x, y):
    return x * x

def fn_plane(x, y):
    return x + y

HRR.visualize = False
HRR.verbose = False
Approximation.verbose_learn = False
Approximation.verbose_probe = False

#input_range = np.array([-3.5, 3.5])
#output_range = np.array([0.0, fn_square(input_range[0])])
input_range = np.array([(-1.0, 1.0), (-1.0, 1.0)])
output_range = np.array([-2.0, 2.0])

print("input_range: {} output_range: {}".format(input_range, output_range))

#HRR.incremental_weight = 0.5

#appr = Approximation(fn=fn_2dparab, size=3000)
#appr.learn(input_range=input_range, output_range=output_range, n_samples=200, stddev=0.02, use_incremental=False)
#appr.plot_result(input_range=input_range, output_range=output_range, n_samples=19)
appr = Approximation(fn=fn_plane, size=10000)
appr.learn(input_range=input_range, output_range=output_range, n_samples=(10, 10), stddev=0.01, use_incremental=False)

n_samples = (10, 10)

if True:
    input_tuples = []
    X = np.linspace(-1.0, 1.0, n_samples[0])
    Y = np.linspace(-1.0, 1.0, n_samples[1])
    for x in X:
        for y in Y:
            input_tuples.append((x, y))
    appr.verify(input_tuples=input_tuples, input_range=input_range, output_range=output_range, suppress_input=True)

appr.plot3d_result(input_range=input_range, output_range=output_range, n_samples=n_samples)
