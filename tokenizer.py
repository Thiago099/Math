import math as mt
functions = {
    'sin'       : mt.sin,
    'sind'      : lambda a: mt.sin(mt.radians(a)),
    'cos'       : mt.cos,
    'cosd'      : lambda a: mt.cos(mt.radians(a)),
    'tan'       : mt.tan,
    'tand'      : lambda a: mt.tan(mt.radians(a)),
    'acos'      : mt.acos,
    'acosd'     : lambda a: mt.acos(mt.radians(a)),
    'acos'      : mt.acos,
    'acosd'     : lambda a: mt.acos(mt.radians(a)),
    'asin'      : mt.asin,
    'asind'     : lambda a: mt.asin(mt.radians(a)),
    'atan'      : mt.atan,
    'atand'     : lambda a: mt.atan(mt.radians(a)),
}
parentesis = {
    '(':')',
    '[':']',
    '{':'}',
    '\'':'\'',
    '"':'"'
}
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        if(self.type in parentesis.keys()):
            cur = ''
            for i in self.value:
                cur +=  i.__repr__()
            return self.type + cur + parentesis[self.type]
        if(self.type == 'X'):
            return str(self.variable) + '^' + str(self.power)
        return str(self.value)
    def __eq__(self, other):
        if(self.type != other.type):
            return False
        if(self.type == 'X'):
            return self.variable == other.variable and self.power == other.power
        return self.value == other.value
    def __ne__(self, other):
        return not self.__eq__(other)
def parse(input):
    #char
    def parse_char(m):
        return ' ' if m < '"' else '#' if m < '0' else '0' if m < ':' else '#' if m < 'A' else 'A' if m < '[' else '#' if m < 'a' else 'A' if m < '{' else '#'
    parsed_input = []
    current = input[0]
    current_type = parse_char(input[0])
    for j in range(1, len(input)):
        t = parse_char(input[j])
        if(t != current_type or current_type == '#'):
            parsed_input.append([current_type, current])
            current_type = t
            current = ''
        current += input[j]
    parsed_input.append([current_type, current])
    # text
    input = parsed_input
    result = []
    current = []
    i = 0
    def get_text():
        nonlocal current, result
        if(len(current) == 1):
            result.append(['F' if current[0][1] in functions.keys() else 'A', current[0][1]])
        else:
            pos = ''
            for k in current:
                pos += k[1]
            result.append(['F' if pos in functions.keys() else 'A', pos])
        current = []
    
    def word():
        nonlocal i, current, result
        while(i < len(input)):
            if(input[i][0] == '#'):
                if(input[i][1] != '_'):
                    get_text()
                    symbol()
                    return
            if(input[i][0] == ' '):
                get_text()
                i += 1
                return
            current.append(input[i])
            i += 1
        get_text()
    def symbol():
        nonlocal i, current, result
        result.append(input[i])
        i += 1
    
    def number():
        def get_number():
            nonlocal current, result, dot
            compiled = ''
            for i in current:
                compiled += i[1]
            result.append(['0', float(compiled) if dot else int(compiled)])
            current = []
        nonlocal i, current, result
        dot = False
        while(i < len(input)):
            if(input[i][0] == '#'):
                if(input[i][1] != '.'):
                    get_number()
                    symbol()
                    return
                else:
                    dot = True
            if(input[i][0] in ['a', 'A']):
                    get_number()
                    word()
                    return
            if(input[i][0] == ' '):
                get_number()
                i += 1
                return
            current.append(input[i])
            i += 1
        get_number()
    obj = {
        'A': word,
        '#': symbol,
        '0': number
    }
    while(i < len(input)):
        if(input[i][0] == ' '):
            i += 1
        else:
            current = []
            obj[input[i][0]]()
    #tree
    input = result
    expected = []
    found = []
    result = []
    ctx = []
    complement = {
        '(': ')',
        '[': ']',
        '{': '}',
        '\'': '\'',
        '"': '"',
    }
    ci = ''
    for i in input:
        if(i[0] == '#'):
            if(i[1] == ci):
                exp = expected.pop()
                data, label = ctx.pop(), found.pop()
                ci = expected[-1] if len(expected) > 0 else ''
                if(len(data) == 0):
                    label = label + exp
                    if(len(ctx) == 0):
                        result.append(token(label, ''))
                    else:
                        ctx[-1].append(token(label, ''))
                    continue
                if(len(ctx) == 0):
                    result.append(token(label, data))
                else:
                    ctx[-1].append(token(label, data))
                continue
            elif(i[1] in ['(', '[', '{', '\'' ,'"']):
                ci = complement[i[1]]
                found.append(i[1])
                expected.append(ci)
                ctx.append([])
                continue
            
        if(len(ctx) == 0):
            result.append(token(i[0], i[1]))
        else:
            ctx[-1].append(token(i[0], i[1]))
    return result


def parse_group(input):
    expression = {}
    value = {}
    def split(input):
        result = []
        current = []
        for i in input:
            if(i.type == '#' and i.value == '='):
                result.append(current)
                current = []
            else:
                current.append(i)
        result.append(current)
        return result
    for i in input:
        ii = split(i)
        def single(a, b):
            if ii[b][0].type == 'A':
                pos = ii[b][0].value
                if len(ii[a]) == 1:
                    if(ii[a][0].type == 'A'):
                        value[ii[a][0].value] = ii[b][0] 
                    value[pos] = ii[a][0]
                else:
                    try:
                        expression[pos].append(ii[a])
                    except:
                        expression[pos] = [ii[a]]
            
        if len(ii[0]) == 1:
            single(1, 0)
        elif len(ii[1]) == 1:
            single(0, 1)
    return expression, value