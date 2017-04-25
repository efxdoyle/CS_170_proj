import numpy as np
import time
 
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
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
        self.sets = [] # lists of incompatible classes
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

    def readVar(self, f):
        for i in range(4):
            self.v[i] = float(f.readline())
        self.v[2], self.v[3] = int(self.v[2]), int(self.v[3])

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

    def readIncomp(self, f):
        for i in range(self.C()):
            self.sets += [list(map(int, f.readline().split(',')))]

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
        weight, price, resale = 0, 0, 0
        used = []
        for i in self.ordering:
            if weight + wt(self.X[i]) <= self.P() and price + cst(self.X[i]) <= self.M():
                weight += wt(self.X[i])
                price += cst(self.X[i])
                resale += val(self.X[i])
                used += [i]
        return weight, price, resale, used
