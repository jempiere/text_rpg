
import curses

# Color: \$f[0-9|d] (foreground)
# Color: \$b[0-9|d] (background)
    # 0: 
# 
# Style: \$s[b|u|i|d] (styling)
    # b(old)
    # u(nderline)
    # i(tallic)
    # d(efault)
# Reset



testcase =\
"""$b0$f7░░░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░$fd$bd
$b0$f7░░░░░░░░░░░░▄████████████████▄░░░░░░░░░░$fd$bd      Nicholas cage admonishes you to not commit this $f1$suMURDER$fd$sd.
$b0$f3░░░░░░░░░░▄██▀░░░░░░░▀▀████████▄░░░░░░░░$fd$bd
$b0$f7░░░░░░░░░▄█▀░░░░░░░░░░░░░▀▀██████▄░░░░░░$fd$bd
$b0$f7░░░░░░░░░███▄░░░░░░░░░░░░░░░▀██████░░░░░$fd$bd
$b0$f7░░░░░░░░▄░░▀▀█░░░░░░░░░░░░░░░░██████░░░░$fd$bd
$b0$f7░░░░░░░█▄██▀▄░░░░░▄███▄▄░░░░░░███████░░░$fd$bd
$b0$f7░░░░░░▄▀▀▀██▀░░░░░▄▄▄░░▀█░░░░█████████░░$fd$bd
$b0$f7░░░░░▄▀░░░░▄▀░▄░░█▄██▀▄░░░░░██████████░░$fd$bd
$b0$f7░░░░░█░░░░▀░░░█░░░▀▀▀▀▀░░░░░██████████▄░$fd$bd
$b0$f7░░░░░░░▄█▄░░░░░▄░░░░░░░░░░░░██████████▀░$fd$bd
$b0$f7░░░░░░█▀░░░░▀▀░░░░░░░░░░░░░███▀███████░░$fd$bd
$b0$f7░░░▄▄░▀░▄░░░░░░░░░░░░░░░░░░▀░░░██████░░░$fd$bd
$b0$f7██████░░█▄█▀░▄░░██░░░░░░░░░░░█▄█████▀░░░$fd$bd
$b0$f7██████░░░▀████▀░▀░░░░░░░░░░░▄▀█████████▄$fd$bd
$b0$f7██████░░░░░░░░░░░░░░░░░░░░▀▄████████████$fd$bd
$b0$f7██████░░▄░░░░░░░░░░░░░▄░░░██████████████$fd$bd
$b0$f7██████░░░░░░░░░░░░░▄█▀░░▄███████████████$fd$bd
$b0$f7███████▄▄░░░░░░░░░▀░░░▄▀▄███████████████$fd$bd"""


def toCurses(number):
    if number < 0: return number
    return [curses.COLOR_BLACK, curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_BLUE, curses.COLOR_PURPLE, curses.COLOR_CYAN, curses.COLOR_WHITE][number]


def getMagicStyle(val):
    match val.lower():
        case 'b': return '2097152'
        case 'i': return '2147483648'
        case 'u': return '131072'
    return 'd'

def defseq(string) -> int:
    bg = -1
    fg = -1
    st = -1

    out = {'f':-1,'b':-1,'s':-1}
    if len(string) % 2 != 0:
        raise Exception(f"Invalid Escape Sequence: '{string}'")
        
    for i in range(0,len(string),2):
        key = string[i].lower()
        val = string[i+1]
        
        if key == 's':
            val = getMagicStyle(val)

        if val == 'd' or val == 'D':
            val = '-1'

        out[key] = int(val)

    return [out['f'],out['b'],out['s']] #out['f'] | out['b'] | out['s']


def tokenize(string: str) -> list:
    escapes = string.split('$')
    out = []
    seq = ''
    for escape in escapes:
        while len(escape) >= 2 and escape[0].lower() in 'fbs':
            tag = escape[:2]
            seq += tag
            escape = escape[2:]
        if escape == '':
            continue
        out.append(defseq(seq))
        out.append(escape)
        seq = ''
    return out

def hasColor(curselib, maxpair, tup1, tup2):
    for i in range(maxpair):
        a = curses.color_pair(i)
        if a == (tup1 | tup2):
            return (a,True)
    return (None,False)

def test_str():
    pair_num = 1
    result = []
    pair = ['',0]
    filled = 0
    tokens = tokenize(testcase)
    for item in tokens:
        if type(item) == list:
            curses.init_pair(pair_num,item[0],item[1])
            pair[1] = curses.color_pair(pair_num)
            if item[2] != -1:
                pair[1] |= item[2]
            pair_num += 1
            #search, status = hasColor(curses,pair_num,item[0],item[1])
            #if not status:
            #    curses.init_pair(pair_num,item[0],item[1])
            #    pair[1] = pair_num
            #    pair_num += 1
            #else:
            #    pair[1] = search
            filled+=1
        else:
            pair[0] += item
            filled+=1
            
        if filled == 2:
            result.append(pair)
            pair = ['',0]
            filled = 0

    return result
