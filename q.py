X = None
y = None

def index(lst):
    return lst[0]

def clas(lst):
    return int(lst[1])

def wt(lst):
    return float(lst[2])

def cst(lst):
    return float(lst[3])

def val(lst):
    return float(lst[4])

def eff(lst):
    return float(lst[5])

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
        self.classes = {}
        self.con = {}

    def P(self):
        return self.v[0]
    
    def M(self):
        return self.v[1]
    
    def N(self):
        return self.v[2]
    
    def C(self):
        return self.v[3]

    def classes(self):
        return self.classes

    
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
            if (cst(x) < val(x)):
                lst = [0, 0, 0, 0, []]
                if clas(x) in self.classes.keys():
                    lst = self.classes[clas(x)]
                self.classes[clas(x)] = lst
                lst[0] += clas(x)
                lst[1] += val(x) - cst(x)
                lst[2] += 1
                lst[3] += wt(x)
                lst[4].append(x)
                self.classes[clas(x)][1] = self.classes[clas(x)][1] / self.classes[clas(x)][2]
            # self.classes[clas(x)][4] = sorted(self.classes[clas(x)][4], key = lambda x : -(val(x) - cst(x)) / wt(x))
        # print(self.classes[4][4])
                
    def readIncomp(self, f):
        for i in range(self.C()):
            line = f.readline().split(',')
            for i in line:
                i = int(i)
                if i not in self.con.keys():
                    self.con[i] = set()
                for j in line:
                    j = int(j)
                    if i != j:
                        self.con[i].add(j)
            # self.sets += [list(map(int, f.readline().split(',')))]
        # print(self.sets)

    def hasConflict(self, lst, y):
        for i in lst:
            if i in self.con.keys():
                if y in self.con[i]:
                    return True
        return False

    def solve(self):
        # sort classes in order of best efficiency
        w = 0
        lst = []
        for x in self.classes.keys():
            lst.append((x, self.classes[x][1]))
        lst = sorted(lst, key = lambda x: -x[1])
        # print(lst)


        i = 0
        max_items = []
        max_profit = 0


        p = len(lst)
        if len(self.classes) > 50:
            p = 50
        p = len(lst)
        for i in range(p):
            comp = set()
            comp.add(lst[i][0])
            q = int(min(len(lst), p))
            q = len(lst)
            for j in range(q):
                if j != i:
                    if not self.hasConflict(comp, lst[j][0]):
                        comp.add(lst[j][0])
            use = []
            # print(comp)

            # use = just the most efficient items with constraints checked for
            for q in comp:
                use.extend(self.classes[q][4])
            use = sorted(use, key = lambda x : -(val(x) - cst(x)) / (wt(x) + 0.1))


            items = []
            w = 0
            profit = 0
            p = 0

            # or just use the knapsack solution here, no need to work about constraints cuz
            # theyre already checked
            for i in use:
                weight = float(i[2])
                price = float(i[3])
                if weight + w <= self.P() and price + p <= self.M():
                    w += w
                    p += price
                    profit += float(i[4]) - price
                    items.append(i[0])
            # print(items)
            if profit > max_profit:
                max_items = items
                max_profit = profit

        print("max profit: " + str(max_profit))
        print("max items:")
        print(max_items)

        f = open('output/' + self.filename[4:-2] + "out", "w")

        for x in max_items:
            f.write(x + "\n")





# prob = Problem('data/problem1.in')
# prob.readFile()
# prob.solve()

x = 'data/problem'

for i in range(1, 22):
    prob = Problem(x + str(i) + '.in')
    prob.readFile()
    prob.solve()


# print('weight: {} / {} \nprice: {} / {} \nresale: {} \nprofit: {} \nitems used: {} / {}'.format( \
#             w, prob.P(), p, prob.M(), r, r - p, len(u), prob.N()))