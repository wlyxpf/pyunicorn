#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tutorial on how to handle recurrence plots and recurrence networks using
Python, based on the timeseries package.

Written as part of a PhD thesis in Physics by Jonathan F. Donges
(donges@pik-potsdam.de) at the Potsdam Institute of Climate Impact Research
(PIK) and Humboldt University Berlin,

Copyright 2008-2018.
"""

# array object and fast numerics
import numpy as np

# plotting facilities
import pylab

from pyunicorn.timeseries import RecurrencePlot, RecurrenceNetwork


#
#  Functions
#
def logistic_map(x0, r, T):
    """
    Returns a time series of length T using the logistic map
    x_(n+1) = r*x_n(1-x_n) at parameter r and using the initial condition x0.

    INPUT: x0 - Initial condition, 0 <= x0 <= 1
            r - Bifurcation parameter, 0 <= r <= 4
            T - length of the desired time series
    TODO: Cythonize
    """
    #  Initialize the time series array
    timeSeries = np.empty(T)

    timeSeries[0] = x0
    for i in range(1, len(timeSeries)):
        xn = timeSeries[i-1]
        timeSeries[i] = r * xn * (1 - xn)

    return timeSeries


def logistic_map_lyapunov_exponent(timeSeries, r):
    """
    Returns the Lyapunov exponent of the logistic map for different r.

    INPUT: timeSeries - The time series generated by a logistic map
                    r - the bifurcation parameter
    """
    lyap = np.log(r) + (np.log(np.abs(1 - 2 * timeSeries))).mean()

    return lyap

#
#  Settings
#

#  Parameters of logistic map
r = 3.679  # Bifurcation parameter
x0 = 0.7   # Initial value

#  Length of the time series
T = 150

#  Settings for the embedding
DIM = 1  # Embedding dimension
TAU = 0  # Embedding delay

#  Settings for the recurrence plot
EPS = 0.05  # Fixed threshold
RR = 0.05   # Fixed recurrence rate
# Distance metric in phase space ->
# Possible choices ("manhattan","euclidean","supremum")
METRIC = "supremum"

#
#  Main script
#
#  Create a time series using the logistic map
time_series = logistic_map(x0, r, T)

#  Print the time series
print(time_series)
#  Plot the time series
pylab.plot(time_series, "r")
#  You can include LaTex labels...
pylab.xlabel("$n$")
pylab.ylabel("$x_n$")

#  Generate a recurrence plot object with fixed recurrence threshold EPS
rp = RecurrencePlot(time_series, dim=DIM, tau=TAU, metric=METRIC,
                    normalize=False, threshold=EPS)

#  Show the recurrence plot
pylab.matshow(rp.recurrence_matrix())
pylab.xlabel("$n$")
pylab.ylabel("$n$")
pylab.show()

#  Calculate and print the recurrence rate
print("Recurrence rate:", rp.recurrence_rate())

#  Calculate some standard RQA measures
DET = rp.determinism(l_min=2)
LAM = rp.laminarity(v_min=2)

print("Determinism:", DET)
print("Laminarity:", LAM)

#  Generate a recurrence plot object with fixed recurrence rate RR
rp = RecurrencePlot(time_series, dim=DIM, tau=TAU, metric=METRIC,
                    normalize=False, recurrence_rate=RR)

#  Calculate and print the recurrence rate again to check if it worked...
RR = rp.recurrence_rate()
print("Recurrence rate:", RR)

#  Calculate some standard RQA measures
DET = rp.determinism(l_min=2)
LAM = rp.laminarity(v_min=2)

print("Determinism:", DET)
print("Laminarity:", LAM)

#  Generate a recurrence network at fixed recurrence rate
rn = RecurrenceNetwork(time_series, dim=DIM, tau=TAU, metric=METRIC,
                       normalize=False, recurrence_rate=RR)

#  Calculate average path length, transitivity and assortativity
L = rn.average_path_length()
T = rn.transitivity()
C = rn.global_clustering()
R = rn.assortativity()

print("Average path length:", L)
print("Transitivity:", T)
print("Global clustering:", C)
print("Assortativity:", R)
