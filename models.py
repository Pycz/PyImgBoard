# -*- coding: utf-8 -*-
import sqlite3

class Record:
    '''Implements all records on board'''

    def __init__(self, 
                 number):
        self.number = number
        
