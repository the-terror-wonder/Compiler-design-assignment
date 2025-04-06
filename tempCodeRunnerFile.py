import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from compiler.disassembler import dump_objfile
from compiler.assembler import write_cobj
from compiler.lexer import tokenize
from compiler.parser import parse
import io
from contextlib import redirect_stdout

class MiniCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compiler Debugger")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="MiniLang Source Code:").grid(row=0, column=0, sticky="w")
        self.code_text = tk.Text(frame, height=10, wrap="none", bg="#1e1e1e", fg="#f8f8f2", insertbackground="white")
        self.code_text.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        ttk.Button(frame, text="Compile", bootstyle=SUCCESS, command=self.compile_code).grid(row=2, column=0, sticky="ew", padx=5)
        ttk.Button(frame, text="Load File", bootstyle=PRIMARY, command=self.load_file).grid(row=2, column=1, sticky="ew", padx=5)
        ttk.Button(frame, text="Objdump", bootstyle=INFO, command=self.show_disassembly).grid(row=2, column=2, sticky="ew", padx=5)
        ttk.Button(frame, text="Exit", bootstyle=DANGER, command=self.root.quit).grid(row=2, column=3, sticky="ew", padx=5)

        self.tabs = ttk.Notebook(frame, bootstyle="primary")
        self.tabs.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=10)

        self.symbol_tab = tk.Text(self.tabs, wrap="none", bg="#111", fg="#0f0")
        self.tac_tab = tk.Text(self.tabs, wrap="none", bg="#111", fg="#ff0")
        self.asm_tab = tk.Text(self.tabs, wrap="none", bg="#111", fg="#fff")
        self.exec_tab = tk.Text(self.tabs, wrap="none", bg="#000", fg="#0cf")

        self.tabs.add(self.symbol_tab, text="Symbol Table")
        self.tabs.add(self.tac_tab, text="Three-Address Code")
        self.tabs.add(self.asm_tab, text="Objdump Output")
        self.tabs.add(self.exec_tab, text="Program Output")

        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(3, weight=2)
        frame.columnconfigure((0, 1, 2, 3), weight=1)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("MiniLang Files", ".mc"), ("All Files", ".*")])
        if filepath:
            with open(filepath, 'r') as f:
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert(tk.END, f.read())

    def compile_code(self):
        self.symbol_tab.delete("1.0", tk.END)
        self.tac_tab.delete("1.0", tk.END)
        self.asm_tab.delete("1.0", tk.END)
        self.exec_tab.delete("1.0", tk.END)

        source = self.code_text.get("1.0", tk.END).strip()

        # Handling custom DIVDIV instruction
        if source.startswith("DIVDIV"):
            parts = source.split()
            if len(parts) == 4:
                _, a, b, c = parts
                target = 'result'
                tac_code = f"{target} = {a} / {b} / {c}"
                self.symbol_tab.insert(tk.END, f"Target: {target}\nVariables: {a}, {b}, {c}")
                self.tac_tab.insert(tk.END, tac_code)

                # Result computation
                try:
                    a_val = float(a)
                    b_val = float(b)
                    c_val = float(c)
                    result = a_val / b_val / c_val
                    self.exec_tab.insert(tk.END, f"Compiled custom instruction.\nResult: {target} = {result}")

                    with open("output.cobj", "w") as f:
                        f.write(f"DIVDIV {a} {b} {c} {target}\n")

                except Exception as e:
                    self.exec_tab.insert(tk.END, str(e))
                    messagebox.showerror("Execution Error", str(e))
                return

        # Handling standard expressions like x = 16/4/3
        try:
            tokens = tokenize(source)
            target, ast = parse(tokens)
            write_cobj(ast, target, "output.cobj")

            self.symbol_tab.insert(tk.END, f"Target: {target}\nVariables: {', '.join(set(t for t in tokens if t.isalpha()))}")
            self.tac_tab.insert(tk.END, self.generate_tac(ast, target))

            # Extracting variable values from the source code
            variables = {}
            for token in tokens:
                if token.isalpha() and token not in variables:
                    value = simpledialog.askfloat("Input", f"Enter value for {token}:")
                    variables[token] = value

            result = self.evaluate_ast(ast, variables)
            self.exec_tab.insert(tk.END, f"Compiled successfully.\nResult: {target} = {result}")

        except Exception as e:
            self.exec_tab.insert(tk.END, str(e))
            messagebox.showerror("Compilation Error", str(e))

    def generate_tac(self, ast, target):
        lines = []
        def traverse(node):
            if isinstance(node, tuple):
                left = traverse(node[1])
                right = traverse(node[2])
                temp = f"t{len(lines)}"
                lines.append(f"{temp} = {left} / {right}")
                return temp
            return node
        final = traverse(ast)
        lines.append(f"{target} = {final}")
        return '\n'.join(lines)

    def evaluate_ast(self, ast, variables):
        if isinstance(ast, tuple):
            left = self.evaluate_ast(ast[1], variables)
            right = self.evaluate_ast(ast[2], variables)
            return left / right
        elif ast in variables:
            return variables[ast]
        else:
            return float(ast)

    def show_disassembly(self):
        try:
            with open("output.cobj", "r") as f:
                content = f.read().strip()

            self.asm_tab.delete("1.0", tk.END)

            if content.startswith("DIVDIV"):
                parts = content.split()
                if len(parts) == 5:
                    _, a, b, c, target = parts
                    self.asm_tab.insert(tk.END, f"08049000 <main>:\n")
                    self.asm_tab.insert(tk.END, f"08049000:  cd33     DIVDIV {a}, {b}, {c} -> {target}\n")
                else:
                    self.asm_tab.insert(tk.END, "Invalid DIVDIV format in output.cobj")
            else:
                output_buffer = io.StringIO()
                with redirect_stdout(output_buffer):
                    dump_objfile("output.cobj")
                disassembled_text = output_buffer.getvalue()
                self.asm_tab.insert(tk.END, disassembled_text)

        except Exception as e:
            self.asm_tab.insert(tk.END, f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCompilerGUI(root)
    root.mainloop()
