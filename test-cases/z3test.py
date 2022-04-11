from z3 import *

a = Bool('a')
b = Bool('b')
c = Int('c')
s = Solver()

s.add(And(a, Not(b)))
s.add(a == True)

satisfied = s.check()
print(satisfied)
if satisfied == sat:
    model = s.model()
    print(model)
