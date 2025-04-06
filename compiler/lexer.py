import re

def tokenize(instruction):
    return re.findall(r'\w+|/|=', instruction)
