def evaluate_ast(ast, context):
    if isinstance(ast, tuple):
        op, left, right = ast
        left_val = evaluate_ast(left, context)
        right_val = evaluate_ast(right, context)
        if op == '/':
            return left_val / right_val
        else:
            raise ValueError(f"Unsupported operator: {op}")
    return context[ast]
