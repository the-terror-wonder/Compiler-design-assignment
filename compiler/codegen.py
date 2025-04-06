def generate_python_code(target, ast):
    def emit(node):
        if isinstance(node, tuple):
            op, left, right = node
            return f"({emit(left)} {op} {emit(right)})"
        return node
    return f"{target} = {emit(ast)}"
