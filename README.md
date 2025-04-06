🧠 Custom Instruction In the Compiler
============================================

A mini compiler built with Python and ttkbootstrap GUI. It supports basic arithmetic expressions and a custom DIVDIV instruction format, with objdump disassembly visualization.

--------------------------
🚀 Features
--------------------------
- Parse and compile expressions like:

  DIVDIV A B C
  
- Special command support:

  DIVDIV A B C
  
- Generate .cobj object code
  
- View output via:
  
  • Symbol Table

  • Three-Address Code (TAC)
  
  • Objdump Output
  
  • Program Output
  
- GUI powered by ttkbootstrap and tkinter

--------------------------
🛠️ Installation
--------------------------
1. Clone the repository:
   
       git clone https://github.com/yourusername/sage_compiler.git
   
       cd sage_compiler

2. Install dependencies:
   
       pip install -r requirements.txt

3. Install `objdump` if missing:
   
       Linux:
   
           sudo apt install binutils
   
       Windows:
   
         Install via MinGW or use WSL

--------------------------
🖥️ Running the GUI
--------------------------

Run:

     python main.py

Make sure `main.py` and the following structure exist:

     compiler/
      ├── lexer.py
      ├── parser.py
      ├── assembler.py
      └── disassembler.py

--------------------------
#💡 Input Format
--------------------------

For Example:

    DIVDIV 16 4 2

Standard assignment:

     x = 16 / 4 / 2

Custom instruction:

     DIVDIV 16 4 2

--------------------------
🌳 Parse Tree (for `x = 16 / 4 / 2`)
--------------------------

The expression is parsed into a right-associative binary tree:

                (/)
               /   \
            (/)     2
           /   \
        16      4

Which evaluates as:

     x = (16 / 4) / 2
   
     x = 4 / 2 = 2.0

--------------------------
🧠 What Happens?
--------------------------

Example: x = 16 / 4 / 2

Tokenized ➝ Parsed ➝ TAC:

     t1 = 16 / 4
   
     t2 = t1 / 2
   
     x = t2

Evaluation ➝ Result: x = 2.0

Custom instruction:

     DIVDIV 16 4 2
   
   ➝ Interpreted as: result = 16 / 4 / 2
   
   ➝ Stored in output.cobj

--------------------------
🔬 Objdump Output
--------------------------

Raw disassembly of output.cobj using:

     objdump -d -M intel output.cobj

To filter relevant instructions:

     objdump -d -M intel output.cobj | grep -E "mov|div|imul|add|sub"

Simplified View:

     mov $16, %eax
   
     mov $4, %ebx
   
     div %ebx       ; EAX = 4
   
     mov $2, %ecx
   
     div %ecx       ; EAX = 2
   
     mov %eax, [x]

--------------------------
📂 Folder Structure
--------------------------
.

├── compiler/

│   ├── lexer.py

│   ├── parser.py

│   ├── assembler.py

│   └── disassembler.py

├── main.py

├── output.cobj

└── README.txt

--------------------------
✅ Output Tabs in GUI
--------------------------

- Symbol Table: shows target and used variables
  
- TAC: shows three-address code breakdown
  
- Objdump: shows disassembled instructions
  
- Program Output: shows final computation result

--------------------------
✨ Author : Amit kumar panchayan
--------------------------
✨ Roll NO. : 23115005
--------------------------
Built with ❤️ for Compiler Design.
