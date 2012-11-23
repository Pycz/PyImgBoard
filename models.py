# -*- coding: utf-8 -*-
import sqlite3
import time
from lib.utils import get_root_dir
import sys

class Record:
    '''Implements all records on board'''

    def __init__(self, 
                 T_id,
                 date,
                 time,
                 name,
                 email,
                 title,
                 post,
                 image,
                 tread_id):
        self.id = T_id
        self.date = date
        self.time = time
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
        

class Model:
    ''' DB connector '''
    def __init__(self):
        self.conection = sqlite3.connect(get_root_dir()+"/ImageBoard.db")
        self.cur = self.conection.cursor()
     
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
        {"timestamp": sqlite3.TimestampFromTicks(time.time()), 
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
        return self.cur.fetchall()
    
    def get_tread_by_id(self, T_id, board = "B"):
        its_treads = "treads" + board
        self.cur.execute("""
        SELECT * FROM %s WHERE id = :tread_id""" % (its_treads,),
        {"tread_id": T_id})
        return self.cur.fetchall()
    
    def get_all_treads(self, board = "B"):
        its_treads = "treads" + board
        self.cur.execute("""
        SELECT * FROM %s """ % (its_treads,))
        return self.cur.fetchall()
    
    
                 
    def __del__(self):
        try:
            self.conection.commit()
        except:
            pass
        
        self.conection.close()
        
    
