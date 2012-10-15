# -*- coding: utf-8 -*-
import os
from lib import utils
import settings
import sys

class Template:
    def __init__(self, template_name):
        self.template_name = template_name
        self.tags = {'for': self._loop, 'if': self._condition}
        self.endtags = ['endfor', 'endif']
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
                elif char == '%':
                    self._ungetc(-2)
                    text += self._tag()
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
                    var_name = self._variable_name()
                    var_value = self.context.get(var_name)
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

        return str(var_value)
        
    def _tag(self):
        tag_result = None
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError()

            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError()

            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    tag_name = self._get_tag_name()
                    if self.tags.has_key(tag_name):
                       tag_result = self.tags[tag_name]()
                       break
                    else:                        
                        raise SyntaxError()
            char = self.template.read(1)

        return tag_result
        
    
    def _get_tag_name(self):
        tag_name = ''
        char = self.template.read(1)
        while (len(char) == 1):
            if char.isalpha():
                tag_name += char
            elif char == ' ':
                break
            else:
                raise SyntaxError()
            char = self.template.read(1)
        return tag_name

    def _loop(self):
        for_var_name = None
        in_var_name = None
        state = 0
        last_state = False
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    for_var_name = self._variable_name()
                    state = 1
                elif char <> ' ':
                    raise SyntaxError()

            elif state == 1:
                if char == 'i':
                    state = 2
                elif char <> ' ':
                    raise SyntaxError()
            
            elif state == 2:
                if char == 'n':
                    state = 3
                else:
                    raise SyntaxError()

            elif state == 3:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    in_var_name = self._variable_name()
                    state = 4

            elif state == 4:
                if char == '%':
                    state = 5
                elif char <> ' ':
                    raise SyntaxError()
                
            elif state == 5:
                if char == '}':
                    last_state = True
                    break
                else:
                    raise SyntaxError()
            char = self.template.read(1)

        if not last_state:
            #TODO other error need
            raise SyntaxError()
        
        in_var_value = self.context.get(in_var_name)
        if type(in_var_value) != type([]):
            #TODO other error need
            raise SyntaxError

        result = ''
        start_loop = self.template.tell()
        for for_var_value in in_var_value:
            self.template.seek(start_loop)
            self.context.set(for_var_name, for_var_value)
            result += self._body()
            
        self.context.del_var(for_var_name)
        return result

    def _condition(self):
        pass
        
    def _body(self):
        result = ''
        state = 0
        buf = None
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                    buf = '{'
                else:
                    result += char
            
            elif state == 1:
                if char == '{':
                    self._ungetc(-2)
                    result += self._variable()
                    state = 0
                elif char == '%':
                    self._ungetc(-2)
                    if self._is_endtag():
                        self._endtag()
                        break
                    else:
                        result += self._tag()
                else:
                    result += buf + char

            char = self.template.read(1)

        return result
            
    def _is_endtag(self):
        ok = False
        state = 0
        num_of_read_char = 0
        char = self.template.read(1)
        while (len(char) == 1):
            num_of_read_char += 1
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError()
            
            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError()

            elif state == 2:
                if char == 'e':
                    state = 3
                elif char.isalpha():
                    break
                elif char <> ' ':
                    raise SyntaxError()

            elif state == 3:
                if char == 'n':
                    state = 4
                else:
                    break

            elif state == 4:
                if char == 'd':
                    ok = True
                break
                    
            char = self.template.read(1)

        self._ungetc(-num_of_read_char)
        return ok

    def _endtag(self):
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError()

            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError()

            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    endtag_name = self._get_endtag_name()
                    if endtag_name in self.endtags:
                        state = 3
                    else:
                        raise SyntaxError()

            elif state == 3:
                if char == '%':
                    state = 4
                elif char <> ' ':
                    raise SyntaxError()

            elif state == 4:
                if char == '}':
                    break
                else:
                    raise SyntaxError()
            char = self.template.read(1)

    def _get_endtag_name(self):
        endtag_name = ''
        char = self.template.read(1)
        while (len(char) == 1):
            if char.isalpha():
                endtag_name += char
            else:
                self._ungetc(-1)
                break
            char = self.template.read(1)
        return endtag_name

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
        return var_name
        

    def _ungetc(self, numb):
        self.template.seek(numb, os.SEEK_CUR)
        
        
class Context:
    def __init__(self, context):
        self.context = context

    def get(self, key):
        return self.context.get(key, '')

    def set(self, key, value):
        self.context[key] = value

    def del_var(self, key):
        try:
            del self.context[key]
        except KeyError:
            #TODO exception
            pass

class SyntaxError(Exception):
    pass
