import numpy as np
import time
import pickle
from cvxopt import *
from lp_solver import *

datapath = '../data/'

# for i in range(1, 22):
#     prob = Problem(datapath + 'problem' + str(i) + '.in')
#     prob.readFile()
#     pickleDump(prob, i)
#     prob.solve()

i = 1
prob = Problem(datapath + 'problem' + str(i) + '.in')
prob.readFile()
pickleDump(prob, i)
prob.solve()
