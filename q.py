import numpy as np
import time
from problem import *

prob = Problem('data/problem1.in')
prob.readFile()
prob.removePricey()
w, p, r, u = prob.solve()

print('weight: {} / {} \nprice: {} / {} \nresale: {} \nprofit: {} \nitems used: {} / {}'.format( \
            w, prob.P(), p, prob.M(), r, r - p, len(u), prob.N()))
