import numpy as np
import time
import pickle
from cvxopt import *

picklepath = '../pickled/'
writepath = '../output/'

def strSplit(s, lst):
    for r in lst:
        s = s.replace(r, ' ')
    return s.split()

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r %2.2f sec' % \
              (method.__name__, te-ts))
        return result

    return timed

def index(lst):
    return lst[0]

def clas(lst):
    return lst[1]

def wt(lst):
    return lst[2]

def cst(lst):
    return lst[3]

def val(lst):
    return lst[4]

def eff(lst):
    return lst[5]

def profit(cost, resale):
    return resale - cost

class Problem(object):
    def __init__(self, f):
        self.filename = f
        self.read = False
        self.v = [0, 0, 0, 0] # contains variables P, M, N, C
        self.names = [] # maps index to item name
        self.X = None # data matrix of [number, class, weight, cost, value]
        self.sets = None # matrix of sets of incompatible classes; last 2 rows are blanks
        self.ordering = () # indices of cut X in order of decreasing efficiency

    def P(self):
        return self.v[0]

    def M(self):
        return self.v[1]

    def N(self):
        return self.v[2]

    def C(self):
        return self.v[3]

    @timeit
    def readFile(self):
        if self.read:
            raise Exception('already read')
        with open(self.filename) as f:
            self.readVar(f)
            self.readItems(f)
            self.readIncomp(f)
        self.read = True

    @timeit
    def readVar(self, f):
        for i in range(4):
            self.v[i] = float(f.readline())
        self.v[2], self.v[3] = int(self.v[2]), int(self.v[3])

    @timeit
    def readItems(self, f):
        for i in range(self.N()):
            x = f.readline().split(';')
            self.names += [x[0]]
            x[0] = i
            x = [float(s) for s in x]
            if i == 0:
                self.X = np.array(x, dtype = 'float64')
            else:
                self.X = np.vstack((self.X, x))

    @timeit
    def readIncomp(self, f):
        temp = []
        for i in range(self.C()):
            temp += [set(int(x.strip()) for x in f.readline().split(","))]
        self.setSets(temp)

    @timeit
    def setSets(self, lst):
        self.sets = spmatrix(0, [0], [0], (3 * self.N() + 2, self.N()))
        for s in lst:
            incomp = [p for q in [[i for i in range(self.N()) if x == self.X[i, 1]] for x in s] for p in q]
            for i in incomp:
                self.sets[i, incomp] = 1

    def shouldRemove(self, row):
        if cst(row) >= val(row):
            return True
        if wt(row) > self.P():
            return True
        if cst(row) > self.M():
            return True
        return False

    @timeit
    def removePricey(self):
        temp = []
        efficiency = []
        for i, row in enumerate(self.X):
            if self.shouldRemove(row):
                temp += [i]
                pass
            efficiency += [(val(row) - cst(row)) / wt(row)]
        self.X = np.delete(self.X, temp, axis = 0)
        self.X = np.column_stack((self.X, np.array(efficiency, dtype = 'float64').reshape((-1, 1))))
        self.ordering = list(zip(*sorted(enumerate(efficiency), key=lambda x: x[1])[::-1]))[0]

    @timeit
    def solve(self):
        c = - matrix(self.X[:, 4]) # negatives of prices
        A = self.sets # set constraints, and 2 extra rows
        A[-2, :], A[-1, :] = self.X[:, 2], self.X[:, 3] # weight, cost constraints
        for i in range(self.N()):
            A[self.N() + i, i] = -1 # 0 constraints
            A[2 * self.N() + i, i] = 1 # 1 constraints
        b = matrix([1 for _ in range(len(self.X))] + [0 for _ in range(self.N())] + [1 for _ in range(self.N())] + [self.P(), self.M()]) # set constraints, weight, cost
#         print('c: \n{}'.format(c))
#         print('A: \n{}'.format(A))
#         print('b: \n{}'.format((b)))
        bound = [0, 1] # 0-1 bound x
        res = solvers.lp(c, A, b, solver = 'glpk')
        self.writeSol(res['x'])
        return res

    @timeit
    def writeSol(self, x):
        with open(writepath + strSplit(self.filename, ['/', '.'])[-2] + '.out', 'w') as f:
            for i, val in enumerate(x):
                if val > 0.5:
                    f.write(str(self.names[i]) + '\n')

@timeit
def pickleDump(p, num):
    pickle.dump(p.v, open(picklepath + "p" + str(num) + "v.p","wb"))
    pickle.dump(p.names, open(picklepath + "p" + str(num) + "names.p","wb"))
    pickle.dump(p.X, open(picklepath + "p" + str(num) + "X.p","wb"))
    pickle.dump(p.sets, open(picklepath + "p" + str(num) + "sets.p","wb"))
