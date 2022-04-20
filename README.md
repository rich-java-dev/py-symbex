# Py-Symbex

A Static Analysis and Symbolic Execution tool for Analyzing python source code

## Overview

Symbolic Execution is the technique of analyzing source code for the purpose of identifying sets of inputs which lead programs through the various paths of execution without having to explore/test every possible input.


## Note

This tool has only been tested on very basic 'pure' functions with basic data structures.

I'd like to build out more dynamic/symbolic control flow execution

PEP 484 - Type Hints/Annotations are pretty much required to properly parse types to build formal Z3 models at this time.

I do aim to build out more of the AST functionality and maybe then handle type inference better in some circumstances.


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
- [X] non-trivial variable ASSIGNMENT
- [ ] handle FOR loops
- [ ] handle WHILE loops
- [ ] refactor into non-branching structures
- [ ] ternary "a if b else c"

### Built With

* Z3
* python AST
* ast2json
