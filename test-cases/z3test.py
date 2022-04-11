from z3 import *

a = Bool('a')
b = Bool('b')
c = Bool('c')
s = Solver()

s.add(Or(And(a, Not(b)), c))

s.add(And(a, b, Not(c)))

satisfied = s.check()
print(satisfied)
if satisfied == sat:
    model = s.model()
    print(model)
