from z3 import *

# build out a mapping from 'AST' generated python string representation Operators
# to Z3's ArithReference
py2z3_op_map: dict = {
    'Or': Or,
    'And': And,
    'Not': Not,
    'Add': ArithRef.__add__,
    'Sub': ArithRef.__sub__,
    'Mul': ArithRef.__mul__,
    'Div': ArithRef.__div__,
    'Eq': ArithRef.__eq__,
    'Gt': ArithRef.__gt__,
    'Lt': ArithRef.__lt__,
    'LtE': ArithRef.__le__,
    'GtE': ArithRef.__ge__,
    'Mod': ArithRef.__mod__,
}

# Fallback execution to evaluate expressions between Z3 and Python.
# May handle some Type inference
py2z3_bkup_op_map: dict = {
    'Or': Or,
    'And': And,
    'Not': Not,
    'Add': int.__add__,
    'Sub': int.__sub__,
    'Mul': int.__mul__,
    'Eq': int.__eq__,
}
# Fallback execution to evaluate expressions between Z3 and Python.
# May handle some Type inference
py2z3_str_op_map: dict = {
    'Or': Or,
    'And': And,
    'Not': Not,
    'Add': SeqRef.__add__,
    'Eq': SeqRef.__eq__,
    'Gt': SeqRef.__gt__,
    'Lt': SeqRef.__lt__,
    'LtE': SeqRef.__le__,
    'GtE': SeqRef.__ge__,
}

# Mapping from Python dict key in string form to Z3 type
py2z3_var_map: dict = {
    'bool': Bool,
    'int': Int,
    'str': String
}


def get_z3_op_type(op_type):
    if op_type in py2z3_op_map:
        return py2z3_op_map[op_type]

    print(f"DEBUG: missing op_type: {op_type}")


def get_z3_var(var_name: str, var_type: str):
    if var_type in py2z3_var_map:
        return py2z3_var_map[var_type](var_name)

    print(f"DEBUG: missing var_type: {var_type}")


def get_z3_bkup_op_type(op_type):
    if op_type in py2z3_bkup_op_map:
        return py2z3_bkup_op_map[op_type]

    print(f"DEBUG: missing op_type: {op_type}")


def get_z3_str_op_type(op_type):
    if op_type in py2z3_str_op_map:
        return py2z3_str_op_map[op_type]

    print(f"DEBUG: missing op_type: {op_type}")


def get_z3_str_value(val):
    return StringVal(val)
