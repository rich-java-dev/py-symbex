import argparse
import ast
import json
from ast2json import ast2json

from z3 import *


test_str = '''
a = Bool('a')
b = Bool('b')
c = Bool('c') 
s = Solver()

s.add('Or(And(a, Not(b)), c)')


print(s.check())
model = s.model()
print(model)
'''

eval(test_str)
