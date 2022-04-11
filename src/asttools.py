
# Collection of convenience methods for parsing the AST

import ast
import json
from ast2json import ast2json
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

        self.tests = []
        self.constraints = {}
        self.expressions = []
        self.errors = []

        self.z3e = None

        args = body['args']['args']
        # function args
        self.args = {arg['arg']:
                     z3tools.get_z3_var(arg['arg'], arg['annotation']['id'])
                     for arg in args}

    def debug(self):
        print(f"function: {self.name}")
        print(f"args: {self.args}")
        print(f"branch expressions: {self.expressions}")
        print(f"constraints: {self.constraints}")
        print(f"tests: {self.tests}")
        print(f"Errors/Issues: {self.errors}")
        # print(f"body: {self.body}")
        # print(f"expr: {self.expr}")
        print("")

    def parse(self):
        # begin traversing function body
        for line in self.body:

            if self.detect_var(line):
                self.store_var(line)

            elif self.detect_var_change(line):
                self.store_var_change(line)

            # detect branching (If statements)
            elif self.detect_branching(line):
                self.generate_test_expr(line['test'])
                # After Z3 expression is parsed, call Solver
                s = z3.Solver()

                if hasattr(self.z3e,  '__call__'):
                    s.add(self.z3e())
                else:
                    s.add(self.z3e)

                for k, expr in self.constraints.items():
                    s.add(expr())

                satisfied = s.check()
                if satisfied == z3.sat:
                    model = s.model()
                    self.tests.append(model)
                    self.expressions.append(self.z3e)
                else:
                    self.errors.append(f"Unsatisfied: {self.z3e}")

    def detect_var(self, line) -> bool:
        line_type = line['_type']
        return line_type == 'AnnAssign'

    # store variables in Z3 context
    def store_var(self, line):
        var_name = line['target']['id']
        var_type = line['annotation']['id']
        z3_var = z3tools.get_z3_var(var_name, var_type)
        self.args[var_name] = z3_var

        # add a constraint for the variable
        var_value = line['value']['value']
        self.constraints[var_name] = lambda: (z3_var == var_value)

    def detect_var_change(self, line) -> bool:
        line_type = line['_type']
        return line_type == 'Assign'

    def store_var_change(self, line):

        for target in line['targets']:
            var_name = target['id']
            z3_var = self.args[var_name]

            # add a constraint for the variable
            var_value = line['value']['value']
            self.constraints[var_name] = lambda: (z3_var == var_value)

    def detect_branching(self, line) -> bool:
        line_type = line['_type']
        # limit implementation to only handle IF statements for now
        return line_type == 'If'

    def generate_test_expr(self, test: dict):
        test_type = test['_type']

        if test_type in ['UnaryOp', 'BoolOp']:
            op_type = test['op']['_type']

            # self.expr = f"{op_type}({self.build_test_expr(test)})"
            z3_op = z3tools.get_z3_op_type(op_type)
            self.z3e = z3_op(self.build_z3e(test))

        if test_type == 'Compare':
            op_type = test['ops'][0]['_type']
            op_value = test['comparators'][0]['value']
            left_id = test['left']['id']
            left_var = self.args[left_id]
            z3_op = z3tools.get_z3_op_type(op_type)
            self.z3e = lambda: z3_op(left_var, op_value)

    # recursive function to consume/traverse the AST

    def build_z3e(self, test: dict) -> list:
        sub_expr: list = []
        if 'values' in test:
            values = test['values']
            length = len(values)

            for i in range(length):
                value = values[i]

                var_name = value['id'] if 'id' in value else ''
                inner_op = value['_type'] if '_type' in value else ''
                inner_op_type = value['op']['_type'] if 'op' in value else ''

                if(inner_op == 'UnaryOp'):
                    var_name = value['operand']['id']

                # print(var_name)
                # print(inner_op)
                # print(inner_op_type)

                if inner_op_type:
                    inner_z3_op = z3tools.get_z3_op_type(inner_op_type)
                    inner_z3_operands = None
                    if var_name:
                        if var_name in self.args:
                            inner_z3_operands = self.args[var_name]
                    else:
                        inner_z3_operands = self.build_z3e(value)

                    sub_expr.append(inner_z3_op(inner_z3_operands))

                elif var_name:
                    sub_expr.append(self.args[var_name])

        return sub_expr


"""
Root Parser, which iterates over a provided python source file,
then break down and parsed functions

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
