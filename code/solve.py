import numpy as np
import time
import pickle
from cvxopt import *
from lp_solver import *

datapath = '../data/'

@timeit
def solve():
    for i in range(2, 22):
        solveOne(i)

@timeit
def solveOne(i):
    prob = Problem(datapath + 'problem' + str(i) + '.in')
    prob.readFile()
    pickleDump(prob, i)
    prob.solve()

# i = 1
# prob = Problem(datapath + 'problem' + str(i) + '.in')
# prob.readFile()
# pickleDump(prob, i)
# prob.solve()

if __name__ == "__main__":
    solve()
