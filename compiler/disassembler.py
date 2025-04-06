import struct

OPCODES_REVERSE = {
    0: "MOV",
    1: "DIV"
}

FAKE_OPCODES = {
    "MOV": "89 e5",  # totally fake — could be mov %esp, %ebp
    "DIV": "f7 f1",  # fake div %ecx
}

def read_cobj(path="output.cobj"):
    with open(path, 'rb') as f:
        if f.read(4) != b'COBJ':
            raise ValueError("Invalid object file")
        count = struct.unpack("B", f.read(1))[0]
        instructions = []
        for _ in range(count):
            opcode = struct.unpack("B", f.read(1))[0]
            len_a = struct.unpack("B", f.read(1))[0]
            a = f.read(len_a).decode()
            len_b = struct.unpack("B", f.read(1))[0]
            b = f.read(len_b).decode() if len_b else None
            instructions.append((OPCODES_REVERSE[opcode], a, b))
        return instructions

def dump_objfile(path="output.cobj"):
    instrs = read_cobj(path)

    print("08049000 <main>:")
    addr = 0x08049000
    for op, a, b in instrs:
        hex_addr = f"{addr:08x}"
        opcode_bytes = FAKE_OPCODES.get(op, "??")
        operands = f"{a}, {b}" if b else a
        asm_line = f"{op.lower():<6} {operands}"
        print(f"{hex_addr}:  {opcode_bytes:<8}  {asm_line}")
        addr += 3  # simulate 3-byte x86 instructions
