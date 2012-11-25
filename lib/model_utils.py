import models
from lib.utils import now_timestamp

def get_simple_board(name = "Random", adr = "b", category_id = 1):
    return models.Board(1, name, adr, adr.upper(), adr.upper(), category_id)

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
    return models.Category(T_id = 1, name = name)