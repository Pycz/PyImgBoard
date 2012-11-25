import sys
import settings
import sqlite3
import time
import re
import codecs

sstr_pat = re.compile("[a-zA-Z0-9_]")
sstr_num = re.compile("[0-9]")

def get_root_dir():
    return sys.path[0]

def get_template_file(template_name):
    template = None
    root_dir = get_root_dir()
    for dir in settings.TEMPLATE_DIRS:
        try:
            template = open(root_dir +  dir + template_name)
            break
        except IOError:
            pass
    return template

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> test
def strip_tags(s):
    new_s = ''
    for w in s:
        if w == '<':
            new_s += '&lt'
        elif w == '>':
            new_s += '&gt'
        else:
            new_s += w
    return new_s


def wakaba(s):
    i = 0
    sym = ['*', '_']
    stacks = {}
    for d in range(1, 3):
        for x in sym:
            stacks[d * x] = []

    while i < len(s):
        d = 0
        for w in sym:
            if s[i] == w:
                if i + 1 < len(s) and s[i + 1] == w:
                    dw = w + w
                    if isopen(dw, s, i):
                        stacks[dw].append(i)
                        d = 1
                    elif isclose(dw, s, i) and len(stacks[dw]) <> 0:
                        i, s = replace(dw, s, stacks[dw].pop(), i)
                        d = 1
                elif isopen(w, s, i):
                    stacks[w].append(i)
                elif isclose(w, s, i) and len(stacks[w]) <> 0:
                    i, s = replace(w, s, stacks[w].pop(), i)
                break

        i += d + 1
    return s


def isopen(sym, s, i):
    d = len(sym)
    if i - 1 >= 0 and isdop(s[i - 1]) or i - 1 < 0:
        if i + d < len(s) and isgraph(s[i + d]):
            return True
    return False

def isclose(sym, s, i):
    d = len(sym)
    if i - 1 >= 0 and isgraph(s[i - 1]):
        if i + d < len(s) and isdop(s[i + d]) or i + d >= len(s):
            return True
    return False

def replace(sym, s, open_i, close_i):
    rep = ['i', 'b']
    tag = '<' + rep[len(sym) - 1] + '>'
    end_tag = '</' + rep[len(sym) - 1] + '>'
    s = s[:open_i] + tag + s[open_i + len(sym):close_i] + \
        end_tag + s[close_i + len(sym):]
    index = close_i + len(tag) - len(sym) + len(end_tag) - len(sym)
    return index, s

def isgraph(char):
    chars = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    if char.isalnum() or char in chars:
        return True
    else:
        return False

def isdop(char):
    chars = '*_'
    if char.isspace() or char in chars:
        return True
    else:
        return False
<<<<<<< HEAD
=======
=======

>>>>>>> test
def now_timestamp():
    return sqlite3.TimestampFromTicks(time.time())


# ITS A FUCKING BYCICLE I think
def get_normal_string(s):
    ret = str([x for x in s if sstr_pat.match(x)])
    if (not ret) or (sstr_num.match(ret[0])):
        ret+="New"
    return ret 
<<<<<<< HEAD
>>>>>>> upstream/master
=======

>>>>>>> test
