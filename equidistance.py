from random import choice, shuffle, uniform, random
from math import cos, sin, pi
from collections import namedtuple
import matplotlib.pyplot as plt #you'll need to this plot
import numpy #only used one easily replacable function call from this

class Point:
    def __init__(self, x, n1, n2, p):
        self.x = x #the id number of this point
        self.n1 = n1 #id of first target
        self.n2 = n2 #id of second target
        self.p = p #position stored as complex number
        self.np = p 
        #this variable used as a temporary storage for self.p 
        #when self.p itself is being modified

def goodlist(xs):
    for i in xrange(len(xs)/2):
        if i == xs[2*i] or i == xs[2*i+1] or xs[2*i] == xs[2*i+1]:
            return False
    return True

#construct a system of n points
def makebodies(n):
    b = []
    m = range(n)*2
    while not goodlist(m):
        shuffle(m)
    for x in xrange(0,n):
        b.append(Point(x, m[2*x], m[2*x+1], 0))
    return b

#return a random vector of length d as a complex number
def randvec(d):
    r = random()*d
    angle = random()*2*pi
    return r*cos(angle)+r*sin(angle)*1j

#returns a potential function which takes a list of points (xs)
#and a single point (obj), and returns a score which describes how well
#that point is obeying the rules (of being equidistant to targets
#and not going too far away / getting too close) in the system
#which contains the list of points (xs)
#
#the lower the score the better the point is doing. 0 is perfect.
#actually i'm not sure if you can get 0. 
#i don't remember how i wrote this function.
#
#ratio is a constant which defines the sensitivity of the system 
#(how good each point is at telling distance)
#mind and maxd define the minimum and maximum distance points can be
# ... or something like that
#c1 and c2 are constants which i manually played around with 
#until i got something nice
def make_potfn(ratio, mind, maxd, c1, c2):
    def pot(xs, obj):
        o1 = xs[obj.n1]
        o2 = xs[obj.n2]
        d1 = abs(obj.p-o1.p)
        d2 = abs(obj.p-o2.p)
        r = max(d1,d2)/min(d1,d2)
        dist_p = 0
        for obj2 in xs:
            if (obj.x == obj2.x):
                continue
            d = abs(obj2.p-obj.p)
            dist_p += (max(1,max(d/maxd,mind/d))-1)**2
        d0 = abs(obj.p)
        dist_p += 10*(max(1,max(d0/maxd*2,mind/d0))-1)**2
        ratio_p = max(0,r-ratio)**2
        return c1*ratio_p+c2*dist_p
    return pot

#given two points and a color, plots a perpendicular bisector
def plotbisector(p1,p2,rc):
    dy = p2.imag-p1.imag
    dx = p2.real-p1.real
    my = (p2.imag+p1.imag)/2.
    mx = (p2.real+p1.real)/2.
    y = lambda x: -dx/dy*(x-mx)+my
    plt.plot([-8,8],[y(-8),y(8)],c = rc, zorder=0, alpha = 0.3)
    
#main class
class Eqsystem:
    #n is the number of bodies
    #s is half the size of the initial box
    #d is the timestep
    #p is the number of possible movements each point considers in one timestep
    def __init__(self, n, ratio = 1.0, mind = .5, maxd = 12.,
                 c1 = 1, c2 = 100, p = 10, d = 0.1, s = 4.):
        #initialize points
        self.bodies = makebodies(n)
        for body in self.bodies:
            body.p = uniform(-s,s)+uniform(-s,s)*1j
        self.pot_fn = make_potfn(ratio, mind, maxd, c1, c2/n)
        self.p = p
        self.d = d
        self.s = s
        self.iter = 0 #current iteration
        #this randomly picks colors for all the points
        self.cs = [numpy.random.rand(3,) for body in self.bodies]
        #plot initial state and run the system
        plt.cla()
        self.plot()
        self.run()
    #returns the "cost" of the current configuration
    def cost(self):
        return sum((self.pot_fn(self.bodies, b) for b in self.bodies))
    #updating a single point
    #
    #basically we move the point to random locations, and see if follows
    #the rules it's supposed to any better or not. if it does, then we 
    #move the point to that new location.
    def updatebody(self,body):
        score = self.cost()-.001 #i don't remember why i subtracted .001
        body.np = body.p
        best = body.p
        for x in xrange(self.p):
            body.p = body.np+randvec(self.d)
            nscore = self.pot_fn(self.bodies,body)
            if nscore < score:
                score = nscore
                best = body.p
        body.p = body.np
        #the reason we store the new location of the point away and don't
        #update the location of the point yet, is because we want to update
        #every single point simultaneously. we end up setting 
        #body.p = body.np a few lines below this comment
        body.np = best 
    #update all the points
    def update(self):
        for body in self.bodies:
            self.updatebody(body)
        for body in self.bodies:
            body.p = body.np #right here.
        self.iter += 1
    #run the system and plot in a loop
    def run(self):
        print self.cost()
        i = 0
        while 1:
            self.update()
            print i, #self.cost()
            self.plot()
            i+=1
    #just some boring plotting
    #if you don't want the perpendicular bisectors, set line = False
    def plot(self, line = True):
        for i, body in enumerate(self.bodies):
            if line:
                plotbisector(self.bodies[body.n1].p, self.bodies[body.n2].p,self.cs[i])
            plt.scatter(body.p.real, body.p.imag, c = self.cs[i])
        plt.axes().set_aspect('equal')
        plt.axes().set_xlim(-self.s*2,self.s*2)
        plt.axes().set_ylim(-self.s*2,self.s*2)
        plt.savefig(str(self.iter)+"test.png", bbox_inches='tight')
        plt.cla()

W = Eqsystem(50)
#set up a system with 50 points and run it
