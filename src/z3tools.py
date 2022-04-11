from z3 import *


def get_z3_op_type(op_type):
    if op_type == 'Or':
        return Or

    elif op_type == 'And':
        return And

    elif op_type == 'Not':
        return Not


def get_z3_var(var_id: str, var_type: str):
    if var_type == 'bool':
        return Bool(var_id)
