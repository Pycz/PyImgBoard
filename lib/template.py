# -*- coding: utf-8 -*-
import os
from lib import utils
import settings
import sys

class Template:
    def __init__(self, template_name):
        self.template_name = template_name
        self.template = None

    def render(self, context):
        self.context = context
        self.template = None
        root_dir = utils.get_root_dir()
        for dir in settings.TEMPLATE_DIRS:
            try:
                self.template = open(root_dir + dir + self.template_name)
                break
            except IOError:
                pass

        output = ''
        if not self.template:
            #TODO raise exception
            return output
        try:
            output =  self._text()
        except SyntaxError:
            output = 'Syntax error'
        return output

    def _text(self):
        text = ''
        buf = None
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                    buf = '{'
                else:
                    text += char
            
            elif state == 1:
                state = 0
                if char == '{':
                    self._ungetc(-2)
                    text += self._variable()
#                elif char == '%':
#                    self._ungetc(-2)
#                    text += self._tag()
                else:
                    text += buf + char

            char = self.template.read(1)

        return text

    def _variable(self):
        state = 0
        var_value = None
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError()
            
            elif state == 1:
                if char == '{':
                    state = 2                    
                else:
                    raise SyntaxError()

            elif state == 2:
                if char.isalpha() or char == '_':
                    state = 3
                    self._ungetc(-1)
                    var_value = self._variable_name()
                elif char <> ' ':
                    raise SyntaxError()

            elif state == 3:
                if char == '}':
                    state = 4
                elif char <> ' ':
                    raise SyntaxError()

            elif state == 4:
                if char == '}':
                    break
                else:
                    raise SyntaxError()

            char = self.template.read(1)

        return var_value

    def _variable_name(self):
        state = 0
        var_name = ''
        char = self.template.read(1)
        while (len(char) == 1):
            if char.isalnum() or char == '_':
                var_name += char
            else:
                self._ungetc(-1)
                break
            char = self.template.read(1)
        
        return self.context.get(var_name)
        

    def _ungetc(self, numb):
        self.template.seek(numb, os.SEEK_CUR)
        
        
class Context:
    def __init__(self, context):
        self.context = context

    def get(self, key):
        return self.context.get(key, '')

class SyntaxError(Exception):
    pass
