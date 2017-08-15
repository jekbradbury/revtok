import unicodedata


HALF = ' '


def space_priority(char):
    return {'L': 6, 'M': 6, 'N': 4, 'S': 2, 'P': 0,
            'Z': 0, 'C': 0}[unicodedata.category(char)[0]]


def tokenize(s):
    """Simple reversible tokenizer"""

    toks = ['']
    current_cat = 0
    for c in s:
        cat = space_priority(c)
        if c == ' ':
            toks[-1] += HALF
            toks.append(HALF)
            current_cat = None
        elif current_cat is None or cat == current_cat:
            toks[-1] += c
            current_cat = cat
        else:
            if cat + current_cat == 0:
                toks.append(c)
            elif cat < current_cat:
                toks[-1] += HALF
                toks.append(c)
            else:
                toks.append(HALF + c)
            current_cat = cat
    if toks[0] == '':
        toks = toks[1:]
    if current_cat > 0:
        toks[-1] += HALF
    return toks
    
def detokenize(l):
    return ''.join(l).replace(
        HALF * 2, '\ue301').replace(HALF, '').replace('\ue301', ' ')
