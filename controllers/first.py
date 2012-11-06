# -*- coding: utf-8 -*-
from lib.template import Template, Context

def index(request):
    template = Template('index.html')
    context = Context({'welcome_text': 'Добро пожаловать'})
    result = template.render(context)
    return result

def faq(request):
    template = Template('faq.html')
    context = Context({'s': 'gogog ogogog'})
    return template.render(context)

def downloads(request):
    return 'downloads'

def other(request):
    return request['REQUEST_URI']

def board(request, name):
    #TODO get 'name' board comments
    return 'name = ' + name
