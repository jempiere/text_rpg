def resolveSequence(seq: str) -> list[int]:
    result = {
    'f': -1,
    'b': -1,
    's': -1
    }

    if len(seq) % 2 != 0: raise Exception(f"Invalid Escape: '{seq}'")

    for i in range(0, len(seq), 2):
        key = seq[i].lower()
        val = seq[i+1]

        if key == 's': val = {
            'b': '2097152',
            'i': '2147483648',
            'u': '131072',
        }.get(val.lower(),'d')

        if val == 'd': val = '-1'

        result[key] = int(val)

    return [result['f'],result['b'],result['s']]


def makeTokens(string: str) -> list[int|str]:
    chunks = string.split('$') # color delimiter

    result: list[int|str] = []

    seq = ''
    for chunk in chunks:
        while len(chunk) >= 2 and chunk[0].lower() in ['f','b','s']:
            seq += chunk[:2]   #add the escape characters to the long sequence
            chunk = chunk[2:]  #remove those characters from the current

        if chunk == '': continue

        result.append(resolveSequence(seq))
        result.append(chunk)
        seq = ''

    return result


def makePairs(curse, tokens) -> list:
    color_counter = 0
    newColor = lambda a,b: curse.init_pair(color_counter,a,b)
    colorPair = lambda : curse.color_pair(color_counter)

    result = []

    pair = {'data': '', 'color': 0}
    filled: int = 0

    for token in tokens:
        if type(token) == list:
            fg, bg, st = token
            newColor(*token[:2])
            pair['color'] = colorPair()

            if st != -1:
                pair['color'] |= st #only include state if it's not defaulted

            color_counter += 1

            filled += 1
        else:
            pair['data'] += token

            filled += 1

        if filled == 2:
            filled = 0
            result.append([pair['data'],pair['color']]) # maybe turn this into an array
            pair = {'data': '', 'color': 0}

    return result

def flatten(pairs: list[int|str]) -> list:
    result = []
    for pair in pairs:
        msg, color = pair
        sublines = ['']
        for char in msg:
            if char != '\n':
                sublines[-1] += char
                continue
            else:
                sublines.append(char)

        if sublines[0] == '': sublines.pop(0)

        for line in sublines:
            result.append([line, color]) #all lines in connected blocks share one color
    return result

def transform(curse, string: str) -> list:
    tokens = makeTokens(string)
    pairs  = makePairs(curse, tokens)
    flats  = flatten(pairs)
    return flats
