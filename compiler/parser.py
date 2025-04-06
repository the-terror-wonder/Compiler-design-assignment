from compiler.ast import build_ast

def parse(tokens):
    if '=' not in tokens or '/' not in tokens:
        raise SyntaxError("Invalid syntax")

    assign_index = tokens.index('=')
    target = tokens[0]
    if assign_index != 1:
        raise SyntaxError("Malformed assignment")

    expr_tokens = tokens[2:]
    if not expr_tokens or expr_tokens[1::2] != ['/'] * ((len(expr_tokens) - 1) // 2):
        raise SyntaxError("Invalid division expression")

    ast = build_ast(expr_tokens)
    return target, ast
