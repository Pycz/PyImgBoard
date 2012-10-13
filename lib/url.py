# -*- coding: utf-8 -*-
import re

class Url:
    def __init__(self, url_pattern, function):
        self.url_pattern = url_pattern
        self.function = function
        self.pattern = re.compile(url_pattern)

    def is_correct(self, url_string):
        correct = False
        matches = self.pattern.findall(url_string)
        if len(matches) > 0:
            correct = True;
        return correct

    def call_function(self, environ):
        #TODO give only request headers
        #TODO function have to return HttpResponse
        output = self.function(environ)
        return output
