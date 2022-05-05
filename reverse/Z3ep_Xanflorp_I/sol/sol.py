from z3 import *

from random import random
import numpy as np
from z3 import *

##### Set up constraints
SIZE = 3
x = RealVector('x', SIZE)
y = RealVector('y',SIZE)

c11 , c12, c13 = 5,2,3
c21 , c22, c23 = 4,5,6
c31 , c32, c33 = 7,8,5

eq1 = c11*x[0] + c12*x[1] + c13*x[2] + y[0] + y[1] + y[2] == x[0]
eq2 = c21*x[0] + c22*x[1] + c23*x[2] + y[0] - y[1] - y[2] == x[1]
eq3 = c31*x[0] + c32*x[1] + c33*x[2] - y[0] + y[1] - y[2] == x[2]
eq4 = x[0] < -4
eq5 = x[1] > 7
eq6 = x[1] + x[2] == 3
eq7 = x[0] != x[2]

s = Solver()
s.add(eq1,eq2,eq3, eq4, eq5,eq6, eq7)
print(s.check())
print(s.model())
