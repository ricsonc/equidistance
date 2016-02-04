from random import choice, shuffle, uniform
from collections import namedtuple

class Point:
    def __init__(self, x, n1, n2, p):
        self.x = x
        self.n1 = n1
        self.n2 = n2
        self.p = p

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

#damping upon static state
#scoring fn

class Eqsystem:
    def __init__(self, n):
        self.bodies = makebodies(n)
    def updatebody(body, d):
        pass
    def update(d):
        for body in self.bodies:
            self.updatebody(body, d)
