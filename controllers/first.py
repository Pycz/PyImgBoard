# -*- coding: utf-8 -*-
from lib.template import Template, Context

def index(request):
    template = Template('index.html')
    a = [1, 2, 3, 4, 5]
    b = [4, 8, 15, 16, 23, 42]
    context = Context({'title': 'Главная страница', 
                       'welcome_text': 'Добро пожаловать!', 
                       'array1': a,
                       'array2': b, 
                       'pred': False})
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
