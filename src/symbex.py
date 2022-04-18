
# Collection of convenience methods for parsing the AST

import ast
import json
from typing import Set
from ast2json import ast2json
import z3tools
import z3
import copy

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


'''
GET_EXPR
'''


def get_expr(expr):
    return expr() if hasattr(expr,  '__call__') else expr


''''
Function Parser
'''


class FunctionParser():

    def __init__(self, func_name: str, body: dict):

        self.name = func_name
        self.body = body['body']

        self.tests: Set = set()
        self.constraints = {}
        self.expressions = []
        self.errors = []

        args = body['args']['args']
        # function args
        self.args = {arg['arg']:
                     z3tools.get_z3_var(arg['arg'], arg['annotation']['id'])
                     for arg in args}

        # local vars and function args
        self.vars = copy.deepcopy(self.args)

    '''
    DEBUG PRINTER
    '''

    def debug(self):
        print(f"function: {self.name}")
        print(f"args: {self.args}")
        print(f"vars:{self.vars}")

        # print(f"branch expressions: ")
        # for expr in self.expressions:
        #     for k, v in expr.items():
        #         print(get_expr(v))

        # print(f"constraints:")
        # for k, expr in self.constraints.items():
        #     print(get_expr(expr))

        print(f"tests: {self.tests}")

        print(f"Errors/Issues: {self.errors}")
        for err in self.errors:
            print(get_expr(err))

        # print(f"body: {self.body}")
        # print(f"expr: {self.expr}")
        print("")

    '''
    PARSE - base call/initiate parsing of function
    '''

    def parse(self):
        # begin traversing function body
        for line in self.body:
            self.parse_body_line(line)

    '''
    PARSE_BODY_LINE
    '''

    def parse_body_line(self, line, depth=0):

        if self.detect_var(line):
            self.handle_var(line)

        elif self.detect_var_change(line):
            self.handle_var_change(line)

        elif self.detect_branching(line):  # detect branching (If statements)
            self.handle_branching(line, depth)

    '''
    CHECK_SATISFIABILITY
    '''

    def check_satisfiability(self, line: dict):
        # After Z3 expression is parsed, call Solver
        s = z3.Solver()

        for k, expr in self.constraints.items():
            s.add(get_expr(expr))

        z3e = self.constraints

        satisfied = s.check()
        if satisfied == z3.sat:
            model = s.model()
            self.tests.add(str(model))
            self.expressions.append(get_expr(z3e))

        else:
            self.errors.append(
                f"Unsatisfied ({get_expr(z3e)}) - line {line['lineno']}")

    '''
    GET_VAR_VALUES
    '''

    def get_var_value(self, value: dict):
        if 'value' in value:
            return value['value']

        if 'id' in value:
            ref = value['id']

            if ref in self.vars:
                return self.vars[ref]

        return None

    '''
    DETECT VAR
    '''

    def detect_var(self, line) -> bool:
        line_type = line['_type']
        return line_type == 'AnnAssign'

    '''
    DETECT_VAR_CHANGE
    '''

    def detect_var_change(self, line) -> bool:
        line_type = line['_type']
        return line_type == 'Assign'

    '''
    DETECT_OR_ELSE
    '''

    def detect_or_else(self, line) -> bool:
        line_type = line['_type']
        return line_type == 'Assign'

    '''
    DETECT_BRANCHING
    '''

    def detect_branching(self, line) -> bool:
        line_type = line['_type']
        # limit implementation to only handle IF statements for now
        return line_type == 'If'

    '''
    HANDLE_BRANCHING
    '''

    def handle_branching(self, line, depth=0):
        pre_branch_constraints = copy.deepcopy(self.constraints)

        z3e = self.generate_test_expr(line['test'])
        negate_z3e = z3tools.py2z3_op_map['Not'](get_expr(z3e))

        if 'body' in line:
            for sub_line in line['body']:
                self.parse_body_line(sub_line, depth+1)

        self.check_satisfiability(line)

        self.constraints = pre_branch_constraints
        # process or-else blocks
        self.handle_or_else(negate_z3e, line)
        # again, restore constraints
        self.constraints = pre_branch_constraints

    '''
    HANDLE_OR_ELSE
    '''

    def handle_or_else(self, negate_z3e, line=dict):
        if 'orelse' not in line:
            return

        orelse_lines = line['orelse']
        if len(orelse_lines) > 0:
            self.store_constraint(negate_z3e)
            self.check_satisfiability(line)
            for oeline in orelse_lines:
                self.parse_body_line(oeline)

    '''
    HANDLE_VAR
    '''

    def handle_var(self, line):
        # store variables in Z3 context

        var_name = line['target']['id']
        var_type = line['annotation']['id']
        z3_var = z3tools.get_z3_var(var_name, var_type)
        self.vars[var_name] = z3_var

        # add a constraint for the variable
        var_value = self.get_var_value(line['value'])

        self.constraints[var_name] = lambda: (z3_var == var_value)

    '''
    HANDLE_VAR_CHANGE
    '''

    def handle_var_change(self, line):

        for target in line['targets']:
            var_name = target['id']

            z3_var = self.vars[var_name]

            # add a constraint for the variable
            var_value = line['value']['value']
            self.constraints[var_name] = lambda: (z3_var == var_value)

    '''
    GENERATE_TEST_EXPR
    '''

    def generate_test_expr(self, test: dict):
        test_type = test['_type']

        def z3e(): return False

        if test_type == 'Name':
            var_name = test['id']
            z3_var = self.vars[var_name]
            def z3e(): return z3_var == True

        if test_type in ['UnaryOp', 'BoolOp']:
            op_type = test['op']['_type']

            # self.expr = f"{op_type}({self.build_test_expr(test)})"
            z3_op = z3tools.get_z3_op_type(op_type)
            z3e = z3_op(*self.build_z3e(test))

        if test_type == 'Compare':
            z3e = self.handle_compare(test)

        self.store_constraint(z3e)
        return z3e

    '''
    HANDLE COMPARE
    '''

    def handle_compare(self, test):
        op_type = test['ops'][0]['_type']

        comparator = test['comparators'][0]
        op_value = self.get_expr_value(comparator)
        left_expr = self.get_expr_value(test['left'])

        z3_op = z3tools.get_z3_op_type(op_type)
        return z3_op(left_expr, op_value)

    '''
    GET EXPRESSION VALUE
    recursive function to evaluate out test expressions
    '''

    def get_expr_value(self, expr: dict):
        if 'id' in expr:
            expr_id = expr['id']
            return self.vars[expr_id]

        if 'value' in expr:
            return expr['value']

        if 'left' in expr:
            left = self.get_expr_value(expr['left'])
            right = self.get_expr_value(expr['right'])
            op_type = expr['op']['_type']
            z3_op = z3tools.get_z3_op_type(op_type)
            return z3_op(left, right)

    '''
    STORE_CONSTRAINT
    '''

    def store_constraint(self, expr):
        for i in range(0, 100):
            if i in self.constraints:
                continue
            self.constraints[i] = expr
            break

    '''
    BUILD_Z3E
    recursive function to consume/traverse the AST
    '''

    def build_z3e(self, test: dict) -> list:
        sub_expr: list = []

        if 'values' in test:
            values = test['values']
            length = len(values)
            for i in range(length):
                value = values[i]
                sub_expr.append(self.handle_expr_values(value))

        elif 'op' in test:
            var_name = test['operand']['id']
            z3_var = self.vars[var_name]
            sub_expr.append(z3_var)

        return sub_expr

    '''
    HANDLE_EXPR_VALUES
    '''

    def handle_expr_values(self, value):
        var_name = value['id'] if 'id' in value else ''
        inner_op = value['_type'] if '_type' in value else ''
        inner_op_type = value['op']['_type'] if 'op' in value else ''

        if(inner_op == 'UnaryOp'):
            var_name = value['operand']['id']
        elif(inner_op == 'Compare'):
            return self.handle_compare(value)

        if inner_op_type:
            inner_z3_op = z3tools.get_z3_op_type(inner_op_type)
            inner_z3_operands = None
            if var_name:
                if var_name in self.vars:
                    inner_z3_operands = self.vars[var_name]
            else:
                inner_z3_operands = self.build_z3e(value)

            return inner_z3_op(inner_z3_operands)
        elif var_name:
            return self.vars[var_name]


"""
Root Parser, which iterates over a provided python source file,
then break down and parsed functions

"""


class FileParser():

    def __init__(self, filename: str):
        self.ast_tree = ast.parse(open(filename).read())
        self.json_tree = ast2json(self.ast_tree)
        self.functions: list = []

    '''
    '''

    def results(self):
        for func in self.functions:
            func.debug()

    '''
    '''

    def print_ast(self):
        print(json.dumps(self.json_tree, indent=4))

    '''
    '''

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

    '''
    '''

    def detect_branching(self, line) -> bool:
        line_type = line['_type']
        if line_type == 'If':
            return True

        return False