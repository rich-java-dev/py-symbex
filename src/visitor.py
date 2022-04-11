from collections import defaultdict
import ast


class SimpleVisitor(ast.NodeVisitor):

    def generic_visit(self, node):
        print(node)
        ast.NodeVisitor.generic_visit(self, node)
