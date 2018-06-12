import re
import unicodedata


HALF = ' '
CAP = '\ue302'


def space_priority(char):
    return {'L': 7, 'M': 7, 'N': 5, 'S': 3, 'P': 1,
            'Z': -1, 'C': -3}[unicodedata.category(char)[0]]


def tokenize(s, decap=False, split_punctuation=True):
    """Simple reversible tokenizer"""

    toks = ['']
    current_cat = 0
    for c in s:
        cat = space_priority(c)
        if c == ' ':
            toks[-1] += HALF
            toks.append(HALF)
            current_cat = None
            continue
        elif current_cat is None:
            toks[-1] += c
        elif cat == current_cat and (cat > 2 or not split_punctuation):
            toks[-1] += c # HALF + c
        elif cat <= 0 and current_cat <= 0:
            toks.append(c)
        elif cat <= current_cat:
            toks[-1] += HALF
            toks.append(c)
        else:
            toks.append(HALF + c)
        current_cat = cat
    if toks[0] == '':
        toks = toks[1:]
    if current_cat is not None and current_cat > 0:
        toks[-1] += HALF
    if decap:
        toks = list(map(decapitalize, toks))
    return toks


def decapitalize(tok):
    if len(tok) == 0:
        return tok
    pre, tok = (HALF, tok[1:]) if tok[0] == HALF else ('', tok)
    if tok[0] == tok[0].lower():
        return pre + tok
    if tok[0] == tok[0].upper() and (len(tok) == 1 or tok[1] != tok[1].upper()):
        return CAP + pre + tok[0].lower() + tok[1:]
    return pre + tok

def detokenize(l):
    text = ''.join(l).replace(CAP + HALF, HALF + CAP)
    text = re.sub(HALF + '+', lambda s: ' ' * (len(s.group(0)) // 2), text)
    return re.sub(CAP + '.', lambda s: s.group(0)[-1].upper(), text, flags=re.S)
