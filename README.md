# Py-Symbex

A Static Analysis and Symbolic Execution tool for Analyzing python source code

## Overview

Symbolic Execution is the technique of analyzing source code for the purpose of identifying sets of inputs which lead programs through the various paths of execution without having to explore/test every possible input.

## Usage

* python src/main.py -f sourcefile.py

## Roadmap

- [X] dump and traverse python source file as AST (Abstract Syntax Tree)
- [X] initial integration of Z3 sat solver
  - [X] handling boolean expressions
    - [X] implement OR, AND, NOT
  - [X] handling int expressions
    - [X] implement equals, greater than, less than, greater or equal, less or equal
- [X] detect IF branching
- [X] handle line traversal and store satisfiable input agruments in tests structure
- [X] handling (store/update) local variables or changes to input variables
- [X] identify dead code/unreachability via failed satisfiable branch conditions
- [X] handle 'ORELSE' (elif/else semantics)
- [ ] handle FOR loops
- [ ] handle WHILE loops
- [ ] refactor into non-branching structures

### Built With

* Z3
* python AST

