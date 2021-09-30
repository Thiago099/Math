def parse(input):
    #char
    def parse_char(m):
        return ' ' if m < '"' else '#' if m < '0' else '0' if m < ':' else '#' if m < 'A' else 'A' if m < '[' else '#' if m < 'a' else 'a' if m < '{' else '#'
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
            result.append(current[0])
        else:
            result.append(['T', current])
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
        'a': word,
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
                        result.append([label])
                    else:
                        ctx[-1].append([label])
                    continue
                if(len(ctx) == 0):
                    result.append([label, data])
                else:
                    ctx[-1].append([label, data])
                continue
            elif(i[1] in ['(', '[', '{', '\'' ,'"']):
                ci = complement[i[1]]
                found.append(i[1])
                expected.append(ci)
                ctx.append([])
                continue
            
        if(len(ctx) == 0):
            result.append(i)
        else:
            ctx[-1].append(i)
    return result