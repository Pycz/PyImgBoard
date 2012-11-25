# -*- coding: utf-8 -*-
import os
import os.path
import sys
import inspect
from lib import utils
import settings
import types


class Template:
    def __init__(self, template_name):
        self.template_name = template_name
        self.tags = {'for': self._loop, 'if': self._condition, 
                     'block': self._block}

        self.endtags = []
        self.pairs = {}
        for key in self.tags.keys():
            self.endtags.append('end' + key)
            self.pairs[key] = self.endtags[-1]

        self.tags_stack = []
        self.template = None
        self.blocks = None

    def render(self, context):
        self.context = context
        self.template = utils.get_template_file(self.template_name)
        output = ''
        if not self.template:
            #TODO raise exception
            return output
        try:
            output =  self._text()
        except SyntaxError as ser:
            output = str(ser)
        return output

    def _text(self):
        if self._is_extends():
            return self._extends()
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

        if len(self.tags_stack) > 0:
            raise SyntaxError('tags stack is not empty', self._whoami())

        return text

    def _variable(self, do=True):
        state = 0
        var_value = None
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError('expected {', 
                                      self._whoami(), state, 
                                      daddy = self._whosdaddy())
            
            elif state == 1:
                if char == '{':
                    state = 2                    
                else:
                    raise SyntaxError('expected second {', 
                                      self._whoami(), state, 
                                      daddy = self._whosdaddy())

            elif state == 2:
                if char.isalpha() or char == '_':
                    state = 3
                    self._ungetc(-1)
                    var_name = self._variable_name()
                    if do:
                        var_value = self.context.get(var_name)
                    else:
                        var_value = ''
                elif char <> ' ':
                    raise SyntaxError('only blank can be \
                    between {{ and var', self._whoami())

            elif state == 3:
                if char == '}':
                    state = 4
                elif char <> ' ':
                    raise SyntaxError('only blank can be between var and }}', self._whoami())

            elif state == 4:
                if char == '}':
                    break
                else:
                    raise SyntaxError('expected second }', self._whoami())

            char = self.template.read(1)

        return str(var_value)
        
    def _tag(self, do=True):
        tag_result = None
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError('expected {', self._whoami())

            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError('expected %', self._whoami())

            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    tag_name = self._get_tag_name()
                    if self.tags.has_key(tag_name):
                        self.tags_stack.append(tag_name)
                        tag_result = self.tags[tag_name](do)
                        self.tags_stack.pop()
                        break
                    else:                        
                        raise SyntaxError('tag ' + tag_name + ' does \
                        not exist', self._whoami())
                elif char <> ' ':
                    raise SyntaxError('only blank can be between tag \
                    and in', self._whoami())
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
                raise SyntaxError('char ' + char + ' can not be in tag name', self._whoami())
            char = self.template.read(1)
        return tag_name

    def _loop(self, do=True):
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
                    raise SyntaxError('only blank can be between tag and in char = ' + char + ' .', self._whoami(), daddy=self._whosdaddy())

            elif state == 1:
                if char == 'i':
                    state = 2
                elif char <> ' ':
                    raise SyntaxError('expected \'in\'', self._whoami())
            
            elif state == 2:
                if char == 'n':
                    state = 3
                else:
                    raise SyntaxError('expected \'in\'', self._whoami())

            elif state == 3:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    in_var_name = self._variable_name()
                    state = 4
                elif char <> ' ':
                    raise SyntaxError('only blank can be between in and var', self._whoami())

            elif state == 4:
                if char == '%':
                    state = 5
                elif char <> ' ':
                    raise SyntaxError('expected %', self._whoami())
                
            elif state == 5:
                if char == '}':
                    last_state = True
                    break
                else:
                    raise SyntaxError('expected }', self._whoami())

            char = self.template.read(1)

        if not last_state:
            #TODO other error need
            raise SyntaxError('not last state. It is end of file maybe', self._whoami())


        result = ''        
        if not do:
            self._body(False)
        else:
            print >> sys.stderr, 'in_var_name = ' + in_var_name
            in_var_value = self.context.get(in_var_name)
            if type(in_var_value) is list:
                start_loop = self.template.tell()
                for for_var_value in in_var_value:
                    self.template.seek(start_loop)
                    self.context.set(for_var_name, for_var_value)
                    result += self._body()

                if len(in_var_value) <> 0:
                    self.context.del_var(for_var_name)
                else:
                    self._body(False)

            elif type(in_var_value) is dict:
                start_loop = self.template.tell()
                for for_var_value in in_var_value.keys():
                    self.template.seek(start_loop)
                    d = {'key': for_var_value, 'value': in_var_value[for_var_value]}
                    self.context.set(for_var_name, d)
                    result += self._body()

                if len(in_var_value) <> 0:
                    self.context.del_var(for_var_name)
                else:
                    self._body(False)
            else:
                print >> sys.stderr, in_var_name + 'aaa = ' + str(in_var_value)
                raise SyntaxError('type of var after in does not support - ', self._whoami())

        return result

    def _condition(self, do=True):
        state = 0
        predicat_name = None
        last_state = False
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    predicat_name = self._variable_name()
                    state = 1
                elif char <> ' ':
                    raise SyntaxError('only blank can be between if and predicat', self._whoiam())

            elif state == 1:
                if char == '%':
                    state = 2
                elif char <> ' ':
                    raise SyntaxError('expected % or blank', self._whoami())

            elif state == 2:
                if char == '}':
                    last_state = True
                    break
                else:
                    raise SyntaxError('expected }', self._whoami())

            char = self.template.read(1)

        if not last_state:
            #TODO other error
            raise SyntaxError('state is not last', self._whoami(), 
                              daddy = self._whosdaddy())

        result = ''
        if do:
            predicat = self.context.get(predicat_name)
            if not type(predicat) is bool:
                #TODO other error
                raise SyntaxError('only bool is support', self._whoami())

            if predicat:
                result += self._body()
            else:
                self._body(False)
        else:
            self._body(False)

        return result

    def _block(self, do=False):
        last_state = False
        block_name = ''
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    block_name = self._variable_name()
                    state = 1
                elif char <> ' ':
                    raise SyntaxError('expected blank', self._whoami())

            elif state == 1:
                if char == '%':
                    state = 2
                elif char <> ' ':
                    raise SyntaxError('expected %', self._whoami())

            elif state == 2:
                if char == '}':
                    last_state = True
                    break
                else:
                    raise SyntaxError('expected }', self._whoami())
            char = self.template.read(1)

        if not last_state:
            raise SyntaxError('state is not last')

        if self.context.has_key(block_name):
            self._body(False)
            return self.context.get(block_name)
        else:
            return self._body()

    def _body(self, do=True):
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
                    result += self._variable(do)
                    state = 0
                elif char == '%':
                    self._ungetc(-2)
                    if self._is_endtag():
                        self._endtag()
                        break
                    else:
                        result += self._tag(do)
                        state = 0
                else:
                    result += buf + char
                    state = 0

            char = self.template.read(1)
        
        #TODO last state
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
                    raise SyntaxError('expected {', self._whoami())
            
            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError('expected %', self._whoami())

            elif state == 2:
                if char == 'e':
                    state = 3
                elif char.isalpha():
                    break
                elif char <> ' ':
                    raise SyntaxError('only blank can be between {% and tag', self._whoami())

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
        last_state = False
        endtag_name = None
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                else:
                    raise SyntaxError('expected {', self._whoami())

            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    raise SyntaxError('expected %', self._whoami())

            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    endtag_name = self._get_endtag_name()
                    if endtag_name in self.endtags:
                        state = 3
                    else:
                        raise SyntaxError('endtag ' + endtag_name + ' does not exist', self._whoami())

            elif state == 3:
                if char == '%':
                    state = 4
                elif char <> ' ':
                    raise SyntaxError('expected %', self._whoami(), state)

            elif state == 4:
                if char == '}':
                    last_state = True
                    break
                else:
                    raise SyntaxError('expected }', self._whoami(), state)
            char = self.template.read(1)

        if not last_state:
            #TODO other state
            raise SyntaxError('state is not last', self._whoami())

        last_tag = self.tags_stack[-1]
        if self.pairs[last_tag] <> endtag_name:
            raise SyntaxError('end tag is not match', self._whoami())
        
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
        isdot = False
        var_name = ''
        char = self.template.read(1)
        while (len(char) == 1):
            if char.isalnum() or char == '_':
                var_name += char
                isdot = False
            elif char == '.':
                if not isdot:
                    var_name += char
                    isdot = True
                else:
                    raise SyntaxError('two dots', self._whoami())
            else:
                self._ungetc(-1)
                break
            char = self.template.read(1)
        return var_name
    
    def _is_extends(self):
        is_extends = False
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
                elif not char.isspace():
                    break

            elif state == 1:
                if char == '%':
                    state = 2
                else:
                    break

            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    extends_str = self._get_extends_str()
                    if extends_str == 'extends':
                        state = 3
                    else:
                        break
                elif char <> ' ':
                    break

            elif state == 3:
                if char.isalpha() or char == '_':
                    self._ungetc(-1)
                    file_name = self._get_extends_file_name();
                    state = 4
                elif char <> ' ':
                    break
                
            elif state == 4:
                if char == '%':
                    state = 5
                elif char <> ' ':
                    break

            elif state == 5:
                if char == '}':
                    is_extends = True
                else:
                    break
            char = self.template.read(1)

        if is_extends:
            self.extends_file_name = file_name
        else:
            self.template.seek(0)

        return is_extends

    def _extends(self):
        blocks = self._get_blocks()
        template = Template(self.extends_file_name)

        dic_context = self.context.get_dict()
        for key in blocks.keys():
            dic_context[key] = blocks[key]
        context = Context(dic_context)

        return template.render(context)

    def _get_blocks(self):
        blocks = {}
        state = 0
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char == '{':
                    state = 1
            
            elif state == 1:
                if char == '%':
                    state = 2
            
            elif state == 2:
                if char.isalpha():
                    self._ungetc(-1)
                    tag_name = self._get_tag_name()
                    if tag_name == 'block':
                        position = self.template.tell()
                        block_name = self._variable_name()
                        self.template.seek(position)
                        self.tags_stack.append(tag_name)
                        blocks[block_name] = self.tags[tag_name]()
                        state = 0
                    else:
                        raise SyntaxError('only block tag can be in file which extend', self._whoami())
                    
            char = self.template.read(1)

        return blocks

    def _get_extends_str(self):
        state = 0
        extends_str = ''
        len_extends_str = len('extends')
        num = 0
        char = self.template.read(1)
        while (len(char) == 1 and num < len_extends_str):
            extends_str += char
            num += 1
            char = self.template.read(1)

        if num == len_extends_str:
            self._ungetc(-1)

        return extends_str

    def _get_extends_file_name(self):
        last_state = False
        state = 0
        file_name = ''
        char = self.template.read(1)
        while (len(char) == 1):
            if state == 0:
                if char.isalpha() or char == '_':
                    state = 1
                    file_name += char
                else:
                    raise SyntaxError('error in file name which extends', self._whoami())

            elif state == 1:
                if char.isalnum() or char == '_' or char == '.':
                    file_name += char
                elif char == ' ':
                    self._ungetc(-1)
                    last_state = True
                    break
                else:
                    raise SyntaxError('expected blank', self._whoami())

            char = self.template.read(1)

        if not last_state:
            raise SyntaxError('state is not last', self._whoami())
        
        return file_name

    def _ungetc(self, numb):
        self.template.seek(numb, os.SEEK_CUR)
    def _whoami(self):
        return inspect.stack()[1][3]
    def _whosdaddy(self):
        return inspect.stack()[2][3]
        
        
class Context:
    def __init__(self, context):
        self.context = context

    def get(self, key):
        keys = key.split('.')
        result = self.context.get(keys[0])
        print >> sys.stderr, 'result = ' + str(result)
        if not result:
            return ''
        if isinstance(result, (types.FunctionType,
                             types.MethodType,
                             types.BuiltinFunctionType)):
            result = result()
        
        for i in xrange(1, len(keys)):
            if type(result) is dict:
                result = result.get(keys[i])
                print >> sys.stderr, 'r = ' + str(result)
            elif not getattr(result, keys[i], None) is None:
                attr = getattr(result, keys[i])
                if not isinstance(attr, (types.FunctionType,
                                         types.MethodType,
                                         types.BuiltinFunctionType)):
                    result = attr
                else:
                    result = attr()
            elif type(result) is list and type(keys[i]) is int:
                result = result[keys[i]]
            else:
                raise SyntaxError('error type in context',
                                  self._whoami())
                
        return result

    def set(self, key, value):
        self.context[key] = value
    
    def has_key(self, key):
        return self.context.has_key(key)

    def del_var(self, key):
        try:
            del self.context[key]
        except KeyError:
            #TODO exception
            pass

    def get_dict(self):
        return self.context

    def _whoami(self):
        return inspect.stack()[1][3]
    def _whosdaddy(self):
        return inspect.stack()[2][3]


class SyntaxError(Exception):
    def __init__(self, info='unknown', func_name=None, 
                 state=None, daddy=None):
        self.info = info
        self.state = None
        self.func_name = func_name
        self.daddy = daddy

    def __str__(self):
        text = 'SyntaxError: %s' % (self.info,)
        if self.state:
            text += ' state = ' + str(self.state) 
        if self.func_name:
            text += ' in ' + self.func_name
        if self.daddy:
            text += ' daddy: ' + self.daddy
        return text
