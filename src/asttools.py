
# Collection of convenience methods for parsing the AST

import ast
import json
from ast2json import ast2json

import asttools
import z3tools
import z3

'''
AST CHEATSHEAT 
https://docs.python.org/3/library/ast.html


stmt = FunctionDef(identifier name, arguments args,
                    stmt* body, expr* decorator_list, expr? returns,
                    string? type_comment)
        | AsyncFunctionDef(identifier name, arguments args,
                            stmt* body, expr* decorator_list, expr? returns,
                            string? type_comment)

        | ClassDef(identifier name,
            expr* bases,
            keyword* keywords,
            stmt* body,
            expr* decorator_list)
        | Return(expr? value)
        | Delete(expr* targets)
        | Assign(expr* targets, expr value, string? type_comment)
        | AugAssign(expr target, operator op, expr value)
        -- 'simple' indicates that we annotate simple name without parens
        | AnnAssign(expr target, expr annotation, expr? value, int simple)

        -- use 'orelse' because else is a keyword in target languages
        | For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        | While(expr test, stmt* body, stmt* orelse)
        | If(expr test, stmt* body, stmt* orelse)
        | With(withitem* items, stmt* body, string? type_comment)
        | AsyncWith(withitem* items, stmt* body, string? type_comment)

        | Match(expr subject, match_case* cases)

        | Raise(expr? exc, expr? cause)
        | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
        | Assert(expr test, expr? msg)

        | Import(alias* names)
        | ImportFrom(identifier? module, alias* names, int? level)

        | Global(identifier* names)
        | Nonlocal(identifier* names)
        | Expr(expr value)
        | Pass | Break | Continue

expr = BoolOp(boolop op, expr* values)
        | NamedExpr(expr target, expr value)
        | BinOp(expr left, operator op, expr right)
        | UnaryOp(unaryop op, expr operand)
        | Lambda(arguments args, expr body)
        | IfExp(expr test, expr body, expr orelse)
        | Dict(expr* keys, expr* values)
        | Set(expr* elts)
        | ListComp(expr elt, comprehension* generators)
        | SetComp(expr elt, comprehension* generators)
        | DictComp(expr key, expr value, comprehension* generators)
        | GeneratorExp(expr elt, comprehension* generators)
        -- the grammar constrains where yield expressions can occur
        | Await(expr value)
        | Yield(expr? value)
        | YieldFrom(expr value)
        -- need sequences for compare to distinguish between
        -- x < 4 < 3 and (x < 4) < 3
        | Compare(expr left, cmpop* ops, expr* comparators)
        | Call(expr func, expr* args, keyword* keywords)
        | FormattedValue(expr value, int conversion, expr? format_spec)
        | JoinedStr(expr* values)
        | Constant(constant value, string? kind)

        -- the following expression can appear in assignment context
        | Attribute(expr value, identifier attr, expr_context ctx)
        | Subscript(expr value, expr slice, expr_context ctx)
        | Starred(expr value, expr_context ctx)
        | Name(identifier id, expr_context ctx)
        | List(expr* elts, expr_context ctx)
        | Tuple(expr* elts, expr_context ctx)

        -- can appear only in Subscript
        | Slice(expr? lower, expr? upper, expr? step)

'''


class FunctionParser():

    def __init__(self, func_name: str, body: dict):
        self.name = func_name
        self.body = body['body']
        self.expr = ""
        self.tests = []
        self.z3e = None

        args = body['args']['args']
        # function args
        self.args = {arg['arg']:
                     z3tools.get_z3_var(arg['arg'], arg['annotation']['id'])
                     for arg in args}

    def debug(self):
        print(f"function: {self.name}")
        print(f"args: {self.args}")
        print(f"body: {self.body}")
        print(f"tests: {self.tests}")
        print(f"expr: {self.expr}")
        print(f"z3e: {self.z3e}")
        print("")

    def parse(self):
        # begin traversing function body
        for line in self.body:

            # detect branching (If statements)
            if self.detect_branching(line):
                self.set_test_expr(line['test'])
                # After Z3 expression is parsed, call Solver
                s = z3.Solver(self.z3e)

    def detect_branching(self, line) -> bool:
        line_type = line['_type']
        # limit implementation to only handle IF statements for now
        return line_type == 'If'

    def set_test_expr(self, test: dict) -> str:
        test_type = test['_type']

        if test_type == 'UnaryOp':
            op_type = test['op']['_type']

        if test_type == 'BoolOp':
            op_type = test['op']['_type']

            # self.expr = f"{op_type}({self.build_test_expr(test)})"
            z3_op = z3tools.get_z3_op_type(op_type)
            self.z3e = z3_op(self.build_z3e(test))

    # DEPRECATED - FOR REFERENCE ONLY
    # def build_test_expr(self, test: dict):
    #     if 'values' in test:
    #         values = test['values']
    #         length = len(values)
    #         for i in range(length):
    #             value = values[i]
    #             var_id = value['id'] if 'id' in value else ''
    #             inner_op = value['_type'] if '_type' in value else ''
    #             inner_op_type = value['op']['_type'] if 'op' in value else ''
    #             if(inner_op == 'UnaryOp'):
    #                 var_id = value['operand']['id']
    #             # print(var_id)
    #             # print(inner_op)
    #             # print(inner_op_type)
    #             if inner_op_type:
    #                 self.expr += inner_op_type+"("
    #                 if var_id:
    #                     self.expr += var_id
    #                 else:
    #                     self.build_test_expr(value)
    #                 self.expr += ")"
    #             elif var_id:
    #                 self.expr += var_id
    #             if(i+1 < length):
    #                 self.expr += ","

    def build_z3e(self, test: dict) -> list:
        sub_expr: list = []
        if 'values' in test:
            values = test['values']
            length = len(values)

            for i in range(length):
                value = values[i]

                var_id = value['id'] if 'id' in value else ''
                inner_op = value['_type'] if '_type' in value else ''
                inner_op_type = value['op']['_type'] if 'op' in value else ''

                if(inner_op == 'UnaryOp'):
                    var_id = value['operand']['id']

                # print(var_id)
                # print(inner_op)
                # print(inner_op_type)

                if inner_op_type:
                    inner_z3_op = z3tools.get_z3_op_type(inner_op_type)
                    inner_z3_operands = None
                    if var_id:
                        if var_id in self.args:
                            inner_z3_operands = self.args[var_id]
                    else:
                        inner_z3_operands = self.build_z3e(value)

                    sub_expr.append(inner_z3_op(inner_z3_operands))

                elif var_id:
                    sub_expr.append(self.args[var_id])

        return sub_expr


"""


"""


class FileParser():

    def __init__(self, filename: str):
        self.ast_tree = ast.parse(open(filename).read())
        self.json_tree = ast2json(self.ast_tree)
        self.functions: list = []

    def results(self):
        for func in self.functions:
            func.debug()

    def parse(self):

        for body in self.json_tree['body']:

            # Current Implementation Only interested in pure function analysis
            if body["_type"] != "FunctionDef":
                continue

            # get function anme from AST
            func_name = body['name']

            parse_func: FunctionParser = FunctionParser(func_name, body)
            parse_func.parse()
            self.functions.append(parse_func)

    def detect_branching(self, line) -> bool:
        line_type = line['_type']
        if line_type == 'If':
            return True

        return False


def get_z3_expression(op_type, arg1, arg2):
    if op_type == 'Name':
        return
    elif(op_type == 'BoolOp'):
        return


def build_model():
    return


def get_input_args(body):
    if body["_type"] != "FunctionDef":
        return

    args = body['args']['args']
    # function args

    return [(arg['annotation']['id'], arg['arg']) for arg in args]
