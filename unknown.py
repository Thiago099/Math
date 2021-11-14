import tokenizer as to
import math as mt

def solve():
    expression, value = to.parse_group(input)
    print(expression)
    print(value)
    
    unknown = {}
    for i in expression:
        for j in expression[i]:
            for k in j:
                
                def read_char(l):
                    if l in value:
                        return
                    if(l not in unknown):
                        unknown[l] = [i]
                    else:
                        unknown[l].append(i)
                def read_parentesis(l):
                    for m in l:
                        function[m[0]](m[1])
                def nothing(l):
                    pass
                function = {
                    '[' : read_parentesis,
                    '(' : read_parentesis,
                    '{' : read_parentesis,
                    '"' : read_parentesis,
                    '\'': read_parentesis,
                    'A' : read_char,
                    '#' : nothing,
                    'F' : nothing,
                    '0' : nothing
                }
                function[k[0]](k[1])
    print(unknown) 