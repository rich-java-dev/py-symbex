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
