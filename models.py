# -*- coding: utf-8 -*-
import sqlite3
from lib.utils import now_timestamp
from lib.utils import get_root_dir
import lib.utils
import sys

class Category:
    '''Implement all categorys'''
    def __init__(self,
                 T_id,
                 name):
        self.id = T_id
        self.name = name
        
        
class Board:
    '''Implement all boards'''
    def __init__(self,
                 T_id,
                 name,
                 adr,
                 treads_name,
                 records_name,
                 category_id):
        self.id = T_id
        self.name = name
        self.adr = adr
        self.treads_name = treads_name
        self.records_name = records_name
        self.category_id = category_id
        
class Record:
    '''Implements all records on board'''

    def __init__(self, 
                 T_id = 1,
                 timestamp = now_timestamp(),
                 name = "Anonymous",
                 email = "",
                 title = "",
                 post = "",
                 image = "",
                 tread_id = 1):
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
     
    def insert_record_into(self, tread, record, board = lib.utils.get_simple_board()):
        its_records = "records" + board.records_name
        its_treads = "treads" + board.treads_name
        
        self.conection.execute("""
        INSERT INTO %s (name, email, title, post, image, tread_id)
        VALUES (:name, :email, :title, :post, :image, :tread_id)
        """ % (its_records,), 
        {"name": record.name, "email": record.email, 
            "title": record.title, "post": record.post, 
                "image": record.image, "tread_id":  tread.id}) 
        if record.email!="sage": 
            # update time of last adding
            self.conection.execute("""
            UPDATE %s SET last_time = :timestamp WHERE id = :id """ % (its_treads,),
            {"timestamp": now_timestamp(), 
             "id": tread.id})
        
        self.conection.commit()
        
    def get_all_records_from(self, tread, board = lib.utils.get_simple_board()):
        its_records = "records" + board.records_name
        #its_treads = "treads" + board
        
        self.cur.execute(
        """
        SELECT * FROM (%s) WHERE tread_id = (:tread_id) ORDER BY id
        """ % its_records, {"tread_id": str(tread.id)}
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Record)
    
    def get_tread_by_id(self, T_id, board = lib.utils.get_simple_board()):
        its_treads = "treads" + board.records_name
        
        self.cur.execute("""
        SELECT * FROM %s WHERE id = :tread_id""" % (its_treads,),
        {"tread_id": T_id}
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    def get_all_treads(self, board = lib.utils.get_simple_board()):
        its_treads = "treads" + board.records_name
        
        self.cur.execute("""
        SELECT * FROM %s""" % (its_treads,)
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    def get_all_treads_by_date(self, board = lib.utils.get_simple_board()):
        "Returns treads in inverse"
        
        its_treads = "treads" + board.records_name
        
        self.cur.execute("""
        SELECT * FROM %s ORDER BY timestamp DESC""" % (its_treads,)
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread)
    
    def get_y_treads_from_x_position(self, x, y, board = lib.utils.get_simple_board()):
        '''Returns y treads in inverse order 
        Numering from 1'''
        its_treads = "treads" + board.records_name
        
        if x<=0: 
            x=1
        
        self.cur.execute("""
        SELECT * FROM %s ORDER BY timestamp DESC LIMIT %d OFFSET %d""" % (its_treads, y, x-1)
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Tread) 
    
    def get_last_x_records_from_tread(self, tread, x, board = lib.utils.get_simple_board()):
        its_records = "records" + board.records_name
        
        self.cur.execute(
        'SELECT count(*) FROM (%s) WHERE tread_id = (:tread_id)' 
         % its_records, {"tread_id": str(tread.id)})
        quantity = int(self.cur.fetchone()[0])
        if quantity < x:
            skip = 0
        else:
            skip = quantity - x
        
        self.cur.execute(
        """
        SELECT * FROM (%s) WHERE tread_id = (:tread_id) ORDER BY id LIMIT :x OFFSET :skip 
        """ % its_records, {"tread_id": str(tread.id), "x": str(x), "skip": str(skip)}
        )
        
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Record)              
    
    def add_new_board(self, board = lib.utils.get_simple_board()):
        its_records = "records" + board.records_name
        its_treads = "treads" + board.treads_name
        
        self.conection.execute("""
        CREATE TABLE IF NOT EXISTS "%s" 
        (
            "id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , 
            "last_time" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP
        ) 
        """ % (its_treads,)) 
        
        self.conection.execute("""        
        CREATE TABLE IF NOT EXISTS "%s" 
        (
            "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , 
            "timestamp" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
             "name" TEXT NOT NULL  DEFAULT "Anonymous",
             "email" TEXT DEFAULT "",
             "title" TEXT DEFAULT "",
             "post" TEXT NOT NULL  DEFAULT "", 
            "image" TEXT DEFAULT "", 
            "tread_id" INTEGER NOT NULL 
        )""" % (its_records,))
        
        self.conection.commit() 
        
    def get_all_boards_from_category(self, category = lib.utils.get_simple_category()):
        self.cur.execute(
        """
        SELECT * FROM boards WHERE category_id = (:category_id) ORDER BY name 
        """ , {"category_id": str(category.id)}
        )
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Board)
    
    def get_all_categorys(self):
        self.cur.execute(
        """
        SELECT * FROM categorys ORDER BY name 
        """
        )
        return self._list_of_tuple_to_list_of_obj(self.cur.fetchall(), Category) 
           
    def add_new_category(self, category = lib.utils.get_simple_category()):       
        self.cur.execute(
        """
        SELECT count(*) FROM categorys WHERE name = :name 
        """, {"name": category.name}
        )
        if self.cur.fetchone()[0]==0:
            self.conection.execute("""
            INSERT INTO categorys (name)
            VALUES (:name)
            """ , 
            {"name": category.name}) 
            
            self.conection.commit()
        
            
                  
    def __del__(self):
        try:
            self.conection.commit()
        except:
            pass
        
        self.conection.close()
        
    
