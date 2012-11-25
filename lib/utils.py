# -*- coding: utf-8 -*-
import sys
import settings
import sqlite3
import time
import re


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

def now_timestamp():
    return sqlite3.TimestampFromTicks(time.time())


# ITS A FUCKING BYCICLE I think
def get_normal_string(s):
    ret = str([x for x in s if sstr_pat.match(x)])
    if (not ret) or (sstr_num.match(ret[0])):
        ret+="New"
    return ret 