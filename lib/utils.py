import sys
import settings
import sqlite3
import time
import models

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

def get_simple_board(name = "Random", adr = "b"):
    return models.Board(1, name, adr, adr.upper(), adr.upper())

def get_simple_tread(last_time = now_timestamp()):
    return models.Tread(1, last_time)

def get_simple_record(name = "Anonymous",
                      email = "",
                      title = "",
                      post = "",
                      image = "",
                      tread_id = ""):
    return models.Record(name = name,
                      email = email,
                      title = title,
                      post = post,
                      image = image,
                      tread_id = tread_id)
    
def get_simple_category(name = "Misc"):
    return models.Category(id = 1, name = name)
    