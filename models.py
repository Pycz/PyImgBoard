# -*- coding: utf-8 -*-
import sqlite3
import time
from lib.utils import get_root_dir
import sys

def now_timestamp():
    return sqlite3.TimestampFromTicks(time.time())


class Record:
    '''Implements all records on board'''

    def __init__(self, 
                 T_id,
                 timestamp,
                 name,
                 email,
                 title,
                 post,
                 image,
                 tread_id):
        self.id = T_id
        self.timestamp = timestamp
        self.name = name
        self.email = email
        self.title = title
        self.post = post
        self.image = image
        self.tread_id = tread_id
        
class Tread:
    '''Implement all treads'''
    def __init__(self,
                 T_id,
                 last_time):    
        
        self.id = T_id
        self.last_time = last_time
        
        
    # compare by timestamp
    def __eq__(self, other):    
        return self.last_time==other.last_time
    
    def __ne__(self, other):    
        return self.last_time!=other.last_time 

    def __gt__(self, other):    
        return self.last_time>other.last_time 
    
    def __lt__(self, other):    
        return self.last_time<other.last_time 
    
    def __ge__(self, other):    
        return self.last_time>=other.last_time 
    
    def __le__(self, other):    
        return self.last_time<=other.last_time 
    
           
class Model:
    ''' DB connector '''
    def __init__(self):
        self.conection = sqlite3.connect(get_root_dir()+"/ImageBoard.db")
        self.cur = self.conection.cursor()
        
    def _tuple_to_obj(self, tup, Obj):
        return Obj(*tup)
    
    def _list_of_tuple_to_list_of_obj(self, list_of_t, Obj):
        return [self._tuple_to_obj(tup, Obj) for tup in list_of_t]
     
    def insert_record_into(self, tread, record, board = "B"):
        its_records = "records" + board
        its_treads = "treads" + board
        
        self.conection.execute("""
        INSERT INTO %s (name, email, title, post, image, tread_id)
        VALUES (:name, :email, :title, :post, :image, :tread_id)
        """ % (its_records,), 
        {"name": record.name, "email": record.email, 
            "title": record.title, "post": record.post, 
                "image": record.image, "tread_id":  tread.id}) 
         
        # update time of last adding
        self.conection.execute("""
        UPDATE %s SET last_time = :timestamp WHERE id = :id """ % (its_treads,),
        {"timestamp": now_timestamp(), 
         "id": tread.id})
        
        self.conection.commit()
        
    def get_all_records_from(self, tread, board = "B"):
        its_records = "records" + board
        #its_treads = "treads" + board
        
        self.cur.execute(
        """
        SELECT * FROM (%s) WHERE tread_id = (:tread_id)
        """ % its_records, {"tread_id": str(tread.id)}
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Record)
    
    def get_tread_by_id(self, T_id, board = "B"):
        its_treads = "treads" + board
        
        self.cur.execute("""
        SELECT * FROM %s WHERE id = :tread_id""" % (its_treads,),
        {"tread_id": T_id}
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    def get_all_treads(self, board = "B"):
        its_treads = "treads" + board
        
        self.cur.execute("""
        SELECT * FROM %s """ % (its_treads,)
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    def get_all_treads_by_date(self, board = "B"):
        its_treads = "treads" + board
        
        self.cur.execute("""
        SELECT * FROM %s ORDER BY timestamp""" % (its_treads,)
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    
                 
    def __del__(self):
        try:
            self.conection.commit()
        except:
            pass
        
        self.conection.close()
        
    
