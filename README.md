# Mini Compiler for Custom Equation Language

This mini compiler parses and compiles simple division instructions of the form:

z=a/b/c


It generates equivalent Python code, preserving left-associative order.

## Structure

- `compiler/`: Core compiler modules (lexer, parser, AST, code generator)
- `examples/`: Sample input files
- `main.py`: Entry point to run the compiler

## Run

```bash
python main.py examples/test1.mc
