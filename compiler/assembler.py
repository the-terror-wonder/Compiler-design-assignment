import struct

OPCODES = {
    "MOV": 0,
    "DIV": 1
}

def write_cobj(ast, target, path="output.cobj"):
    instructions = []
    temp_count = 0

    def next_temp():
        nonlocal temp_count
        temp = f"%t{temp_count}"
        temp_count += 1
        return temp

    def walk(node):
        if isinstance(node, tuple):
            op, left, right = node
            left_temp = walk(left)
            right_temp = walk(right)
            result = next_temp()
            instructions.append(("DIV", left_temp, right_temp))
            instructions.append(("MOV", result, None))  # track result
            return result
        else:
            return node

    final_temp = walk(ast)
    instructions.append(("MOV", final_temp, target))

    with open(path, 'wb') as f:
        f.write(b'COBJ')  # header
        f.write(struct.pack("B", len(instructions)))
        for instr in instructions:
            op, a, b = instr
            f.write(struct.pack("B", OPCODES[op]))
            f.write(struct.pack("B", len(a)))
            f.write(a.encode())
            if b:
                f.write(struct.pack("B", len(b)))
                f.write(b.encode())
            else:
                f.write(struct.pack("B", 0))  # no operand B
