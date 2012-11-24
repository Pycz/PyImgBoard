# -*- coding: utf-8 -*-
import re
from lib.http import HttpRequest, Http404

class Url:
    def __init__(self, url_pattern, function):
        self.url_pattern = url_pattern
        self.function = function
        self.pattern = re.compile(url_pattern)
        self.url_string = None
        self.matches = None

    def is_correct(self, url_string):
        correct = False
        self.url_string = url_string
        self.matches = self.pattern.findall(url_string)
        if len(self.matches) == 1:
            correct = True;
        return correct

    def call_function(self, environ):
        request = HttpRequest(environ)
        try:
            if self.matches[0] is tuple:
                output = self.function(request, *self.matches[0])
            elif self.matches[0] <> self.url_string:
                output = self.function(request, self.matches[0])
            else:
                output = self.function(request)
        except Http404 as h404:
            output = h404

        return output
