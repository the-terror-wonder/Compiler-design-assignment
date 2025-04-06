def build_ast(expr):
    if len(expr) == 1:
        return expr[0]
    return ('/', build_ast(expr[:-2]), expr[-1])
