import sys
import settings
import sqlite3
import time
import re
import codecs
import curses.ascii

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
    
    s = insert_quote(s)
    s = insert_urls(s)
    s = s.replace('\r\n', '<br>')
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
    if not char.isspace() or char in chars:
        return True
    else:
        return False

def isdop(char):
    chars = '*_'
    if char.isspace() or char in chars:
        return True
    else:
        return False

def insert_quote(s):
    i = 0
    tag = '<span style="color:#0000ff">'
    end_tag = '</span>'
    s = s.replace('&gt', '>')
    while i < len(s):
        if s[i] == '>' and isquote(s, i):
            s = s[:i] + tag + s[i:]
            i += len(tag)
            j = s.find('\r\n', i)
            if j <> -1:
                s = s[:j] + end_tag + s[j:]
                i = j + len(end_tag) + 2
            else:
                s += end_tag
                break
        else:
            i += 1

    return s
            
def isquote(s, i):
    if i == 0 or (i - 2 >= 0 and s[i - 2:i] == '\r\n'):
        print >> sys.stderr, 's[i - 1: i] = ' + s[i - 2: i]
        return True
    else:
        return False


def insert_urls(s):
    tag = '<a target="_blank" href="'
    mid_tag = '">'
    end_tag = '</a>'
    protocols = ['http:', 'https:', 'ftp:', 'mailto:', 'news:', 'irc:']

    for prot in protocols:
        i = 0
        while i < len(s):
            j = s.find(prot, i)
            if j <> -1:
                blank1 = s.find(' ', j)
                blank2 = s.find('\r\n', j)
                k = 0
                if blank1 == -1 and blank2 == -1:
                    blank = len(s)
                elif blank1 <> -1 and blank2 <> -1:
                    if blank1 < blank2:
                        blank = blank1
                    else:
                        blank = blank2
                elif blank1 == -1 and blank2 <> -1:
                    blank = blank2
                else:
                    blank = blank1

                if protocols.index(prot) < 3:
                    d = '//'
                else:
                    d = ''
                s = s[:j] + tag + s[j:j + len(prot)] + d \
                    + s[j + len(prot):blank] \
                    + mid_tag + s[j + len(prot):blank] \
                    + end_tag + s[blank:]
                i = blank + len(tag + mid_tag + end_tag + d)
            else:
                break
    return s

def now_timestamp():
    return sqlite3.TimestampFromTicks(time.time())


# ITS A FUCKING BYCICLE I think
def get_normal_string(s):
    ret = ""
    fuuu = [str(x) for x in s if sstr_pat.match(x)]
    for i in fuuu:
        ret+=i
    if (not ret) or (sstr_num.match(ret[0])):
        ret = "New" + ret
    return ret 

def get_board_name_from_referer(s):
    x = s.split("/")
    return x[-2]

def get_tread_name_from_referer_rec(s):
    x = s.split("/")
    return x[-2]

def get_board_name_from_referer_rec(s):
    x = s.split("/")
    return x[-3]