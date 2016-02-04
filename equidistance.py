from random import choice, shuffle, uniform, random
from math import cos, sin, pi
from collections import namedtuple
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, n1, n2, p):
        self.x = x
        self.n1 = n1
        self.n2 = n2
        self.p = p
        self.np = p

def goodlist(xs):
    for i in xrange(len(xs)/2):
        if i == xs[2*i] or i == xs[2*i+1] or xs[2*i] == xs[2*i+1]:
            return False
    return True

def makebodies(n):
    b = []
    m = range(n)*2
    while not goodlist(m):
        shuffle(m)
    for x in xrange(0,n):
        b.append(Point(x, m[2*x], m[2*x+1], 0))
    return b

def randvec(d):
    r = random()*d
    angle = random()*2*pi
    return r*cos(angle)+r*sin(angle)*1j

def make_potfn(ratio, mind, maxd, c1, c2):
    def pot(xs):
        score = 0
        for obj in xs:
            o1 = xs[obj.n1]
            o2 = xs[obj.n2]
            d1 = abs(obj.p-o1.p)
            d2 = abs(obj.p-o2.p)
            r = max(d1,d2)/min(d1,d2)
            d1 = max(d1/maxd,mind/d1)
            d2 = max(d2/maxd,mind/d2)
            ratio_p = (r-ratio)**2
            dist_p = d1**2+d2**2
            cost = c1*dist_p+c2*ratio_p
            score += cost
        return score
    return pot

def make_potfn2(ratio, mind, maxd, c1, c2):
    def pot(xs):
        score = 0
        for obj in xs:
            o1 = xs[obj.n1]
            o2 = xs[obj.n2]
            d1 = abs(obj.p-o1.p)
            d2 = abs(obj.p-o2.p)
            r = max(d1,d2)/min(d1,d2)
            d1 = max(d1/maxd,mind/d1)
            d2 = max(d2/maxd,mind/d2)
            ratio_p = (r-ratio)**2
            dist_p = d1**2+d2**2
            cost = c1*dist_p+c2*ratio_p
            score += cost
        return score
    return pot

class Eqsystem:
    def __init__(self, n, ratio = 1.1, mind = 1., maxd = 10.,
                 c1 = 1, c2 = 1, p = 10, d = 0.1, s = 4.):
        self.bodies = makebodies(n)
        for body in self.bodies:
            body.p = uniform(-s,s)+uniform(-s,s)*1j
        self.pot_fn = make_potfn(ratio, mind, maxd, c1, c2)
        self.p = p
        self.d = d
        self.s = s
        self.iter = 0
    def cost(self):
        return self.pot_fn(self.bodies)
    def updatebody(self,body):
        score = self.cost()
        body.np = body.p
        best = body.p
        for x in xrange(self.p):
            body.p = body.np+randvec(self.d)
            nscore = self.cost()
            if nscore < score:
                score = nscore
                best = body.p
        body.p = body.np
        body.np = best
    def update(self):
        for body in self.bodies:
            self.updatebody(body)
        for body in self.bodies:
            body.p = body.np
        self.iter += 1
    def run(self):
        print self.cost()
        i = 0
        while 1:
            self.update()
            print i, self.cost()
            self.plot()
            i+=1
    def plot(self):
        xs = [body.p.real for body in self.bodies]
        ys = [body.p.imag for body in self.bodies]
        plt.scatter(xs,ys)
        plt.axes().set_aspect('equal')
        plt.axes().set_xlim(-self.s*1.5,self.s*1.5)
        plt.axes().set_ylim(-self.s*1.5,self.s*1.5)
        plt.savefig(str(self.iter)+"test.png", bbox_inches='tight')
        plt.cla()

W = Eqsystem(100)
